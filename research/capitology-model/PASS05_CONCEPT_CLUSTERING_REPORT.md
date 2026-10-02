# Pass 5 — provisional concept clustering

The transcript-grounded Pass 4 ledger contains 206 provisional claims. This pass assigns each claim one primary concept, adds optional cross-links, and records relationships that later passes can test. It organizes **what the channel says**; it does not verify match events, establish causal effects, or write the final Overwatch model.

## Coverage and files

| Measure | Result |
|---|---:|
| Pass 4 claims assigned exactly one primary cluster | 206 / 206 |
| Primary clusters | 16 |
| Additional secondary memberships | 316 |
| Explicit concept relationships | 12 |
| Claims with high visual dependency | 164 / 206 |
| Gameplay examples independently checked | 0 |

- `pass05_concept_index.csv` preserves the source claim, date, URL, scope, confidence, visual dependency, and primary and secondary cluster assignments on each row.
- `pass05_cluster_registry.json` records each cluster's primary IDs, counts by upload year, distinct source videos, and high-visual count.
- `pass05_relationships.csv` contains directional, provisional connections with supporting claim IDs and an open-review status.
- `pass05_clusters_seed.py` is the manually assigned, reproducible source. It asserts that the 206 Pass 4 IDs each occur exactly once in primary membership. A primary home is an indexing decision, not a claim that the idea cannot belong elsewhere.

Counts measure **selected claims**, not how often Capitology held an idea. Several claims can come from a single long video; the clustering does not treat those as independent observations. The source ledger is paraphrased automatic caption evidence, with player and guest attribution sometimes uncertain.

## Cluster map

