# Pass 6 — selective visual retrieval

**Status: selective retrieval complete; 23 of 23 windows have playable, verified clips.** This is the Pass 6 retrieval record. The subsequent bounded visual review and remaining uncertainties are in `PASS07_VISUAL_ANALYSIS_REPORT.md`.

## Selection

`pass06_retrieval_queue.csv` contains 23 bounded windows (52 minutes 26 seconds) from 12 videos, anchored to Pass 4 claims. Thirteen are priority A (first retrieval batch); ten are priority B. Every window includes a time link, the claim anchor, an evidence role, and a specific visual question. `pass06_retrieval_queue.py` rebuilds and checks the CSV against the Pass 4 ledger and inventory durations. The windows deliberately include a limiting case or counterexample for each of the six Pass 5 tensions. Priority denotes retrieval order, not credibility.

| Question | Earlier / framing windows | Later / limit or failure windows | What the images must settle |
|---|---|---|---|
| Turns and initiative | V6-01–02, 2023 early and soft turns | V6-03–04, 2026 bait and counterplay | Whether the same decision unit is used, which resources and routes create another turn, and whether the opponent retains a choice. |
| Retreat and space | V6-05, late forced retreat | V6-06–07, voluntary retreat and reset | Starting geometry, remaining cooldowns, distance given, and whether a useful later attack becomes possible. |
| Ultimate economy | V6-08–09, qualified thesis and kite | V6-10–11, secure retake and failed triple use | Ultimate count *and* fight result, objective state, charge recovery, and defensible setup after a flip. |
| Dive survival | V6-12–13, setup denial and route | V6-14–15, early defensive ult and scouting support | Threatened angles, attacker staging, information available to defenders, and timing of defensive resources. |
| Bait and second move | V6-16, passive kite failure; V6-17, accepted bait | V6-18–19, choice after a forced cooldown and clearing the attention holder | Whether the offer is credible, its cost, and whether either team has the resources to answer the next move. |
| Split cores | V6-20–21, 2023 push/pull and failure limit | V6-22–23, 2026 attention exchange and delayed split | Core distance, enemy commitment, timing of counterpressure, and whether two descriptions name the same mechanism. |

The queue is intentionally narrower than the 164 high-visual Pass 4 claims. It samples the open tensions rather than treating the largest claim cluster or the newest upload as representative of the full channel. Other role-specific and lower-priority examples remain available in `pass04_claims.jsonl` for a later expansion if these windows leave a concrete gap.

## Retrieval and evidence boundary

On 2026-10-02, the YouTube watch page and format metadata loaded for `Hl-nV1aF1yE` (“Back Up to Go Forward”). Seeking to 03:05 showed captions, but the browser player displayed a black loading screen; play did not produce a gameplay frame. A direct shell `yt-dlp` / `ffmpeg` section download failed with “Invalid data found when processing input.” Direct range requests for the video format and storyboard formats returned a `Site Unavailable` HTML response instead of media bytes. A storyboard request for a second video, `c92ESPjlveI`, also returned HTML. The cloud browser embed showed error 153. These failures are specific to the cloud media path.

The small GitHub-hosted runner probe also failed to obtain video formats. The existing self-hosted Windows runner succeeded after its Node runtime and `yt-dlp` challenge solver were enabled: [run 37001603925](https://github.com/notethanwalker/youtube-observation/actions/runs/37001603925) retrieved 17 storyboard sheets for `Hl-nV1aF1yE`. [Run 37001993628](https://github.com/notethanwalker/youtube-observation/actions/runs/37001993628) retrieved those sheets and a playable 480p, 727.767-second AV1 source (36,217,669 bytes). The source was transferred here and local FFmpeg cut a 15-second, 429,018-byte video for 03:05–03:20. FFprobe validated its duration; a frame at 03:09 visibly shows the Overwatch overhead review. The clip is saved as `Hl-nV1aF1yE-185-200.mp4`. The runner artifact expires after one day, but the sample clip was saved separately.

The storyboard samples this video about once every five seconds at roughly 320×180 per tile, useful for navigation but insufficient for detailed HUD/cooldown checks. The full source supports exact local cuts and frame stepping.

The subsequent `.github/workflows/capitology-pass6-batch.yml` retrieved the selected footage in four bounded batches on the existing Windows runner. It downloaded each source once per batch, cut the queued windows into silent H.264 clips at no more than 480p, extracted start/middle/end check frames, and removed full source files from the runner. The local proof and four batches yielded all 23 clips across 12 videos. The consolidated `pass06_retrieval_registry.json` records archive, original time range, clip SHA-256, frames, and source run for each window. `pass06_finalize_retrieval.py` verified source-manifest hashes, nonempty frames, clip durations, and exact corrected queue boundaries before packaging. At Pass 6 closure, all rows said `retrieved_video_only` and `not_reviewed`; the current queue incorporates Pass 7's separate sampled review statuses.

| Archive | Windows | Source | Archive SHA-256 |
|---|---:|---|---|
| `Capitology_Pass6_clips_part1.zip` | 5 | local proof; [run 37003705370](https://github.com/notethanwalker/youtube-observation/actions/runs/37003705370) | `c73ea124cde2872cc76450ed5e200ccea888cf4da329a310ff0a483ff2c1e779` |
| `Capitology_Pass6_clips_part2.zip` | 8 | [run 37004151152](https://github.com/notethanwalker/youtube-observation/actions/runs/37004151152) | `30e867146866891c93be5b3e8d11b43c51e1fdb5735e5327041f2d148be31428` |
| `Capitology_Pass6_clips_part3.zip` | 8 | [run 37004457970](https://github.com/notethanwalker/youtube-observation/actions/runs/37004457970) | `fd955fc9cae9a8596a2ae904df29e812f10ff555c40dba50c75a3b077934428b` |
| `Capitology_Pass6_clips_part4.zip` | 2 | [run 37004518270](https://github.com/notethanwalker/youtube-observation/actions/runs/37004518270) | `40477aaeb744780f455db0dab5df4d0b24959e1ea9c3f5233c1c56deb9cd55b9` |

The original queue extended V6-11 and V6-14 beyond the source durations by 11 and 10 seconds. Those runs reported a missing final check frame although they captured video up to its end. The corrected boundaries are 11:52–14:29 and 12:31–15:27. Both clips were trimmed from captured source-end clips and have new start/middle/end frames. The generator now asserts every selected end time is inside the Pass 1 inventory duration.

The check frames establish that video bytes and image frames are available. They do not establish gameplay facts. No tactical claim, sight line, cooldown, outcome, or player attribution has been adjudicated from these clips. The clips have no audio, so Pass 7 must pair them with timed caption segments for spoken context.

## Pass 7 handoff

1. Inspect each archived clip before and after the spoken anchor, pairing it with the timed caption transcript. Log map and objective, both teams' positions and visible information, cooldown/ultimate state where legible, decisive move, outcome, and uncertainty. A commentator's account of off-screen knowledge cannot be verified from a single visible POV.
2. Record the clip and exact source timestamp for each visual observation. Change `visual_review_status` only after footage review, and retain uncertainty when the HUD or viewpoint cannot show the relevant fact.
3. Pass 8 should adjudicate apparent contradictions and temporal changes using those observations alongside the dated captions. Do not update `model.md` as though retrieval itself verified gameplay.
