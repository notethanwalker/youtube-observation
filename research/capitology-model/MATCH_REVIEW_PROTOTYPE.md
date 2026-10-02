# Player-facing match review prototype

**Product target:** A player uploads an unedited Overwatch match recording and receives a useful, timecoded review in Capitology's analytical framework. A question box over the channel research is an optional follow-up tool, not the primary interface.

## Player flow

1. Open the review page on a phone or computer and upload a full match recording (initial target: MP4/MOV). Choose the player POV or spectator view; enter hero, role, team, and the player to review when those are not obvious. Optional: add one concern such as “I keep losing retakes.”
2. See upload and analysis progress. The recording remains private to the job; it does not enter this public GitHub repository.
3. Open a report with a replay timeline and clickable timestamps. The report identifies 3–6 high-impact decisions, explains the visible situation, the player's action, the opponent's observed response, a specific alternative, and what evidence supports the judgment.
4. Expand a finding to replay its surrounding clip and inspect the source rule from the Capitology model. The player can flag a wrong hero, mistaken POV, missed information, or an intentional choice for correction.

### Report contract

Each finding must include:

- recording time range and a playable clip or seek target;
- player, POV, map/objective and relevant team state when visible;
- **observed sequence** separated from the model's **interpretation**;
- why the decision mattered, the conditional alternative, and when that alternative would be wrong;
- model rule IDs and linked Capitology video timestamps;
- confidence and a short statement of what the POV, edit, or resolution cannot establish.

The summary should prioritize recurring decision patterns and two practical next-match cues. Include good decisions, not only errors. Do not grade a fight solely by whether it was won. A single POV cannot prove enemy information or a teammate's cooldown unless visible or otherwise independently supported. Do not invent an exact ability order from sampled frames.

## Minimum viable pipeline

| Stage | Input → output | Prototype acceptance check |
|---|---|---|
| Private upload | Full recording → job ID and source checksum | A player can submit a real full match from a phone or desktop and resume/open its job; raw footage is never committed to GitHub. |
| Media preparation | Recording → duration, audio track, broad frames, fight windows and seekable clips | All derived timestamps map back to the original recording, including after pauses, menus, or cuts. |
| Broad match pass | Sampled footage → candidate fight/decision timeline | The pass covers the entire recording and flags POV changes, menus, unclear segments, and likely decisive windows. Sparse frames are for navigation only. |
| Dense review | Candidate windows → observed actions and uncertainty | Review contiguous motion and relevant audio around selected moments; verify player identity, objective, kill feed and visible resource state before attribution. |
| Model application | Observations + Pass 9 model/evidence index → coaching findings | Findings cite specific rules and source time links, retain conditions/counterexamples, and distinguish observed fact from an inference. |
| Delivery | Findings + clips → mobile-friendly report | A player can tap each finding and inspect the corresponding moment, then download/share a report without exposing the raw upload. |

The first automation should favor a small number of defensible decisions over a confident-sounding commentary on every fight. It may return “unresolved” for a key detail. If the player supplies a short clip rather than a full match, label the result a clip review and do not infer earlier resource cycles.

## Current components and gaps

The repository has `scripts/process_file.py` for FFmpeg-based extraction from a local file, YouTube/Drive ingestion workflows, 206 timestamped provisional channel claims, 16 concept clusters, 23 selectively reviewed examples, and Pass 8 contradiction notes. These are research and media-preparation components; **Pass 9 now has a provisional rule index and the upload application can return a sampled-frame report.** The automated coaching quality is unvalidated until live API and full match review.

The build order is:

1. **Pass 9:** Convert the research into a compact, conditional rule index with rule IDs, evidence URLs, exceptions, and confidence. Keep coaching method and role-specific advice alongside the six visually sampled macro themes.
2. **End-to-end pilot:** Use one full unedited match recording, identify the target player, process it with the existing local-file pipeline, perform a broad pass plus dense review, and produce the report contract above. Measure timestamp accuracy and compare every major finding against the recording. This can be analyst-assisted before model automation is trusted.
3. **Player upload and automated job:** Add private storage, an upload page, background processing, a visual/audio analysis worker, model retrieval, and a report viewer. Reuse the validated pilot output schema. Avoid sending full-resolution videos through GitHub issues or public Actions artifacts.
4. **Acceptance:** Repeat on at least two materially different full matches/POVs; have a knowledgeable reviewer challenge identity, timestamps, ability claims, and proposed alternatives. Correct failures before calling the prototype functional for players.

**Initial input assumption:** “Upload a replay” means an exported screen recording/video file. An Overwatch in-client replay code needs a running game client and capture/controller automation to turn the code into video and selectable POVs; that is a separate input adapter. The report schema and analysis rules should be the same after capture.

## Definition of functional

The player supplies a real recording and receives a completed, replay-linked analysis without having to ask strategic questions or manually assemble frames. A model document alone, an extracted contact sheet alone, and a generic ungrounded recap do not meet this definition.

## Build status (2026-10-02)

The first upload-to-report implementation is in `match_review/`; setup, security scope, and validation limits are in `PROTOTYPE_SETUP.md`. It uses sampled stills at 10 and 2.5 second intervals. The initial product contract above calls for contiguous motion and audio; those richer inputs remain a follow-on capability. The UI reports this limitation, and the app must not claim to have examined unsampled motion or audio. Internal transport tests use a fake model and are not player-match acceptance evidence.