| Cluster | Primary claims | Videos | What belongs here | Boundary or exception to retain |
|---|---:|---:|---|---|
| C01 Turns and initiative | 13 | 7 | The 2023 definition of a turn, early and later turns, cooldown-first moves, the 2026 warning that “first/second” alone is weak advice. P4-005–008, P4-033, P4-109, P4-197, P4-206. | A first turn is not necessarily a full engage; an advantage can be held and stacked before the next move. |
| C02 Information and concealment | 7 | 5 | Broad sight, scouting, revealing the opponent's approach, then hiding the final setup. P4-019–020, P4-132, P4-183, P4-202. | Seeing more is useful only from survivable positions; scouting a named target is narrower than broad team sight. |
| C03 Reach, corners, and voluntary space | 13 | 4 | Tank–backline reach, off-corner positions, the “pocket,” early retreat with resources, and corner stalemates. P4-009, P4-030–032, P4-075–076, P4-103, P4-162–163, P4-200. | Backing up after being forced and backing out early to create a later push are explicitly distinguished. Map geometry controls how much can be yielded. |
| C04 Split cores and attention exchange | 14 | 3 | 2023 two-core push/pull, distance and retake constraints, later attention balancing and delayed splits. P4-001–004, P4-091, P4-104–107, P4-143–144, P4-193. | Ten primary claims are from 2023, largely one explanatory video. Do not infer a universal split doctrine from that count. |
| C05 Engage staging and prevention | 22 | 8 | Dive quality, denying a favorable setup, soft probes, synchronized tank/DPS windows, and staging without spending the finishing resources. P4-016–018, P4-063–064, P4-133–139, P4-145–146, P4-205. | “Cannot live a good dive” is his conditional rhetoric about an already good setup; it does not mean no backline can survive a dive. |
| C06 Bait and opponent choices | 12 | 5 | Apply enough pressure to induce a decision, make a credible cooldown or position offer, cover responses, and recognize when the opponent declines or exploits the bait. P4-015, P4-034–035, P4-054, P4-092, P4-125, P4-189–190, P4-199. | Bait can lose a player, cede too much space, or leave too few cooldowns for the counter. |
| C07 Cooldown and role windows | 6 | 5 | A brief missing cooldown can create a small opportunity; decide whether the tank, DPS, support, or whole team can use it. P4-025, P4-081–082, P4-155, P4-164, P4-187. | Finding a window is separate from deciding its size and beneficiary. Many other claims link here secondarily. |
| C08 Ultimate use and economy | 13 | 6 | The 2026 qualified economy thesis, charging and spending around objective state, sequencing, kiting, and specific failed examples. P4-026–029, P4-036–037, P4-053, P4-086, P4-147, P4-176, P4-198. | D.Va/Zarya/Symmetra and other named matchups can make economy central. Spending several ults to win differs from spending them and losing. |
| C09 Composition and matchup adaptation | 23 | 11 | Win conditions, support bans, repeated teleport cycles, draft preparation, target allocation, resource budgets, and setup adaptations. P4-058, P4-070–072, P4-080, P4-117, P4-167, P4-172–174, P4-184–186, P4-204. | Matchup and patch context are essential. Tournament outcome alone does not prove a lineup universally best. |
| C10 Objective and retake routes | 6 | 5 | Where to establish the retake, when to touch, whether a point flip creates a defensible follow-up, and how to contest a room's exit. P4-038, P4-153–154, P4-161, P4-165, P4-177. | Point pressure is a tool for staging or forcing a choice, not automatically a reason to cluster on point. |
| C11 Tank execution | 12 | 3 | Mauga armor, ammunition, pin/cage choices; Hazard scouting and target selection; Winston/Ball defensive-cooldown outplay. P4-046–048, P4-056–057, P4-065–066, P4-114–116, P4-127–128. | Narrow hero and patch examples should not be promoted into timeless tank rules. |
| C12 Damage-role execution | 34 | 11 | Hitscan pressure and safe angles, flex DPS exit and attention, target choice, timing, aim, and duel prediction. P4-044–045, P4-067–068, P4-073–074, P4-078–079, P4-140–142, P4-151–152, P4-191–192. | This is the largest cluster because the ledger contains multiple role guides; its size is not evidence that DPS mechanics outweigh team concepts. |
| C13 Support positioning and escape | 7 | 4 | Brigitte exposure and peel, Kiriko teleport destination, and when a support may remain off the frontline. P4-043, P4-049, P4-059, P4-123–124, P4-179, P4-188. | A protected support still needs to threaten or help the frontline; survival without contribution is not the goal. |
| C14 Attention and match execution | 6 | 4 | Genji gaze tracking, failed execution of a known interaction, reset attention, and mechanics in close fights. P4-012–013, P4-096, P4-150, P4-156–157. | A correct setup may lose to execution; a lost example does not by itself disprove the setup. |
| C15 Observation and coaching method | 13 | 7 | Reconstruct what players knew, compare similar replays, write down details, ask narrow questions, and practice specific actions. P4-022–023, P4-040–042, P4-097–098, P4-168, P4-203. | These are advice and stated methods, not measured evidence that a training intervention works. |
| C16 Balance and design views | 5 | 2 | Role-wide viability, hero alternatives, and counterplay in pre-release design impressions. P4-077, P4-099, P4-159–160, P4-201. | Design opinions and predictions remain outside the strategic gameplay evidence chain. |

The registry gives the exact complete ID set for each cluster; the examples above are navigational anchors. The concept index retains secondary memberships when, for example, a support positioning claim also concerns geometry or a tank move opens a DPS window.

## Relationships to test

These are candidate mechanisms assembled from **spoken claims**. The relation file includes all 12 with claim-level anchors.

