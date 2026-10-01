# Pass 2 — caption corpus acquisition

Completed 2026-10-01 UTC. This pass acquired and normalized captions only. No gameplay interpretation or strategic claim extraction was performed.

## Coverage

| Measure | Result |
|---|---:|
| Inventory records | 54 |
| Caption tracks acquired | 54 |
| Failed or empty tracks | 0 |
| Timed segments | 27,388 |
| Approximate caption words | 181,979 |
| Raw JSON3 bytes | 18,588,375 |
| Language / source | English, YouTube automatic captions |

Each video has three durable representations:

- `captions/raw-json3-gz/<video_id>.en.json3.gz`: losslessly compressed, untouched caption response from yt-dlp/YouTube.
- `captions/segments/<video_id>.json`: normalized segments with start/end times, source checksum, and per-video metrics.
- `captions/text/<video_id>.md`: readable timestamped transcript for later research.

Acquisition logs are stored under `captions/logs/`. The machine-readable summary is `pass02_caption_manifest.json`; the CSV is a compact index.

## Validation

All 54 expected IDs appear exactly once in each of the raw, segment, text, and log directories. All segment files parse as JSON and match their inventory IDs. Every raw file matches the SHA-256 recorded in its segment record. Segment start times are monotonic; no segment ends before it starts; no segment starts beyond its video's declared duration by more than five seconds; no caption track is empty. Maximum leading gap is 4.720 seconds and maximum trailing gap is 3.680 seconds.

Word count ranges from 28 for a 22-second Short to 11,876 for the longest dense transcript; the median is 3,419. These values are acquisition diagnostics, not information-density judgments.

## Quality limits carried forward

All tracks are automatic speech recognition. Names, team names, hero names, acronyms, punctuation, speaker changes, and domain terms may be wrong. The normalized transcripts retain the caption wording rather than silently correcting it. Raw JSON3 remains the source of record. Later passes must quote or classify cautiously and use audio/video review for high-value ambiguous claims.

The readable version removes bracketed non-speech cues only from its word-count calculation; the timed segment JSON preserves every non-empty event. Automatic translation variants were not acquired as separate sources.

## Acquisition incident

The first local four-worker attempt acquired six tracks before YouTube returned HTTP 429. It was stopped. The first GitHub Actions attempt used the wrong yt-dlp cookie option and failed before contacting YouTube; this was diagnosed from its artifact logs. The corrected single-worker runner used the repository's configured YouTube cookies, acquired all 54 tracks, passed the workflow completeness checks, and produced artifact `capitology-pass2-captions-36934287709` (run `36934287709`).

## Next pass boundary

Pass 3 may use these transcripts to divide each upload into topic segments and estimate seriousness, strategic relevance, information density, transcript confidence, and the need for visual verification. Those judgments do not belong in this acquisition pass.
