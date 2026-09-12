#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def run(cmd, *, capture=False):
    print('+', ' '.join(map(str, cmd)), flush=True)
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE if capture else None)
    if p.returncode != 0:
        if capture:
            if p.stdout:
                print(p.stdout, flush=True)
            if p.stderr:
                print(p.stderr, flush=True)
        raise subprocess.CalledProcessError(p.returncode, cmd, p.stdout, p.stderr)
    return p.stdout if capture else None


def safe_name(text: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', text)
    text = re.sub(r'\s+', ' ', text).strip(' .')
    return text[:100] or 'video'


def ytdlp_base(client: str | None = None):
    cmd = ['yt-dlp', '--no-warnings']
    if client:
        cmd += ['--extractor-args', f'youtube:player_client={client}']
    return cmd


def probe_metadata(url: str):
    clients = [None, 'web_embedded', 'android_vr', 'tv_downgraded', 'ios']
    last = None
    for client in clients:
        try:
            print(f'Attempting metadata with client={client or "default"}', flush=True)
            out = run(ytdlp_base(client) + ['--dump-single-json', '--skip-download', url], capture=True)
            return json.loads(out), client
        except subprocess.CalledProcessError as e:
            last = e
            print(f'Metadata attempt failed for client={client or "default"}', flush=True)
    raise last or RuntimeError('All metadata strategies failed')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('url')
    p.add_argument('--preset', choices=['standard', 'motion'], default='motion')
    p.add_argument('--max-height', type=int, choices=[360, 480, 720, 1080], default=1080)
    p.add_argument('--output', default='observation_output')
    args = p.parse_args()

    for binary in ('yt-dlp', 'ffmpeg', 'ffprobe'):
        if not shutil.which(binary):
            raise SystemExit(f'Missing required binary: {binary}')

    root = Path(args.output).resolve()
    root.mkdir(parents=True, exist_ok=True)

    metadata, client = probe_metadata(args.url)
    vid = str(metadata.get('id', 'video'))
    title = safe_name(str(metadata.get('title', vid)))
    pack = root / f'{vid}-{title}'
    source = pack / 'source'
    clips = pack / 'clips'
    sheets = pack / 'contact_sheets'
    audio = pack / 'audio'
    captions = pack / 'captions'
    meta = pack / 'metadata'
    for d in (source, clips, sheets, audio, captions, meta):
        d.mkdir(parents=True, exist_ok=True)

    (meta / 'info.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')

    fmt = f'bv*[height<={args.max_height}]+ba/b[height<={args.max_height}]/best'
    download_cmd = ytdlp_base(client) + [
        args.url, '-f', fmt,
        '--merge-output-format', 'mp4',
        '-o', str(source / 'source.%(ext)s'),
        '--write-subs', '--write-auto-subs', '--sub-langs', 'all,-live_chat',
        '--convert-subs', 'vtt', '--write-info-json', '--no-overwrites',
    ]
    try:
        run(download_cmd)
    except subprocess.CalledProcessError:
        # Last-resort broader client rotation. Useful when one client returns metadata
        # but its media URLs are blocked on a datacenter IP.
        run([
            'yt-dlp', '--extractor-args',
            'youtube:player_client=web_embedded,android_vr,tv_downgraded,ios',
            args.url, '-f', fmt, '--merge-output-format', 'mp4',
            '-o', str(source / 'source.%(ext)s'), '--write-info-json', '--no-overwrites'
        ])

    videos = sorted(p for p in source.iterdir() if p.suffix.lower() in {'.mp4', '.mkv', '.webm', '.mov'})
    if not videos:
        raise SystemExit('No source video produced.')
    video = videos[0]

    for f in list(source.iterdir()):
        if f == video:
            continue
        if f.suffix.lower() in {'.vtt', '.srt', '.ass'}:
            shutil.move(str(f), captions / f.name)
        elif f.name.endswith('.info.json'):
            shutil.move(str(f), meta / 'yt-dlp.info.json')

    duration = float(run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(video)
    ], capture=True).strip())

    if args.preset == 'motion':
        clip_seconds, sample_fps = 60, 2.0
    else:
        clip_seconds, sample_fps = 120, 0.5

    run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(video),
         '-vn', '-c:a', 'aac', '-b:a', '128k', str(audio / 'audio.m4a')])

    run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(video),
         '-vf', "scale=-2:'min(720,ih)'", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24',
         '-c:a', 'aac', '-b:a', '128k',
         '-force_key_frames', f'expr:gte(t,n_forced*{clip_seconds})',
         '-f', 'segment', '-segment_time', str(clip_seconds), '-reset_timestamps', '1',
         str(clips / 'clip_%04d.mp4')])

    tile_count = 16
    vf = (f'fps={sample_fps},scale=480:-2,'
          "drawtext=text='%{pts\\:hms}':x=8:y=h-th-8:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.65,"
          f'tile=4x4:nb_frames={tile_count}:padding=2:margin=2')
    try:
        run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(video), '-vf', vf,
             '-q:v', '3', str(sheets / 'sheet_%04d.jpg')])
    except subprocess.CalledProcessError:
        vf = f'fps={sample_fps},scale=480:-2,tile=4x4:nb_frames={tile_count}:padding=2:margin=2'
        run(['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(video), '-vf', vf,
             '-q:v', '3', str(sheets / 'sheet_%04d.jpg')])

    manifest = {
        'url': args.url,
        'video_id': vid,
        'title': metadata.get('title'),
        'duration_seconds': duration,
        'preset': args.preset,
        'max_height': args.max_height,
        'player_client': client or 'default',
        'clip_seconds': clip_seconds,
        'contact_sheet_fps': sample_fps,
        'source_file': str(video.relative_to(pack)),
    }
    (pack / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    (pack / 'README.txt').write_text(
        f"Title: {metadata.get('title')}\nDuration: {duration:.1f}s\nPreset: {args.preset}\n"
        f"Source: {video.name}\nClips: {clip_seconds}s each\nContact sheets: {sample_fps} sampled fps\n",
        encoding='utf-8')
    print(f'PACK_PATH={pack}')


if __name__ == '__main__':
    main()
