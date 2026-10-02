# Pass 4 — transcript-grounded strategic claim extraction

Started 2026-10-02 UTC. The manually reviewed transcript sweep now includes a complete caption read of every Pass 3 section in all 54 known uploads. This closes the transcript coverage portion of Pass 4. All claims remain provisional until the gameplay and ambiguous audio are checked in later passes.

## Progress

| Measure | Current state |
|---|---:|
| Known uploads | 54 |
| Uploads with transcript-grounded claims | 51 |
| Uploads reviewed without a stable model claim | 3 |
| Provisional atomic claims | 206 |
| Years represented | 2023: 16 claims; 2024: 46; 2025: 99; 2026: 45 |
| Pass 3 sections with a full Pass 4 caption read | 292 of 292 |
| Additional sections with sampled claim windows only | 0 of 292 |
| Sections without a Pass 4 read yet | 0 of 292 |
| Video frames reviewed | 0 |
| Claims requiring high visual review | 164 |
| Claims with low transcript confidence | 4 |

All 54 known uploads were read section by section. The two short reaction clips have too little caption context for a stable tactical claim; the announcement concerns the channel's content plans. The 206 claims select distinct propositions rather than count every repetition, so topic counts are not frequency estimates of the whole corpus. The speaker announced a 2026 shift toward more general public videos and a separate venue for some team-specific analysis; public channel coverage therefore cannot be treated as a uniform sample of his thinking over time (`UC8D2vBDf_0`, 00:00:04–00:05:12).

## Files

- `pass04_claims.jsonl`: one paraphrased claim per row, with video, upload date, timestamp range, time-link, topic, claim class, scope, transcript confidence, visual dependency, and review note.
- `pass04_claims.csv`: same data for filtering.
- `pass04_claims_seed.py`: transparent manually curated source and export script. This script does not invent claims from a keyword classifier.
- `pass04_coverage_queue.csv`: all 54 uploads and their transcript coverage. The 51 claim-bearing videos are marked `full_transcript_reviewed_footage_pending`; the three other rows explain why no model claim was extracted.
- `pass04_section_audit.csv`: all 292 Pass 3 sections marked as complete caption reads. `pass04_section_audit.py` rebuilds this queue from the manual full-read list and claim ledger.

## Extraction rules

1. Read the normalized timed automatic captions in `captions/segments/<video_id>.json`, with Pass 3 sections used for navigation, not as claim evidence.
2. Paraphrase a single testable or definitional idea; retain the speaker's stated condition and the upload date. Record the exact transcript interval and a time-linked video URL. Do not copy extended caption text into the ledger.
3. Separate definitions, conditional rules, mechanisms, case judgments, counterexamples, and methodological advice. A narrator's evaluation of a professional match remains **his interpretation**, not an independently verified result.
4. Mark geometry, player gaze, cooldown state, and fight outcomes for later visual review. Automatic captions alone cannot prove those details and can mangle hero or player names. The transcripts for `nddeTxFzT6Q` and `N5fHwbNE-SQ` are noticeably garbled; claims based on them need audio checks.
5. Keep apparent tensions as questions for Pass 8. Do not silently turn rhetorical titles into universal rules.

Every ledger row is `provisional`, has `gameplay_verified: false`, and states the evidence type as automatic-caption speaker paraphrase. `transcript_confidence` is a local qualitative judgment of whether the spoken idea was recoverable in the sampled interval; it is not a word-level ASR accuracy measure. `visual_dependency` is the amount of video confirmation needed to assess the claim's example, not an evidence score.

## Early relationships to preserve, without synthesizing the model yet

| Relationship | Evidence | Current reading | Later check |
|---|---|---|---|
| First/second/neutral turns | P4-005–008; P4-014; P4-033–035; P4-100; P4-109; P4-118; P4-206 | The early definitions are compatible with the later warning that these timing labels alone do not tell a team how to play. Later examples include cooldown-first moves, repeated turns, and stacking advantages before committing. | Inspect both match POVs. |
| Corner discipline and voluntary retreat | P4-009–011; P4-021; P4-030–032; P4-039 | The speaker explicitly distinguishes giving space early, with resources and future options, from being forced off after the opponent reaches the corner. He raises the apparent conflict with “Lock Eyes and Fight” himself. | Visually check distances, timing, and when fighting the setup is preferable. |
| Ultimate economy | P4-026–029; P4-036–038; P4-117–121; P4-128; P4-134 | “Does Not Matter” is a provocative title. The spoken thesis says it still matters, especially for named composition families; 2024 matchups and proactive defensive ult use show specific situations where ultimate timing is central. This is a scoped relationship, not a settled contradiction. | Inspect the cited fights, ult charge, and patch contexts. Search other videos for genuine counterexamples. |
| Dive survivability | P4-016–018; P4-134–139 | “Cannot live a good dive” is conditional on the dive already being well staged; the actionable claim is to disrupt staging first, sometimes with a proactive ultimate. The low-damage dive review distinguishes soft probes from hard commitment. | Test the boundary with counterexamples and replay POV. |
| Learning method | P4-022–023; P4-040–042 | The advice emphasizes causal reconstruction of what players saw and did, with written observation and matched comparisons. | Sample the coaching archive for earlier or competing advice. |
| Split cores and later aggro balance | P4-001–004; P4-091 | The 2026 discussion resembles the 2023 split-core push/pull account, but it uses a different composition and repeated attention shifts. | Determine which parts generalize and which are hero- or patch-specific. |
| Mechanics, attention, and planning | P4-012–013; P4-022–023; P4-078–079; P4-096–098 | His explanations include aim, mechanical execution, attention allocation, and deliberate practice alongside strategic setup. | Avoid a model that explains every failed fight through positioning alone. |

These relationships are navigation notes, not the final `model.md` synthesis. No claim has been promoted into that scaffold.

## Handoff to later passes

1. The transcript audit confirms 292 unique sections have a full-read status; all 206 IDs are unique and all claim intervals contain timed caption events. This verifies indexing, not the meaning or correctness of a gameplay example.
2. Pass 5 can cluster these provisional claims while preserving their conditions, source dates, counterexamples, and speaker attribution. Do not promote them into `model.md` yet.
3. Passes 6–7 should check the 164 high-visual-dependency claims against footage and revisit ambiguous ASR, especially `nddeTxFzT6Q` and `N5fHwbNE-SQ`. Pass 8 should decide which alleged tensions actually contradict one another.
