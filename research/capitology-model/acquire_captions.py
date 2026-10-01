"""Acquire advertised English captions and build normalized, timed transcripts.

This is a caption-only Pass 2 collector. It does not download video or audio.
"""
import concurrent.futures
import argparse
import datetime as dt
import hashlib
import gzip
import html
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'captions' / 'raw-json3'
RAW_GZ = ROOT / 'captions' / 'raw-json3-gz'
SEG = ROOT / 'captions' / 'segments'
TEXT = ROOT / 'captions' / 'text'
LOG = ROOT / 'captions' / 'logs'
INVENTORY = ROOT / 'pass01_public_index.json'

def timestamp(ms):
    sec = max(0, ms // 1000)
    return f'{sec//3600:02}:{sec%3600//60:02}:{sec%60:02}.{ms%1000:03}'

def normalize_text(value):
    value = html.unescape(value).replace('\u200b', '').replace('\xa0', ' ')
    value = re.sub(r'[ \t\r\f\v]+', ' ', value)
    value = re.sub(r' *\n *', '\n', value)
    return value.strip()

def parse_json3(path):
    source = json.loads(path.read_text())
    segments = []
    for event in source.get('events', []):
        parts = event.get('segs')
        if not parts:
            continue
        text = normalize_text(''.join(part.get('utf8', '') for part in parts))
        if not text or text == '\n':
            continue
        start = int(event.get('tStartMs', 0))
        duration = int(event.get('dDurationMs', 0))
        segments.append({'start_ms': start, 'end_ms': start + duration,
                         'start': timestamp(start), 'end': timestamp(start + duration),
                         'text': text})
    return source, segments

def acquire(video):
    video_id = video['video_id']
    target = RAW / f'{video_id}.en.json3'
    log_path = LOG / f'{video_id}.log'
    attempts = []
    if not target.exists() or target.stat().st_size == 0:
        for attempt in range(1, 4):
            command = ['python', '-m', 'yt_dlp', '--skip-download', '--write-auto-subs',
                       '--sub-langs', 'en', '--sub-format', 'json3', '--ignore-no-formats-error',
                       '--socket-timeout', '30', '--retries', '2', '--fragment-retries', '2',
                       '--paths', str(RAW), '--output', '%(id)s.%(ext)s', video['url']]
            if Path('youtube_cookies.txt').exists():
                command[3:3] = ['--cookies', 'youtube_cookies.txt']
            started = time.time()
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=150)
            attempts.append({'attempt': attempt, 'returncode': result.returncode,
                             'elapsed_seconds': round(time.time() - started, 3),
                             'output': result.stdout})
            if target.exists() and target.stat().st_size:
                break
            time.sleep(attempt * 2)
    log_path.write_text(json.dumps({'video_id': video_id, 'attempts': attempts}, indent=2) + '\n')
    if not target.exists() or target.stat().st_size == 0:
        return {'video_id': video_id, 'status': 'failed', 'attempts': len(attempts),
                'error': attempts[-1]['output'][-1000:] if attempts else 'missing output'}
    try:
        source, segments = parse_json3(target)
    except Exception as exc:
        return {'video_id': video_id, 'status': 'parse_failed', 'error': str(exc)}
    compressed = RAW_GZ / f'{video_id}.en.json3.gz'
    with gzip.GzipFile(filename='', mode='wb', fileobj=compressed.open('wb'), mtime=0) as output:
        output.write(target.read_bytes())
    duration_ms = video['duration_seconds'] * 1000
    spoken = [s for s in segments if not (s['text'].startswith('[') and s['text'].endswith(']'))]
    text = ' '.join(s['text'].replace('\n', ' ') for s in spoken)
    words = re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE)
    record = {'video_id': video_id, 'title': video['title'], 'url': video['url'],
              'upload_date': video['upload_date'], 'duration_seconds': video['duration_seconds'],
              'caption_language': 'en', 'caption_kind': 'automatic',
              'source_format': 'YouTube json3', 'acquired_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'source_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'source_bytes': target.stat().st_size, 'segment_count': len(segments),
              'word_count': len(words), 'character_count': len(text),
              'first_segment_ms': segments[0]['start_ms'] if segments else None,
              'last_segment_end_ms': segments[-1]['end_ms'] if segments else None,
              'leading_gap_seconds': round(segments[0]['start_ms']/1000, 3) if segments else None,
              'trailing_gap_seconds': round(max(0, duration_ms - segments[-1]['end_ms'])/1000, 3) if segments else None,
              'status': 'acquired' if segments else 'empty_track', 'segments': segments}
    (SEG / f'{video_id}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    lines = [f'# {video["title"]}', '', f'Video ID: `{video_id}`', f'URL: {video["url"]}',
             f'Upload date: {video["upload_date"]}', 'Caption source: English automatic captions', '', '## Transcript', '']
    lines.extend(f'[{s["start"]}] {s["text"].replace(chr(10), " ")}' for s in segments)
    (TEXT / f'{video_id}.md').write_text('\n'.join(lines) + '\n')
    return {k: record[k] for k in record if k != 'segments'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    for directory in [RAW, RAW_GZ, SEG, TEXT, LOG]: directory.mkdir(parents=True, exist_ok=True)
    inventory = json.loads(INVENTORY.read_text())
    videos = inventory['videos']
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(acquire, video): video for video in videos}
        for future in concurrent.futures.as_completed(futures):
            try: row = future.result()
            except Exception as exc: row = {'video_id': futures[future]['video_id'], 'status': 'failed', 'error': repr(exc)}
            rows.append(row)
            print(f'{len(rows)}/{len(videos)} {row["video_id"]} {row["status"]}', flush=True)
    rows.sort(key=lambda r: next(i for i,v in enumerate(videos) if v['video_id'] == r['video_id']))
    acquired = [r for r in rows if r['status'] == 'acquired']
    manifest = {'schema_version': 1, 'pass': 2, 'status': 'complete' if len(acquired)==len(videos) else 'incomplete',
                'captured_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'scope': 'Advertised English automatic captions only; no video/audio acquisition or content analysis.',
                'summary': {'inventory_videos': len(videos), 'captions_acquired': len(acquired),
                            'failed': len(videos)-len(acquired), 'total_segments': sum(r.get('segment_count',0) for r in acquired),
                            'total_words': sum(r.get('word_count',0) for r in acquired),
                            'total_source_bytes': sum(r.get('source_bytes',0) for r in acquired)},
                'videos': rows}
    (ROOT / 'pass02_caption_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

if __name__ == '__main__': main()
