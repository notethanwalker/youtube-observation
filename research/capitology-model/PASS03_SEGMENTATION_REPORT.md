# Pass 3 — transcript segmentation and research triage

Completed 2026-10-01 UTC. This pass classifies transcript sections for later research. It does not extract strategic claims, decide whether the analysis is correct, or analyze gameplay.

## Corpus result

| Measure | Result |
|---|---:|
| Videos covered | 54 / 54 |
| Transcript sections | 292 |
| Median section duration | 183.2 seconds |
| Longest section | 264.7 seconds |
| Tier A review candidates | 38 |
| Tier B candidates | 166 |
| Tier C candidates | 82 |
| Tier D / low model priority | 6 |

All 54 videos are represented. There are 292 unique, time-ordered transcript sections that partition the source caption events. YouTube's ASR display intervals can overlap a boundary by a few seconds even though no caption event is duplicated between sections. The only sections shorter than 70 seconds are the five Shorts.

## Outputs

- `pass03_segments.jsonl`: complete structured section inventory, including scoring features and excerpts.
- `pass03_segments.csv`: spreadsheet-friendly section inventory.
- `pass03_video_index.json`: per-video weighted averages, topic distributions, modes, and audit record.
- `pass03_review_queue.csv`: A–D queue for later claim extraction and selective visual review.
- `pass03-outlines/<video_id>.md`: readable section outline for every upload.
- `segment_transcripts.py`: deterministic segmentation and scoring implementation.

## What each score means

All scores range from 0–100 and are intended for ranking within this corpus. They are not calibrated probabilities or judgments of whether a video is good.

- **Seriousness:** explanatory/analytical speech relative to banter, promotion, and filler.
- **Information density:** domain concepts, causal language, specificity, and explanatory markers per unit of transcript.
- **Strategic relevance:** likely usefulness for reconstructing Capitology's Overwatch model, based on broad topic and vocabulary.
- **Transcript confidence:** structural ASR confidence proxy based on speech rate, fragments, repetition, and track completeness. It cannot detect every misheard proper noun or game term.
- **Visual-review priority:** strategic relevance and information density plus visual/deictic language and transcript uncertainty. It predicts where seeing the screen is likely to matter.

## Topic and mode distribution

Primary topics:

| Topic | Sections |
|---|---:|
| `coaching_learning` | 15 |
| `player_decisions_mechanics` | 33 |
| `macro_space_tempo` | 112 |
| `fight_execution_review` | 79 |
| `mixed_other` | 1 |
| `composition_matchups` | 32 |
| `pro_team_analysis` | 8 |
| `game_design_meta` | 7 |
| `career_community_personal` | 5 |

Content modes:

| Mode | Sections |
|---|---:|
| `mixed_discussion` | 70 |
| `analytical_explanation` | 179 |
| `short_analysis_or_highlight` | 5 |
| `collaborative_discussion` | 10 |
| `match_commentary` | 23 |
| `promotion_housekeeping` | 1 |
| `personal_editorial` | 4 |

## Highest visual-review priorities

