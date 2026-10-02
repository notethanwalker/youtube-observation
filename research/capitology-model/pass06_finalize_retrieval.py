"""Verify captured Pass 6 windows and build portable clip archives and registry."""

import csv
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MEDIA = Path(sys.argv[1])
QUEUE = {r["window_id"]: r for r in csv.DictReader((ROOT / "pass06_retrieval_queue.csv").open())}
SOURCES = {
    "part1": ["batch-trial-01", "local-proof"],
    "part2": ["batch-02"],
    "part3": ["batch-03"],
    "part4": ["batch-04"],
}
RUNS = {"part1": [37003705370], "part2": [37004151152],
        "part3": [37004457970], "part4": [37004518270]}
RECOVERED = {
    "V6-11": ("batch-02", "GKkzCd9cvUg", 712, 869),
    "V6-14": ("batch-03", "MYW1ztAeDQc", 751, 927),
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def duration(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(p.stdout.strip())


registry = {}
for part, sources in SOURCES.items():
    entries = []
    for source in sources:
        base = MEDIA / source
        manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8-sig"))
        for row in manifest["windows"]:
            assert sha(base / row["clip"]) == row["clip_sha256"], row["window_id"]
            entries.append(dict(row, _base=base))
        for failure in manifest["failures"]:
            wid = failure["window_id"]
            assert wid in RECOVERED, failure
            src, vid, start, end = RECOVERED[wid]
            assert source == src
            name = f"{wid}_{vid}_{start}-{end}"
            clip = f"clips/{name}.mp4"
            entries.append({"window_id": wid, "video_id": vid, "start_seconds": start,
                            "end_seconds": end, "clip": clip,
                            "clip_sha256": sha(base / clip),
                            "check_frames": [f"frames/{name}_{label}.jpg" for label in
                                             ("start", "middle", "end")],
                            "recovery_note": "Trimmed captured source-end clip to corrected queue boundary",
                            "_base": base})
    archive = MEDIA / f"Capitology_Pass6_clips_{part}.zip"
    if part != "part1":
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as out:
            for row in sorted(entries, key=lambda r: r["window_id"]):
                wid = row["window_id"]
                q = QUEUE[wid]
                assert (row["video_id"], row["start_seconds"], row["end_seconds"]) == (
                    q["video_id"], int(q["start_seconds"]), int(q["end_seconds"])), wid
                assert abs(duration(row["_base"] / row["clip"]) - int(q["duration_seconds"])) < 0.6, wid
                assert sha(row["_base"] / row["clip"]) == row["clip_sha256"], wid
                for f in [row["clip"], *row["check_frames"]]:
                    assert (row["_base"] / f).stat().st_size > 1000, (wid, f)
                    out.write(row["_base"] / f, f)
            out.writestr("manifest.json", json.dumps({"part": part, "source_runs": RUNS[part],
                "windows": [{k: v for k, v in r.items() if k != "_base"} for r in entries]},
                indent=2) + "\n")
    for row in entries:
        wid = row["window_id"]
        assert wid in QUEUE and wid not in registry, wid
        q = QUEUE[wid]
        assert (row["video_id"], row["start_seconds"], row["end_seconds"]) == (
            q["video_id"], int(q["start_seconds"]), int(q["end_seconds"])), wid
        clip = row["_base"] / row["clip"]
        assert abs(duration(clip) - int(q["duration_seconds"])) < 0.6, wid
        for frame in row["check_frames"]:
            assert (row["_base"] / frame).stat().st_size > 1000, (wid, frame)
        registry[wid] = {
            "video_id": row["video_id"], "start_seconds": row["start_seconds"],
            "end_seconds": row["end_seconds"], "archive": archive.name,
            "clip": row["clip"], "clip_sha256": row["clip_sha256"],
            "check_frames": row["check_frames"], "source_runs": RUNS[part],
            "retrieval_status": "retrieved_video_only", "visual_review_status": "not_reviewed",
            **({"recovery_note": row["recovery_note"]} if "recovery_note" in row else {}),
        }
    print(part, len(entries), archive.stat().st_size, sha(archive))

assert set(registry) == set(QUEUE), (set(QUEUE) - set(registry), set(registry) - set(QUEUE))
(ROOT / "pass06_retrieval_registry.json").write_text(json.dumps({"windows": registry}, indent=2) + "\n")
print("Verified", len(registry), "windows")
