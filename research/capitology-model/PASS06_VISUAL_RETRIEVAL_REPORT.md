# Pass 6 — selective visual retrieval

**Status: selection complete; a direct visual retrieval route is verified on one video. The 23-window review remains open.** This is a reproducible retrieval queue, not an adjudication of the Pass 5 relationships.

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

On 2026-10-02, the YouTube watch page and format metadata loaded for `Hl-nV1aF1yE` (“Back Up to Go Forward”). Seeking to 03:05 showed captions, but the browser player displayed a black loading screen; play did not produce a gameplay frame. A direct shell `yt-dlp` / `ffmpeg` section download failed with “Invalid data found when processing input.” Direct range requests for the video format and storyboard formats returned a `Site Unavailable` HTML response instead of media bytes. A storyboard request for a second video, `c92ESPjlveI`, also returned HTML. The cloud browser embed showed error 153. These failures are specific to the cloud media path.

The small GitHub-hosted runner probe also failed to obtain video formats. The existing self-hosted Windows runner succeeded after its Node runtime and `yt-dlp` challenge solver were enabled: [run 37001603925](https://github.com/notethanwalker/youtube-observation/actions/runs/37001603925) retrieved 17 storyboard sheets for `Hl-nV1aF1yE`. [Run 37001993628](https://github.com/notethanwalker/youtube-observation/actions/runs/37001993628) retrieved those sheets and a playable 480p, 727.767-second AV1 source (36,217,669 bytes). The source was transferred here and local FFmpeg cut a 15-second, 429,018-byte video for 03:05–03:20. FFprobe validated its duration; a frame at 03:09 visibly shows the Overwatch overhead review. The clip is saved as `Hl-nV1aF1yE-185-200.mp4`. The runner artifact expires after one day, but the sample clip was saved separately.

This proves a workable route for direct frame inspection without the full observation pack. The storyboard samples this video about once every five seconds at roughly 320×180 per tile, useful for navigation but insufficient for detailed HUD/cooldown checks. The full source supports exact local cuts and frame stepping. The 23 CSV rows remain `queued_not_retrieved` and `not_reviewed` because the full queued windows have not yet been extracted and inspected. No tactical claim, sight line, cooldown, outcome, or player attribution has been adjudicated from the 15-second proof sample.

## Resume procedure

1. Use `.github/workflows/capitology-pass6-home-probe.yml` with a bounded request in `requests/capitology-pass6-home-probe.json` on the existing Windows runner. It retrieves the storyboard and, when FFmpeg is absent there, a source video. Transfer the temporary artifact and use local FFmpeg to cut the exact windows. Start with the thirteen priority A windows, then retrieve the ten B windows before deciding whether the paired tensions hold. Retain source video ID and original timecode with each clip; do not silently replace a missing window with a nearby clip.
2. For each window, inspect before and after the spoken anchor. Log map and objective, both teams' positions and visible information, cooldown/ultimate state where legible, decisive move, outcome, and any uncertainty. A commentator's account of off-screen knowledge cannot be verified from a single visible POV.
3. Record file path or frame/time evidence and update `retrieval_status` only when actual media bytes are present. Keep `visual_review_status` separate until the frames have been inspected. If one side of a pair fails retrieval, leave the tension open.
4. Pass 7 can perform the deeper replay analysis from retrieved footage. Pass 8 should adjudicate apparent contradictions and temporal changes using those observations alongside the dated captions. Do not update `model.md` as though this blocked retrieval verified gameplay.