| Segment | Time | Video | Topic | Density | Relevance | Transcript | Visual |
|---|---|---|---|---:|---:|---:|---:|
| `JM50b3IU6-c:008` | 00:17:43–00:20:48 | How to Play Split Comps in Overwatch (Toronto vs Washington) | `macro_space_tempo` | 67 | 89 | 84 | 78 |
| `QvMsOy1wFr4:009` | 00:25:21–00:28:24 | How NRG Won (And Lost) Overwatch Rock Paper Scissors | `fight_execution_review` | 53 | 84 | 82 | 77 |
| `cXnFhS2l47g:001` | 00:00:02–00:03:22 | How the Best NA OWCS Team Got Their Revenge | `macro_space_tempo` | 69 | 88 | 83 | 76 |
| `AcAxvnAEYpg:005` | 00:11:59–00:14:40 | How Are Old OWL Players Still So Good? | `macro_space_tempo` | 67 | 87 | 84 | 76 |
| `jSCHyAWoUjc:003` | 00:06:34–00:10:06 | Rokit Makes Vendetta Look Broken | `macro_space_tempo` | 59 | 87 | 83 | 76 |
| `K6Ayz-NHVe4:003` | 00:07:07–00:10:18 | How Korea Solved Overwatch | `macro_space_tempo` | 44 | 85 | 82 | 76 |
| `MYW1ztAeDQc:004` | 00:09:39–00:12:43 | Why do Dives Always Kill You | `composition_matchups` | 64 | 86 | 82 | 75 |
| `GIY_4hD9_M8:008` | 00:18:50–00:21:48 | How T1 Beat the Best Overwatch Team in the World | `composition_matchups` | 58 | 84 | 83 | 75 |
| `GIY_4hD9_M8:014` | 00:38:04–00:41:09 | How T1 Beat the Best Overwatch Team in the World | `macro_space_tempo` | 58 | 85 | 83 | 75 |
| `nddeTxFzT6Q:004` | 00:08:52–00:12:09 | How to Play the Easiest Role in Overwatch (Hitscan) | `fight_execution_review` | 63 | 84 | 84 | 74 |
| `1OvQ5PAK0w0:002` | 00:02:39–00:05:29 | Why Good Players Make Stupid Mistakes | `fight_execution_review` | 60 | 84 | 84 | 74 |
| `GIY_4hD9_M8:013` | 00:35:01–00:38:06 | How T1 Beat the Best Overwatch Team in the World | `macro_space_tempo` | 60 | 86 | 83 | 74 |
| `cXnFhS2l47g:004` | 00:08:15–00:10:44 | How the Best NA OWCS Team Got Their Revenge | `macro_space_tempo` | 58 | 87 | 82 | 74 |
| `pMPwEwNEiQA:004` | 00:08:44–00:11:39 | What You're Missing on Genji | `macro_space_tempo` | 51 | 86 | 83 | 74 |
| `KLwLiiYYewQ:001` | 00:00:00–00:00:54 | DON'T hold the choke? | `macro_space_tempo` | 50 | 87 | 80 | 74 |
| `Hl-nV1aF1yE:002` | 00:02:17–00:04:49 | Back Up to Go Forward | `macro_space_tempo` | 67 | 85 | 83 | 73 |
| `M8393UkZxjY:005` | 00:13:09–00:16:07 | Why Does Team Liquid Evaporate on Stage | `macro_space_tempo` | 64 | 87 | 83 | 73 |
| `GIY_4hD9_M8:005` | 00:12:21–00:14:36 | How T1 Beat the Best Overwatch Team in the World | `composition_matchups` | 61 | 85 | 81 | 73 |
| `QvMsOy1wFr4:007` | 00:19:54–00:23:17 | How NRG Won (And Lost) Overwatch Rock Paper Scissors | `macro_space_tempo` | 61 | 87 | 82 | 73 |
| `Hl-nV1aF1yE:001` | 00:00:00–00:02:19 | Back Up to Go Forward | `macro_space_tempo` | 60 | 87 | 83 | 73 |

## Segmentation method

Sections target roughly three minutes. Candidate boundaries are selected between two and four minutes using caption gaps, transition phrases, local vocabulary shifts, and proximity to the target length. A final tail shorter than 70 seconds is merged into the prior section. Shorts remain one section.

Topic labels use transparent domain lexicons and title context. Scores use observable transcript features stored in each JSONL row. They are reproducible and can be revised without changing the caption source.

## Calibration and audit

The first draft overclassified pro-team analysis because broad words such as “team,” “player,” and “match” dominated that label, and it penalized normal spoken filler too heavily. Those terms and weights were revised. The second draft was audited across every video aggregate, the highest visual priorities, the lowest seriousness scores, and samples at the minimum, quartiles, median, and maximum information density.

The sample ordering behaved as intended: a 22-second reaction clip ranked at the low-density end; casual watch-party banter ranked below structured explanation; a Hazard rotation explanation ranked near the middle; structured team-review material ranked above it; and a dive-mirror hypothetical with explicit causal framing ranked at the top. This is a triage validation, not proof that every label is semantically perfect.

## Limits carried forward

Automatic captions contain misspelled names and Overwatch terms. A section can be strategically important even when its score is moderate, especially if the explanation relies on an image rather than explicit narration. The review queue retains all 292 sections; no material was discarded. Pass 4 should treat scores as prioritization signals, extract claims from a broad sample across topics and dates, and preserve contradictions and evolution rather than studying Tier A alone.
