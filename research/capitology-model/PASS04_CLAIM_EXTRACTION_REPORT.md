# Pass 4 — strategic claim extraction (in progress)

Started 2026-10-02 UTC. This is a manually reviewed, transcript-grounded **initial sweep of all known uploads**. It does **not** finish Pass 4 or establish that the gameplay examples are correct.

## Progress

| Measure | Current state |
|---|---:|
| Known uploads | 54 |
| Uploads sampled for claims | 51 |
| Uploads reviewed without a stable model claim | 3 |
| Provisional atomic claims | 99 |
| Years represented | 2023: 8 claims; 2024: 22; 2025: 40; 2026: 29 |
| Video frames reviewed | 0 |
| Claims requiring high visual review | 69 |
| Claims with low transcript confidence | 3 |

The 51 claim-bearing uploads were **not** reviewed exhaustively. Their remaining transcript windows are still in the queue. The two short reaction clips have too little caption context for a stable tactical claim; the announcement concerns the channel's content plans. This is a broad sample across early definitions, role examples, composition and draft discussion, pro reviews, later clarifications, and learning advice. It is not a frequency estimate of the whole corpus. The speaker announced a 2026 shift toward more general public videos and a separate venue for some team-specific analysis; public channel coverage therefore cannot be treated as a uniform sample of his thinking over time (`UC8D2vBDf_0`, 00:00:04–00:02:21).

## Files

- `pass04_claims.jsonl`: one paraphrased claim per row, with video, upload date, timestamp range, time-link, topic, claim class, scope, transcript confidence, visual dependency, and review note.
- `pass04_claims.csv`: same data for filtering.
- `pass04_claims_seed.py`: transparent manually curated source and export script. This script does not invent claims from a keyword classifier.
- `pass04_coverage_queue.csv`: all 54 uploads and their current Pass 4 coverage. A claim-bearing video remains marked `sampled_not_exhaustive`; the three other rows explain why no model claim was extracted.

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
| First/second/neutral turns | P4-005–008; P4-014; P4-033–035 | The early definitions are compatible with the later warning that these timing labels alone do not tell a team how to play. The 2026 example adds deliberate bait and its counterplay. | Read remaining uses across the corpus; inspect both match POVs. |
| Corner discipline and voluntary retreat | P4-009–011; P4-021; P4-030–032; P4-039 | The speaker explicitly distinguishes giving space early, with resources and future options, from being forced off after the opponent reaches the corner. He raises the apparent conflict with “Lock Eyes and Fight” himself. | Visually check distances, timing, and when fighting the setup is preferable. |
| Ultimate economy | P4-026–029; P4-036–038 | “Does Not Matter” is a provocative title. The spoken thesis says it still matters, especially for named composition families; a later match review maintains this qualification and faults lost fights and poor setup. | Inspect the cited fights, ult charge, and 2026 patch context. Search other videos for genuine counterexamples. |
| Dive survivability | P4-016–018 | “Cannot live a good dive” is conditional on the dive already being well staged; the actionable claim is to disrupt staging first. | Test the boundary with counterexamples and replay POV. |
| Learning method | P4-022–023; P4-040–042 | The advice emphasizes causal reconstruction of what players saw and did, with written observation and matched comparisons. | Sample the coaching archive for earlier or competing advice. |
| Split cores and later aggro balance | P4-001–004; P4-091 | The 2026 discussion resembles the 2023 split-core push/pull account, but it uses a different composition and repeated attention shifts. | Determine which parts generalize and which are hero- or patch-specific. |
| Mechanics, attention, and planning | P4-012–013; P4-022–023; P4-078–079; P4-096–098 | His explanations include aim, mechanical execution, attention allocation, and deliberate practice alongside strategic setup. | Avoid a model that explains every failed fight through positioning alone. |

These relationships are navigation notes, not the final `model.md` synthesis. No claim has been promoted into that scaffold.

## Next Pass 4 work

1. Finish the unsampled transcript windows in the 51 claim-bearing videos, prioritizing long videos such as `GIY_4hD9_M8` and mixed watch-party material. Use `pass04_coverage_queue.csv` to keep the denominator visible. The initial sweep covered every upload, not every section.
2. Expand underrepresented exceptions, failed examples, role and composition matchups, and deliberate counterexamples. Revisit the 2024–2025 intervening uploads before making temporal evolution claims.
3. For every new claim, include a timestamp interval and condition; separate guest speech and quoted material from Capitology's own endorsement.
4. Audit the ledger against the caption events and make a second read of ambiguous ASR. Only after transcript coverage is complete should Pass 4 be called complete.
5. Passes 6–7 should resolve high visual dependency. Pass 8 should decide which alleged tensions actually contradict one another.
