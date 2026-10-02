"""Capture Pass 6 windows on a runner that can reach YouTube media.

The output contains silent clips and sparse check frames. Inspection and
claim adjudication are separate tasks; a successful download is not review.
"""

import argparse
import base64
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
URL_RE = re.compile(r"https?://[^\s]+")


def run(args, timeout=600):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def short_error(output):
    lines = [line for line in output.splitlines() if "ERROR:" in line or "error" in line.lower()]
    return URL_RE.sub("[media URL omitted]", " | ".join(lines[-2:])[:500])


def node_path():
    runner_temp = os.environ.get("RUNNER_TEMP")
    if not runner_temp:
        raise RuntimeError("RUNNER_TEMP is required for media retrieval")
    root = Path(runner_temp).parents[1]
    for version in ("node24", "node20"):
        p = root / "externals" / version / "bin" / "node.exe"
        if p.exists():
            return p
    raise RuntimeError("Runner Node executable was not found")


def download_source(video_id, source_dir, cookie_path):
    js = ["--js-runtimes", f"node:{node_path()}", "--remote-components", "ejs:github"]
    url = f"https://www.youtube.com/watch?v={video_id}"
    target = str(source_dir / "source.%(ext)s")
    last_error = ""
    for mode in ("anonymous", "cookies"):
        if mode == "cookies" and not cookie_path:
            continue
        for stale in source_dir.glob("source.*"):
            stale.unlink()
        args = [sys.executable, "-m", "yt_dlp", *js, "--no-cache-dir", "--no-playlist",
                "--no-progress", "--no-warnings", "--force-overwrites",
                "-f", "bv*[height<=480]/b[height<=480]/best[height<=480]",
                "-o", target]
        if mode == "cookies":
            args.extend(["--cookies", str(cookie_path)])
        args.append(url)
        p = run(args)
        files = list(source_dir.glob("source.*"))
        if p.returncode == 0 and len(files) == 1 and files[0].stat().st_size > 10000:
            print(f"{video_id}: downloaded {files[0].stat().st_size} bytes ({mode})", flush=True)
            return files[0]
        last_error = short_error(p.stderr + "\n" + p.stdout)
        print(f"{video_id}: {mode} failed: {last_error}", flush=True)
    raise RuntimeError(last_error or "no video bytes returned")


def capture_window(ffmpeg, source, row, output):
    wid, video_id = row["window_id"], row["video_id"]
    start, end = int(row["start_seconds"]), int(row["end_seconds"])
    base = f"{wid}_{video_id}_{start}-{end}"
    clip = output / "clips" / f"{base}.mp4"
    args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start),
            "-i", str(source), "-t", str(end-start), "-an", "-c:v", "libx264",
            "-crf", "22", "-preset", "veryfast", str(clip)]
    p = run(args, timeout=300)
    if p.returncode or not clip.exists() or clip.stat().st_size < 10000:
        raise RuntimeError(short_error(p.stderr) or "clip encode failed")
    frames = []
    for label, offset in (("start", 0), ("middle", (end-start)//2), ("end", end-start-1)):
        frame = output / "frames" / f"{base}_{label}.jpg"
        p = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                 "-ss", str(offset), "-i", str(clip), "-frames:v", "1", str(frame)], timeout=60)
        if p.returncode or not frame.exists() or frame.stat().st_size < 1000:
            raise RuntimeError(short_error(p.stderr) or f"{label} frame missing")
        frames.append(str(frame.relative_to(output)))
    return {"window_id": wid, "video_id": video_id, "start_seconds": start,
            "end_seconds": end, "clip": str(clip.relative_to(output)),
            "clip_size_bytes": clip.stat().st_size,
            "clip_sha256": hashlib.sha256(clip.read_bytes()).hexdigest(),
            "check_frames": frames, "retrieval_status": "retrieved_video_only",
            "visual_review_status": "not_reviewed"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--source-cache", type=Path, help="local proof run for one video without download")
    args = ap.parse_args()
    request = json.loads(args.request.read_text())
    ids = request["video_ids"]
    if not isinstance(ids, list) or not 1 <= len(ids) <= 4 or len(set(ids)) != len(ids):
        raise SystemExit("request must contain one to four unique video IDs")
    if any(not re.fullmatch(r"[A-Za-z0-9_-]{11}", x) for x in ids):
        raise SystemExit("invalid video ID")
    rows = list(csv.DictReader((ROOT / "pass06_retrieval_queue.csv").open(newline="")))
    if any(x not in {r["video_id"] for r in rows} for x in ids):
        raise SystemExit("video ID not in Pass 6 queue")
    if args.source_cache and len(ids) != 1:
        raise SystemExit("local source cache accepts exactly one video")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "clips").mkdir(exist_ok=True)
    (args.output / "frames").mkdir(exist_ok=True)
    source_dir = args.output / "_source"
    source_dir.mkdir(exist_ok=True)
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg = "ffmpeg"

    manifest = {"batch_key": request.get("batch_key"), "video_ids": ids,
                "media": "silent 480p-or-lower clips; original timecodes",
                "windows": [], "failures": []}
    with tempfile.TemporaryDirectory() as tmp:
        cookie_path = None
        if os.environ.get("YOUTUBE_COOKIES_B64") and not args.source_cache:
            cookie_path = Path(tmp) / "cookies.txt"
            cookie_path.write_bytes(base64.b64decode(os.environ["YOUTUBE_COOKIES_B64"]))
        for video_id in ids:
            try:
                source = args.source_cache or download_source(video_id, source_dir, cookie_path)
                for row in rows:
                    if row["video_id"] != video_id:
                        continue
                    try:
                        item = capture_window(ffmpeg, source, row, args.output)
                        manifest["windows"].append(item)
                        print(f"{item['window_id']}: {item['clip_size_bytes']} bytes", flush=True)
                    except Exception as e:
                        manifest["failures"].append({"window_id": row["window_id"], "error": str(e)[:500]})
                if not args.source_cache:
                    source.unlink(missing_ok=True)
            except Exception as e:
                manifest["failures"].append({"video_id": video_id, "error": str(e)[:500]})
            finally:
                (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"captured {len(manifest['windows'])} windows; {len(manifest['failures'])} failures", flush=True)
    return 0 if not manifest["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
