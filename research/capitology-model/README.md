# Capitology Overwatch Model Project

Status: Pass 2 completed on 2026-10-01: full advertised English automatic-caption corpus acquired and normalized.

Goal: reconstruct Ethan "Capitology" Walker's model of Overwatch from his YouTube corpus, while preserving evidence, contradictions, evolution over time, and the distinction between serious analysis and entertainment.

## Pass 1 inventory

- `pass01_public_index.json`: authoritative structured inventory and coverage notes.
- `pass01_public_index.csv`: spreadsheet-friendly metadata export, including full descriptions.
- `pass01_public_index.preliminary.json`: preserved original preliminary inventory.
- `inventory-evidence/`: per-video metadata evidence and compact channel/playlist enumeration responses.
- `PASS01_INVENTORY_REPORT.md`: collection methodology, reconciliation, and limitations.
- `inventory_channel.py`: metadata-only collection helper.
- `pass02_caption_manifest.json` / `.csv`: caption coverage and quality metrics.
- `captions/raw-json3-gz/`: losslessly compressed original timed automatic-caption responses.
- `captions/segments/`: normalized, timestamped JSON transcripts.
- `captions/text/`: readable timestamped transcripts.
- `PASS02_CAPTION_REPORT.md`: acquisition, validation, and quality notes.
- `acquire_captions.py`: repeatable caption-only collector and normalizer.

54 unique uploads are known: 53 public (48 Videos + 5 Shorts) and one unlisted upload discovered through the public Overwatch Macro playlist. The date range is 2023-10-27 through 2026-09-29, with 14 hours 33 minutes 33 seconds of total runtime. All 54 have titles, upload dates, durations, URLs, descriptions, and advertised English automatic caption tracks. Empty descriptions are preserved as empty strings. No known record has an unresolved metadata gap.

No known entry is confirmed private or deleted. This does not establish that the channel has never had hidden/private/deleted uploads: public interfaces cannot enumerate those exhaustively. The preliminary two known IDs are retained. Three earlier indirect references remain unresolved as references, and are not fabricated into new video rows.

## Pass sequence

1. Channel inventory and metadata — complete within the stated public-discovery scope
2. Caption acquisition and normalization — complete (audio acquisition was unnecessary for this pass)
3. Transcript segmentation and seriousness/information-density scoring
4. Strategic claim extraction
5. Concept clustering
6. Selective visual retrieval
7. Deep visual analysis of high-information/ambiguous segments
8. Contradiction and evolution pass
9. Model synthesis

Next pass: transcript segmentation and seriousness/information-density scoring. No gameplay analysis or strategic claim extraction has begun.
