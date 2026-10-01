# Pass 1 — complete public-discovery inventory

Collected 2026-10-01 UTC. Metadata only; no gameplay analysis, transcript ingestion, audio acquisition, or media downloads.

## Results

| Measure | Result |
|---|---:|
| Unique known uploads | 54 |
| Public Videos-tab entries | 48 |
| Public Shorts-tab entries | 5 |
| Uploads playlist entries | 53 |
| Additional unlisted video from public playlist | 1 |
| Advertised English automatic captions | 54 |
| Advertised manual caption tracks | 0 |
| Known records with metadata gaps | 0 |
| Confirmed private/deleted/unavailable records | 0 |

Channel identity: Capitology, `UCk7BWWbiI8yNdLWt9BdAM9g`, `https://www.youtube.com/@capitology`.

Dates: 2023-10-27 to 2026-09-29. Total duration: 52,413 seconds (14:33:33). Dates are the calendar dates in YouTube's `uploadDate`; exact timestamps retain their supplied offsets. `publishDate` is separately preserved.

Additional unlisted upload: `c92ESPjlveI`, **What are turns?**, uploaded 2023-11-28, duration 998 seconds. It appears in public playlist `PLxP1_pmCHjexukvwiRi8pdPS7q8JWOtEB` (Overwatch Macro), but not in the channel tabs or uploads playlist. Its own player microformat explicitly reports `isUnlisted: true`, and its channel ID matches Capitology.

## Method and reconciliation

1. Clone the existing research repository and preserve the preliminary Pass 1 JSON before replacing the authoritative file.
2. Use yt-dlp 2026.08.19 in flat-playlist mode to enumerate the channel URL. Its Videos and Shorts tab results contain 48 and 5 records respectively.
3. Independently enumerate the channel's uploads playlist `UUk7BWWbiI8yNdLWt9BdAM9g`: its 53 IDs exactly match the union of Videos + Shorts, without duplicates.
4. Check Streams: yt-dlp reports that this channel has no Streams tab.
5. Enumerate the public Playlists tab: one playlist, Overwatch Macro. Its sole entry supplies the additional unlisted ID.
6. Union these sets with both IDs in preliminary Pass 1 (`x2jNJeKiMUU`, `SJdCkYn6Is0`). Both already appear in the complete public listing.
7. Retrieve each watch page using four concurrent requests. Read `ytInitialPlayerResponse.videoDetails`, `microformat.playerMicroformatRenderer`, `playabilityStatus`, and `captions.playerCaptionsTracklistRenderer.captionTracks`.
8. Preserve only relevant metadata in per-video evidence files; exclude signed playback/caption URLs, cookie data, and media. Record source URL, timestamp, and HTML SHA-256 for provenance. The raw HTML is temporary and is not committed.
9. Validate unique IDs, channel identity, required fields, durations, caption tracks, source reconciliation, evidence coverage, and JSON/CSV agreement before writing the repository update.

`KLwLiiYYewQ` initially returned LOGIN_REQUIRED with “Sign in to confirm that you're not a bot.” A subsequent watch-page request succeeded; its Shorts route also succeeded. The final row is public and complete. This transient access restriction was not classified as private/deleted.

## Coverage and gaps

The known 54 rows have no unresolved required metadata gaps. An empty string description means YouTube supplied an empty description; null would mean unavailable. Caption availability means tracks advertised by YouTube, not a tested transcript download. No manual caption tracks were advertised. Automatic translation options are not counted as independent uploaded tracks.

The inventory is exhaustive for the public channel tabs, uploads playlist, and public playlist exposed during this run, plus previously known IDs. It cannot promise every upload ever made: private/deleted uploads and unlisted links absent from public playlists may be undiscoverable. Their count and IDs are **unknown**, not zero. No inaccessible placeholders were exposed in the enumerated sources. Future discovered IDs should be added and explicitly classified, preserving gaps rather than inventing metadata.

The preliminary indirect references dated 2025-08-10, 2025-09-24, and 2026-09 did not carry video IDs. They remain preserved in the preliminary archive and the inventory coverage notes, unresolved. Metadata alone cannot conclusively map them to an upload.

## Refresh

Install current yt-dlp, then collect metadata-only flat listings into a source directory:

```bash
python -m yt_dlp --flat-playlist --dump-single-json --skip-download --ignore-errors 'https://www.youtube.com/@Capitology' > channel-flat.json
python -m yt_dlp --flat-playlist --dump-single-json --skip-download --ignore-errors 'https://www.youtube.com/playlist?list=UUk7BWWbiI8yNdLWt9BdAM9g' > uploads-flat.json
python -m yt_dlp --flat-playlist --dump-single-json --skip-download --ignore-errors 'https://www.youtube.com/@Capitology/playlists' > playlists-flat.json
python -m yt_dlp --flat-playlist --dump-single-json --skip-download --ignore-errors 'https://www.youtube.com/playlist?list=PLxP1_pmCHjexukvwiRi8pdPS7q8JWOtEB' > macro-playlist-flat.json
python research/capitology-model/inventory_channel.py --source-dir /path/to/source-directory
```

On refresh, enumerate any additional public playlists, verify Streams again, regenerate the CSV and reconciliation notes, and retain any previously known IDs no longer exposed by current listings. The collector's optional `*-playlist-flat.json` inputs include playlist-only IDs. This helper is a metadata collector, not an ingestion or analysis workflow.
