# Pass 4 — strategic claim extraction (in progress)

Started 2026-10-02 UTC. This is a manually reviewed, transcript-grounded first tranche. It does **not** finish Pass 4 or establish that the gameplay examples are correct.

## Progress

| Measure | Current state |
|---|---:|
| Known uploads | 54 |
| Uploads sampled for claims | 16 |
| Uploads not yet sampled | 38 |
| Provisional atomic claims | 42 |
| Years represented | 2023: 8 claims; 2024: 7; 2025: 10; 2026: 17 |
| Video frames reviewed | 0 |

The 16 sampled uploads were **not** reviewed exhaustively. Their remaining transcript windows and all 38 unreviewed uploads are still in the queue. This is intentionally a broad first sample across early definitions, role examples, pro reviews, a later clarification, and the most recent learning essay. It is not a frequency estimate of the whole corpus.

## Files

- `pass04_claims.jsonl`: one paraphrased claim per row, with video, upload date, timestamp range, time-link, topic, claim class, scope, transcript confidence, visual dependency, and review note.
- `pass04_claims.csv`: same data for filtering.
- `pass04_claims_seed.py`: transparent manually curated source and export script. This script does not invent claims from a keyword classifier.
- `pass04_coverage_queue.csv`: all 54 uploads and their current Pass 4 coverage. A sampled video remains marked `sampled_not_exhaustive`.

## Extraction rules

1. Read the normalized timed automatic captions in `captions/segments/<video_id>.json`, with Pass 3 sections used for navigation, not as claim evidence.
2. Paraphrase a single testable or definitional idea; retain the speaker's stated condition and the upload date. Record the exact transcript interval and a time-linked video URL. Do not copy extended caption text into the ledger.
3. Separate definitions, conditional rules, mechanisms, case judgments, counterexamples, and methodological advice. A narrator's evaluation of a professional match remains **his interpretation**, not an independently verified result.
4. Mark geometry, player gaze, cooldown state, and fight outcomes for later visual review. Automatic captions alone cannot prove those details and can mangle hero or player names.
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

These relationships are navigation notes, not the final `model.md` synthesis. No claim has been promoted into that scaffold.

## Next Pass 4 work

1. Work through all 38 currently unreviewed uploads, then finish unsampled windows in the initial 16. Use `pass04_coverage_queue.csv` to keep the denominator visible.
2. Expand especially the underrepresented role, composition matchup, pro team, and game design material. Review the 2024–2025 intervening uploads before making temporal evolution claims.
3. For every new claim, include a timestamp interval and condition; separate guest speech and quoted material from Capitology's own endorsement.
4. Audit the ledger against the caption events and make a second read of ambiguous ASR. Only after transcript coverage is complete should Pass 4 be called complete.
5. Passes 6–7 should resolve high visual dependency. Pass 8 should decide which alleged tensions actually contradict one another.
