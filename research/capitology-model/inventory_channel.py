"""Metadata-only inventory; no media, captions, or gameplay are downloaded/analyzed.

Run from repository root:
python research/capitology-model/inventory_channel.py --source-dir /path/to/enumerations
Source directory must contain yt-dlp channel-flat.json and uploads-flat.json.
"""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHANNEL_ID = 'UCk7BWWbiI8yNdLWt9BdAM9g'

def extract_object(html, name):
    match = re.search(r'(?:var )?' + name + r'\s*=\s*(\{)', html)
    return json.JSONDecoder().raw_decode(html[match.start(1):])[0] if match else None

def inspect_video(item):
    vid = item['video_id']
    url = 'https://www.youtube.com/watch?v=' + vid
    row = dict(item, url=url, upload_date=None, upload_datetime=None,
               publish_datetime=None, description=None, captions={'availability': 'unknown', 'tracks': []},
               availability='unknown', metadata_gaps=[], checked_at=None)
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=25) as response:
                html = response.read().decode('utf-8')
            player = extract_object(html, 'ytInitialPlayerResponse')
            if not player:
                raise ValueError('ytInitialPlayerResponse missing')
            details = player.get('videoDetails', {})
            micro = player.get('microformat', {}).get('playerMicroformatRenderer', {})
            status = player.get('playabilityStatus', {})
            tracks = player.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
            reason = status.get('reason', '')
            low = reason.lower()
            availability = ('public' if status.get('status') == 'OK' else
                            'access_blocked' if 'not a bot' in low else
                            'private' if 'private' in low else
                            'deleted' if 'removed' in low or 'deleted' in low else 'unavailable')
            if availability == 'public' and micro.get('isUnlisted'):
                availability = 'unlisted'
            row.update(title=details.get('title', row.get('title')),
                       duration_seconds=int(details['lengthSeconds']) if details.get('lengthSeconds') else row.get('duration_seconds'),
                       description=details.get('shortDescription'),
                       upload_datetime=micro.get('uploadDate'), publish_datetime=micro.get('publishDate'),
                       upload_date=micro.get('uploadDate', '')[:10] or None,
                       availability=availability, playability_status=status.get('status'),
                       availability_reason=reason or None, channel_id=details.get('channelId'),
                       is_live_content=details.get('isLiveContent'),
                       captions={'availability': 'available' if tracks else ('not_advertised' if status.get('status') == 'OK' else 'unknown'),
                                 'manual_available': any(t.get('kind') != 'asr' for t in tracks) if status.get('status') == 'OK' else None,
                                 'automatic_available': any(t.get('kind') == 'asr' for t in tracks) if status.get('status') == 'OK' else None,
                                 'tracks': [{'language_code': t.get('languageCode'),
                                             'name': t.get('name', {}).get('simpleText') or ''.join(r.get('text', '') for r in t.get('name', {}).get('runs', [])),
                                             'kind': 'automatic' if t.get('kind') == 'asr' else 'manual',
                                             'is_translatable': t.get('isTranslatable')} for t in tracks]},
                       checked_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                       source={'url': url, 'method': 'YouTube watch HTML: ytInitialPlayerResponse',
                               'response_sha256': hashlib.sha256(html.encode()).hexdigest()})
            # Retain only relevant raw metadata, excluding signed media/caption URLs.
            evidence = {'video_id': vid, 'checked_at': row['checked_at'], 'playability_status': status,
                        'video_details': {k: details.get(k) for k in ['videoId', 'title', 'lengthSeconds', 'shortDescription', 'channelId', 'author', 'isPrivate', 'isLiveContent']},
                        'microformat': {k: micro.get(k) for k in ['uploadDate', 'publishDate', 'isUnlisted', 'externalChannelId', 'canonicalUrl']},
                        'caption_tracks': row['captions']['tracks'], 'html_sha256': row['source']['response_sha256']}
            (ROOT / 'inventory-evidence' / (vid + '.json')).write_text(json.dumps(evidence, indent=2) + '\n')
            break
        except Exception as exc:
            row['retrieval_error'] = str(exc)
            if attempt == 0:
                time.sleep(1)
    else:
        row['availability'] = 'unknown_retrieval_failed'
    for key in ['title', 'upload_date', 'duration_seconds', 'description']:
        if row.get(key) is None:
            row['metadata_gaps'].append(key)
    if row['captions']['availability'] == 'unknown':
        row['metadata_gaps'].append('caption_availability')
    if row.get('channel_id') and row['channel_id'] != CHANNEL_ID:
        row['metadata_gaps'].append('channel_identity_mismatch')
    if row.get('duration_seconds') is not None:
        s = row['duration_seconds']
        row['duration'] = f'{s//3600:02}:{s%3600//60:02}:{s%60:02}'
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path, required=True)
    args = parser.parse_args()
    channel = json.loads((args.source_dir / 'channel-flat.json').read_text())
    uploads = json.loads((args.source_dir / 'uploads-flat.json').read_text())
    prior_path = ROOT / 'pass01_public_index.preliminary.json'
    prior = json.loads(prior_path.read_text())
    items = {}
    for tab in channel['entries']:
        for entry in tab.get('entries', []):
            items[entry['id']] = {'video_id': entry['id'], 'title': entry.get('title'),
                                  'duration_seconds': entry.get('duration'),
                                  'upload_type': 'short' if tab['webpage_url'].endswith('/shorts') else 'video',
                                  'discovery_sources': [tab['webpage_url']]}
    for entry in uploads['entries']:
        item = items.setdefault(entry['id'], {'video_id': entry['id'], 'title': entry.get('title'), 'duration_seconds': entry.get('duration'), 'upload_type': 'unknown', 'discovery_sources': []})
        item['discovery_sources'].append(uploads['webpage_url'])
    for playlist_path in args.source_dir.glob('*-playlist-flat.json'):
        playlist = json.loads(playlist_path.read_text())
        for entry in playlist.get('entries', []):
            item = items.setdefault(entry['id'], {'video_id': entry['id'], 'title': entry.get('title'), 'duration_seconds': entry.get('duration'), 'upload_type': 'unknown', 'discovery_sources': []})
            item['discovery_sources'].append(playlist['webpage_url'])
    for entry in prior['verified_uploads']:
        item = items.setdefault(entry['video_id'], {'video_id': entry['video_id'], 'title': entry.get('title'), 'duration_seconds': None, 'upload_type': 'unknown', 'discovery_sources': []})
        item['discovery_sources'].append('preliminary Pass 1')
    current_path = ROOT / 'pass01_public_index.json'
    if current_path.exists():
        for entry in json.loads(current_path.read_text()).get('videos', []):
            item = items.setdefault(entry['video_id'], {'video_id': entry['video_id'], 'title': entry.get('title'), 'duration_seconds': entry.get('duration_seconds'), 'upload_type': entry.get('upload_type', 'unknown'), 'discovery_sources': []})
            if 'previous inventory' not in item['discovery_sources']:
                item['discovery_sources'].append('previous inventory')
    (ROOT / 'inventory-evidence').mkdir(exist_ok=True)
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for row in pool.map(inspect_video, items.values()):
            rows.append(row)
            print(f"{len(rows)}/{len(items)} {row['video_id']} {row['availability']} gaps={row['metadata_gaps']}", flush=True)
    result = {'schema_version': 1, 'pass': 1, 'status': 'public_inventory_complete' if all(not r['metadata_gaps'] for r in rows) else 'public_inventory_with_metadata_gaps',
              'captured_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'channel': {'name': channel['channel'], 'channel_id': CHANNEL_ID, 'url': channel['channel_url'], 'handle': channel['uploader_id']},
              'scope': 'All publicly enumerated Videos + Shorts + uploads playlist + public playlists; prior known IDs retained. Hidden private/deleted/unlisted uploads cannot be exhaustively enumerated without owner access.',
              'caption_semantics': 'Tracks advertised by the watch-page player. not_advertised means no caption track in this successful public response, not proof captions never existed. Caption text and media were not downloaded.',
              'summary': {'unique_videos': len(rows),
                          'videos_tab_count': sum(len(t.get('entries', [])) for t in channel['entries'] if t['webpage_url'].endswith('/videos')),
                          'shorts_tab_count': sum(len(t.get('entries', [])) for t in channel['entries'] if t['webpage_url'].endswith('/shorts')),
                          'uploads_playlist_count': len(uploads['entries'])},
              'videos': sorted(rows, key=lambda r: (r['upload_datetime'] or '', r['video_id']), reverse=True)}
    (ROOT / 'pass01_public_index.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')

if __name__ == '__main__':
    main()
