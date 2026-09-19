#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def require(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required command: {name}")


def safe_name(text: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return (text[:120] or "video").strip()


def cookie_args(browser: str | None, cookies_file: str | None) -> list[str]:
    if cookies_file and Path(cookies_file).exists():
        return ["--cookies", cookies_file]
    if browser:
        return ["--cookies-from-browser", browser]
    return []


def run_capture(cmd: list[str]) -> str:
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=sys.stderr)
    if p.returncode != 0:
        raise SystemExit(p.returncode)
    return p.stdout


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--remote", default="youtube-drive:")
    ap.add_argument("--browser", default="firefox")
    ap.add_argument("--cookies-file", default=None)
    ap.add_argument("--max-height", type=int, default=720)
    args = ap.parse_args()

    require("yt-dlp")
    require("rclone")

    cookies = cookie_args(args.browser, args.cookies_file)
    fmt = f"b[height<={args.max_height}]/b"

    metadata_cmd = [
        "yt-dlp", "--no-warnings", *cookies,
        "-f", fmt,
        "--dump-single-json", "--skip-download",
        args.url,
    ]
    raw = run_capture(metadata_cmd)
    meta = json.loads(raw)

    vid = str(meta.get("id") or "video")
    title = safe_name(str(meta.get("title") or vid))
    ext = str(meta.get("ext") or "mp4")
    if ext not in {"mp4", "webm", "mkv", "mov"}:
        ext = "mp4"

    filename = f"{vid} - {title}.{ext}"
    remote = args.remote
    if not remote.endswith(":") and not remote.endswith("/"):
        remote += "/"
    remote_path = f"{remote}{filename}"

    print(f"Streaming {vid} directly to {remote_path}", file=sys.stderr, flush=True)

    ytdlp_cmd = [
        "yt-dlp", "--no-warnings", *cookies,
        "-f", fmt,
        "-o", "-",
        args.url,
    ]
    rclone_cmd = [
        "rclone", "rcat", remote_path,
        "--stats", "15s",
        "--stats-one-line",
        "--drive-chunk-size", "32M",
    ]

    yt = subprocess.Popen(ytdlp_cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
    assert yt.stdout is not None
    rc = subprocess.Popen(rclone_cmd, stdin=yt.stdout, stdout=sys.stderr, stderr=sys.stderr)
    yt.stdout.close()

    rc_code = rc.wait()
    yt_code = yt.wait()

    if yt_code != 0:
        raise SystemExit(f"yt-dlp failed with exit code {yt_code}")
    if rc_code != 0:
        raise SystemExit(f"rclone failed with exit code {rc_code}")

    result = {
        "video_id": vid,
        "title": title,
        "ext": ext,
        "remote_path": filename,
        "source_url": args.url,
        "max_height": args.max_height,
    }
    print("RESULT_JSON=" + json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
