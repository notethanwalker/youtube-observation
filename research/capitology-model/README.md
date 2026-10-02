# Capitology Overwatch Model Project

Status: Pass 4 completed a full caption read of 292 sections and recorded 206 provisional claims from 51 of 54 uploads; two Shorts and an announcement yielded no stable model claim. Pass 5 clusters all claims into 16 provisional primary concepts. Pass 6 retrieved and verified 23 selected visual windows from 12 videos. Pass 7 completed a bounded visual review of all 23 and closer sequence review of seven; the edited footage supports selected mechanisms while leaving exact and corpus-wide claims open.

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
- `pass03_segments.jsonl` / `.csv`: 292 timestamped research sections with topic, mode, and triage scores.
- `pass03_video_index.json`: per-video aggregates and Pass 3 audit state.
- `pass03_review_queue.csv`: A–D queue for claim extraction and later visual review.
- `pass03-outlines/`: readable section map for all 54 uploads.
- `PASS03_SEGMENTATION_REPORT.md`: method, distributions, calibration, and limitations.
- `segment_transcripts.py`: deterministic segmentation and scoring implementation.
- `pass04_claims.jsonl` / `.csv`: provisional timestamped strategic claims, with scope, evidence type, and visual dependency.
- `pass04_claims_seed.py`: manually curated claim export, reproducible as structured files.
- `pass04_coverage_queue.csv`: complete 54-video transcript coverage queue; claim-bearing videos need footage review.
- `pass04_section_audit.csv` / `pass04_section_audit.py`: section-level review queue and its reproducible status export.
- `PASS04_CLAIM_EXTRACTION_REPORT.md`: extraction rules, current coverage, candidate relationships, and remaining work.
- `pass05_concept_index.csv`: claim-by-claim primary and secondary concepts, retaining source date, link, scope, and visual dependency.
- `pass05_cluster_registry.json`: 16 cluster definitions with primary claim IDs, year and video coverage, and visual-review counts.
- `pass05_relationships.csv`: 12 provisional relationships between concepts and their claim-level evidence.
- `pass05_clusters_seed.py`: manual, validated cluster assignments and reproducible exports.
- `PASS05_CONCEPT_CLUSTERING_REPORT.md`: concept map, qualifications, candidate tensions, and visual-review handoff.
- `pass06_retrieval_queue.csv` / `pass06_retrieval_queue.py`: 23 bounded video windows, paired across six open questions, with time links and checks.
- `pass06_retrieval_registry.json` / `pass06_finalize_retrieval.py`: verified clip hashes, source runs, archive mapping, and repeatable package validation.
- `PASS06_VISUAL_RETRIEVAL_REPORT.md`: selection, capture route, archive checksums, and retrieval boundary.
- `pass07_visual_ledger.jsonl` / `PASS07_VISUAL_ANALYSIS_REPORT.md`: window-level visible evidence, caption interpretations, six paired findings, and limits.
- `pass07_contact_sheets.py`: repeatable timestamped visual triage from the retrieved clips.

54 unique uploads are known: 53 public (48 Videos + 5 Shorts) and one unlisted upload discovered through the public Overwatch Macro playlist. The date range is 2023-10-27 through 2026-09-29, with 14 hours 33 minutes 33 seconds of total runtime. All 54 have titles, upload dates, durations, URLs, descriptions, and advertised English automatic caption tracks. Empty descriptions are preserved as empty strings. No known record has an unresolved metadata gap.

No known entry is confirmed private or deleted. This does not establish that the channel has never had hidden/private/deleted uploads: public interfaces cannot enumerate those exhaustively. The preliminary two known IDs are retained. Three earlier indirect references remain unresolved as references, and are not fabricated into new video rows.

## Pass sequence

1. Channel inventory and metadata — complete within the stated public-discovery scope
2. Caption acquisition and normalization — complete (audio acquisition was unnecessary for this pass)
3. Transcript segmentation and seriousness/information-density scoring — complete
4. Strategic claim extraction — transcript sweep complete; claims provisional
5. Concept clustering — provisional transcript-based map complete
6. Selective visual retrieval — complete; 23 of 23 windows retrieved
7. Selective visual analysis of high-information/ambiguous segments — 23 reviewed at sampled intervals, seven examined more closely; unresolved facts retained
8. Contradiction and evolution pass
9. Model synthesis

Next step: Pass 8 contradiction and evolution adjudication using the visual ledger and dated claims. The 16 transcript clusters have selected visual examples and explicit limits, not comprehensive match validation. `model.md` remains a synthesis scaffold until contradiction review. The retrieval registry records clip provenance; the Pass 7 ledger and generated queue record visual review status.