1. **Information → staging:** forward sight can reveal the approach, then a team can hide its final position (P4-019–020, P4-132, P4-183). Footage must confirm who actually sees whom.
2. **Geometry → timing:** the reach of a corner or “pocket” determines whether an early cooldown turn can be spent safely and whether a retreat preserves a later turn (P4-011, P4-031–032, P4-075–076, P4-109).
3. **Splits → bait:** one pressured core can survive and yield while a second creates counterpressure; a delayed split may make the opponent chase the wrong initial group (P4-003–004, P4-091, P4-143–144, P4-193).
4. **Setup prevention → backline survival:** a team can clear an angle or force a poor jump before asking supports to survive an already favorable attack (P4-016–018, P4-134, P4-175).
5. **Bait ↔ counterplay:** a predictable cooldown offer can guide the opponent, but the opponent can take a different route, stack advantages, or force a fight when the baiting side lacks the resources to respond (P4-034–035, P4-199, P4-206).
6. **Window → role selection:** a small opening can justify an angle or tank step without bringing the whole backline into reach (P4-081–082, P4-155, P4-164, P4-187).
7. **Ultimate economy ↔ objective state:** counts spent should be considered alongside the fight result, charge recovered, retake difficulty, and setup after the flip (P4-026, P4-029, P4-036, P4-038, P4-053, P4-158, P4-198).
8. **Composition → exception:** a teleport cycle or off-tank composition can change how much economy and repeated cooldown denial matter (P4-026, P4-058, P4-072, P4-080, P4-086, P4-117, P4-147).
9. **Tank entry → DPS opportunity:** even a strong jump is wasted if the damage angle is absent, late, or unable to reach the target (P4-064, P4-145, P4-170, P4-180). This is a timing hypothesis, not a verified replay conclusion.
10. **Geometry ↔ damage pressure:** a hitscan needs a position safe from a trade but close and open enough to damage the walk-up (P4-044–045, P4-073–074, P4-108, P4-130–131).
11. **Knowledge → in-game execution:** the attention process and repeated practice are distinct from stating the correct plan after the match (P4-022–023, P4-096–098, P4-150, P4-156).
12. **Design opinions ≠ match evidence:** pre-release judgments and balance preferences should be examined as such, not mixed with observed tactical examples (P4-077, P4-080, P4-099, P4-159–160, P4-201).

## Candidate tensions and temporal questions

| Question for Pass 8 | Evidence to compare | Present status |
|---|---|---|
| Do 2023 turns and 2026 first/second descriptions use the same decision unit? | P4-005–008; P4-014; P4-033–035; P4-100; P4-109; P4-196–199; P4-206 | The later account gives operational detail and counterplay; no contradiction established. |
| Does “lock eyes and fight” conflict with “go back to go forward”? | P4-021; P4-030–032; P4-133; P4-200 | He explicitly distinguishes an early, unforced retreat from a late forced one. Distances and options need video. |
| Does “ultimate economy does not matter” conflict with named ult-dependent fights? | P4-026–029; P4-036–038; P4-053; P4-086; P4-117–121; P4-147; P4-158; P4-198 | The spoken thesis is qualified. Test whether particular examples still overstate or understate the exception. |
| Is an early setup clear always preferable to living an incoming dive? | P4-016–018; P4-063–064; P4-134; P4-171; P4-175; P4-181 | No universal rule in the ledger; matchup, ults, routes, and objective state matter. |
| Can playing second retain initiative without conceding the map? | P4-015; P4-034–035; P4-054; P4-095; P4-125; P4-189–190; P4-199; P4-206 | The claimed mechanism requires pressure and flexible answers. Failure cases remain important. |
| Is the 2023 two-core push/pull the same as the 2026 repeated aggro exchange? | P4-001–004; P4-091; P4-104–107; P4-143–144; P4-193 | Related vocabulary; different comps and durations. Do not merge them as one universal mechanic yet. |

## Handoff

Pass 5 is an index and hypothesis map. Pass 6 should select representative footage across *both sides* of these relationships, including failures and counterexamples, rather than only attractive examples. Pass 7 should inspect both teams' POVs, sight lines, cooldowns, and objective state. Pass 8 can then adjudicate apparent conflicts and evolution. The `model.md` synthesis scaffold remains untouched.
