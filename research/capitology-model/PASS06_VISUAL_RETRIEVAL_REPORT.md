# Pass 6 — selective visual retrieval

**Status: selection complete; footage retrieval blocked. No gameplay frame has been reviewed.** This is a reproducible retrieval queue, not visual evidence or an adjudication of the Pass 5 relationships.

## Selection

`pass06_retrieval_queue.csv` contains 23 bounded windows (52 minutes 52 seconds) from 12 videos, anchored to Pass 4 claims. Thirteen are priority A (first retrieval batch); ten are priority B. Every window includes a time link, the claim anchor, an evidence role, and a specific visual question. `pass06_retrieval_queue.py` rebuilds and checks the CSV from the Pass 4 ledger. The windows deliberately include a limiting case or counterexample for each of the six Pass 5 tensions. Priority denotes retrieval order, not credibility.

| Question | Earlier / framing windows | Later / limit or failure windows | What the images must settle |
|---|---|---|---|
| Turns and initiative | V6-01–02, 2023 early and soft turns | V6-03–04, 2026 bait and counterplay | Whether the same decision unit is used, which resources and routes create another turn, and whether the opponent retains a choice. |
| Retreat and space | V6-05, late forced retreat | V6-06–07, voluntary retreat and reset | Starting geometry, remaining cooldowns, distance given, and whether a useful later attack becomes possible. |
| Ultimate economy | V6-08–09, qualified thesis and kite | V6-10–11, secure retake and failed triple use | Ultimate count *and* fight result, objective state, charge recovery, and defensible setup after a flip. |
| Dive survival | V6-12–13, setup denial and route | V6-14–15, early defensive ult and scouting support | Threatened angles, attacker staging, information available to defenders, and timing of defensive resources. |
| Bait and second move | V6-16, passive kite failure; V6-17, accepted bait | V6-18–19, choice after a forced cooldown and clearing the attention holder | Whether the offer is credible, its cost, and whether either team has the resources to answer the next move. |
| Split cores | V6-20–21, 2023 push/pull and failure limit | V6-22–23, 2026 attention exchange and delayed split | Core distance, enemy commitment, timing of counterpressure, and whether two descriptions name the same mechanism. |

The queue is intentionally narrower than the 164 high-visual Pass 4 claims. It samples the open tensions rather than treating the largest claim cluster or the newest upload as representative of the full channel. Other role-specific and lower-priority examples remain available in `pass04_claims.jsonl` for a later expansion if these windows leave a concrete gap.

## Retrieval attempt and evidence boundary

On 2026-10-02, the YouTube watch page and format metadata loaded for `Hl-nV1aF1yE` (“Back Up to Go Forward”). Seeking to 03:05 showed captions, but the player displayed a black loading screen; play did not produce a gameplay frame. A `yt-dlp` / `ffmpeg` section download of 03:05–05:10 failed with “Invalid data found when processing input.” Direct range requests for the available video format and storyboard formats returned `text/html`, not video or image bytes. A storyboard request for a second video, `c92ESPjlveI`, also returned `text/html`. These checks establish an access failure in this environment, not a claim that the source videos lack footage.

All 23 CSV rows therefore remain `queued_not_retrieved` and `not_reviewed`; only the two named source videos were directly tested. In particular, no sight line, cooldown, player position, map distance, outcome, or spoken player attribution has been confirmed from footage. The caption-based claims remain provisional. No frame sheets, clips, or visual annotations were produced.

## Resume procedure

1. Obtain playable video files or an environment that returns actual media bytes for these URLs. Start with the thirteen priority A windows, then retrieve the ten B windows before deciding whether the paired tensions hold. Retain source video ID and original timecode with each clip; do not silently replace a missing window with a nearby clip.
2. For each window, inspect before and after the spoken anchor. Log map and objective, both teams' positions and visible information, cooldown/ultimate state where legible, decisive move, outcome, and any uncertainty. A commentator's account of off-screen knowledge cannot be verified from a single visible POV.
3. Record file path or frame/time evidence and update `retrieval_status` only when actual media bytes are present. Keep `visual_review_status` separate until the frames have been inspected. If one side of a pair fails retrieval, leave the tension open.
4. Pass 7 can perform the deeper replay analysis from retrieved footage. Pass 8 should adjudicate apparent contradictions and temporal changes using those observations alongside the dated captions. Do not update `model.md` as though this blocked retrieval verified gameplay.
