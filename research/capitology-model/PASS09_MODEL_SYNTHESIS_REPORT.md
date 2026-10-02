# Pass 9 — provisional model synthesis

**Result:** `model.md` contains 24 conditional rules spanning all 16 Pass 5 clusters. `pass09_rules.json` is the machine-readable index for match review. It links 120 distinct Pass 4 claim anchors and references selected Pass 7 windows where relevant. `pass09_rules.py` is the curated source and renderer; it validates all claim IDs, visual IDs, and cluster IDs before writing both files.

## Synthesis choices

- The central structure is a **useful next response**: map pressure and resource exchanges shape an opponent's options, while a team retains a reply to what actually happens. This is a cross-theme candidate, not a measured universal principle.
- Every rule has a trigger, action, and failure boundary. This prevents title rhetoric such as “ultimate economy does not matter” from becoming unconditional advice.
- Role-specific duties, aim, attention, learning method, and design views remain distinct. The six Pass 7 visual themes cannot stand in for all 206 claims.
- `sampled_visual`, `illustrative_visual`, and `transcript_only` identify the evidence level. No rule is labeled experimentally validated; the general effectiveness of each is not established by this corpus.
- Source links and upload dates permit audit. Upload chronology is not a patch-controlled or recording-date study.

## Coverage and remaining uncertainty

| Measure | Result |
|---|---:|
| Conditional rules | 24 |
| Primary concept clusters represented | 16 / 16 |
| Distinct claim anchors linked | 120 / 206 |
| Selected visual windows referenced | 23 / 23 |
| General tactical effects independently measured | 0 |

The other 86 selected claims remain available in the Pass 4 ledger and concept index. This synthesis chooses nonredundant anchors, not a sample from which to infer topic frequency. Some rules rely only on captions. The OW1/OW2 ultimate-economy comparison is unmeasured, and ambiguous guest/ASR attribution must be checked in audio when decisive. In a new player's replay, the model must be applied **after** observing the actual fight; it cannot infer a mistake from the loss or force every moment into one of these rules.

## Product handoff

`MATCH_REVIEW_PROTOTYPE.md` defines the upload → analysis → replay-linked report. The rule index is ready to be retrieved by an analysis worker. A functioning player product still requires a private upload job, full-match broad pass, dense inspection of candidate windows, rule-grounded findings, and an internal end-to-end review before user upload testing. This report does not claim that those engineering steps are already complete.
