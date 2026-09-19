#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(cmd, *, capture=False):
    print("+", " ".join(map(str, cmd)), flush=True)
    if capture:
        p = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE)
        return p.stdout
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--output", default="observation_output")
    ap.add_argument("--preset", choices=["motion", "standard"], default="motion")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--remote-path", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--video-id", default="")
    args = ap.parse_args()

    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"Missing required binary: {binary}")

    video = Path(args.video).resolve()
    root = Path(args.output).resolve()
    clips = root / "clips"
    sheets = root / "contact_sheets"
    audio = root / "audio"
    meta = root / "metadata"
    for d in (clips, sheets, audio, meta):
        d.mkdir(parents=True, exist_ok=True)

    duration = float(run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video)
    ], capture=True).strip())

    if args.preset == "motion":
        clip_seconds, sample_fps = 60, 2.0
    else:
        clip_seconds, sample_fps = 120, 0.5

    audio_streams = run([
        "ffprobe", "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "csv=p=0", str(video)
    ], capture=True).strip()
    has_audio = bool(audio_streams)

    if has_audio:
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", str(video),
            "-vn", "-c:a", "aac", "-b:a", "128k", str(audio / "audio.m4a")
        ])

    clip_cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", str(video),
        "-vf", "scale=-2:'min(720,ih)'",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
    ]
    if has_audio:
        clip_cmd += ["-c:a", "aac", "-b:a", "128k"]
    else:
        clip_cmd += ["-an"]
    clip_cmd += [
        "-force_key_frames", f"expr:gte(t,n_forced*{clip_seconds})",
        "-f", "segment", "-segment_time", str(clip_seconds), "-reset_timestamps", "1",
        str(clips / "clip_%04d.mp4")
    ]
    run(clip_cmd)

    tile_count = 16
    vf = (
        f"fps={sample_fps},scale=480:-2,"
        "drawtext=text='%{pts\\:hms}':x=8:y=h-th-8:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.65,"
        f"tile=4x4:nb_frames={tile_count}:padding=2:margin=2"
    )
    try:
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
            "-i", str(video), "-vf", vf, "-q:v", "3",
            str(sheets / "sheet_%04d.jpg")
        ])
    except subprocess.CalledProcessError:
        vf = f"fps={sample_fps},scale=480:-2,tile=4x4:nb_frames={tile_count}:padding=2:margin=2"
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
            "-i", str(video), "-vf", vf, "-q:v", "3",
            str(sheets / "sheet_%04d.jpg")
        ])

    manifest = {
        "source_url": args.source_url,
        "remote_path": args.remote_path,
        "video_id": args.video_id,
        "title": args.title,
        "duration_seconds": duration,
        "preset": args.preset,
        "clip_seconds": clip_seconds,
        "contact_sheet_fps": sample_fps,
        "source_file_name": video.name,
        "has_audio": has_audio,
    }
    (root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (meta / "source.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"PACK_PATH={root}")


if __name__ == "__main__":
    main()
