# Capitology's Overwatch model — provisional synthesis

This reconstructs the speaker's stated decision framework from 54 known uploads, 206 selected caption-grounded claims, 16 clusters, 23 selectively reviewed video windows, and ten Pass 8 adjudications. The 24 rules below cite 120 distinct claim anchors. They are conditional coaching hypotheses, not measured laws or a claim that the selected fights prove causation.

**How to use it in a match review:** establish player/POV and observable fight state first; identify which rule's trigger actually occurred; compare the observed action and response with its conditional alternative; report the exception and uncertainty. A bad outcome alone is not proof of a bad choice. The machine-readable companion is `pass09_rules.json`.

## Vocabulary and evidence

- **Turn:** a bounded opportunity to spend resources or space proactively. First/second describes timing, not a full fight instruction.
- **Pocket / reach:** the map region where the opponent can initiate an effective hit, varying by heroes, resources, and sight lines.
- **Staging:** the route, angles, information, and resources set before a decisive engage.
- **Split / core:** separated pressure groups that can exchange enemy attention and counterpressure; their exact formation depends on matchup.
- **Evidence tags:** `sampled_visual` means selected edited 480p windows were inspected; `illustrative_visual` means mostly diagrams or limited POV; `transcript_only` means no selected visual test. None means full replay validation. Speaker-model confidence and gameplay effectiveness are separate.

## Candidate unifying structure

A team uses space, sight, objective pressure, and resource timing to change the opponent's available responses, then needs a useful answer to the actual response. This connects turns, bait, retreat, dive prevention, splits, and ultimate conversion. It is a synthesis of selected explanations, not a universal rule or a substitute for mechanics, role duties, matchup, and objective clock.

## Core decision model

### CAP-01 — A turn is a bounded opportunity

A turn spends cooldowns or takes space for proactive value; first, second, and neutralizing turns describe timing, not a complete plan.

**When:** Before a team commits resources or chooses to wait for the opponent. **Action:** Name the specific space, cooldown, target, or response the turn should gain, and the next move if it does not finish the fight.

**Boundary:** A first turn can be soft pressure rather than an all-team engage; a role window may be smaller than a team turn.

**Evidence:** [P4-005](https://www.youtube.com/watch?v=c92ESPjlveI&t=58s), [P4-006](https://www.youtube.com/watch?v=c92ESPjlveI&t=125s), [P4-033](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=0s), [P4-081](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=720s), [P4-109](https://www.youtube.com/watch?v=z9n-JNB52rk&t=606s). Visual: V6-01, V6-03. Level: `sampled_visual`.

### CAP-02 — Preserve a useful next response

The first exchange should create or retain an answer to the opponent's likely reply; inducing a cooldown alone does not win the fight.

**When:** After pressure forces an enemy cooldown, rotation, or ultimate. **Action:** Check whether the team has distance, angle, resources, and time to punish the actual response; delay commitment to stack advantages when needed.

**Boundary:** A fast finish can be correct when the response is already exposed; the opponent may decline the offered route.

**Evidence:** [P4-008](https://www.youtube.com/watch?v=c92ESPjlveI&t=550s), [P4-015](https://www.youtube.com/watch?v=K6Ayz-NHVe4&t=400s), [P4-035](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=635s), [P4-118](https://www.youtube.com/watch?v=QvMsOy1wFr4&t=212s), [P4-199](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=370s), [P4-206](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=555s). Visual: V6-02, V6-04, V6-17, V6-18. Level: `sampled_visual`.

### CAP-08 — Bait needs a punish and a fallback

Offering a cooldown, player, or lane can shape an opponent's choice only if the offer is credible and the baiting side can survive and answer it.

**When:** A team intends to play second or lure an engage. **Action:** State the desired enemy action, the cost of the offer, the counter, and a response if the opponent clears a different lane.

**Boundary:** The first mover may correctly accept the bait and win; a passive kite with no counterpressure is not enough.

**Evidence:** [P4-015](https://www.youtube.com/watch?v=K6Ayz-NHVe4&t=400s), [P4-034](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=135s), [P4-035](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=635s), [P4-054](https://www.youtube.com/watch?v=QvMsOy1wFr4&t=730s), [P4-125](https://www.youtube.com/watch?v=K6Ayz-NHVe4&t=773s), [P4-199](https://www.youtube.com/watch?v=KlcWDgdXrZk&t=370s). Visual: V6-03, V6-16, V6-17, V6-18, V6-19. Level: `sampled_visual`.

### CAP-09 — Use objective pressure to force a choice

Cart or point pressure can create an enemy response that opens an angle or later turn, but occupying objective is not automatically the best fight location.

**When:** A retake or attack stalls against a strong hold. **Action:** Choose whether touching, threatening a route, or clearing an exit makes the defender move; set up the fight that follows the touch.

**Boundary:** A panic flip without defensible angles or follow-up may leave the team worse off.

**Evidence:** [P4-007](https://www.youtube.com/watch?v=c92ESPjlveI&t=395s), [P4-038](https://www.youtube.com/watch?v=GKkzCd9cvUg&t=390s), [P4-153](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=1s), [P4-154](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=184s), [P4-177](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=2090s). Visual: V6-01, V6-11. Level: `sampled_visual`.

### CAP-14 — Size a window to the role that can use it

A missing cooldown can permit a tank step, DPS angle, or distant support contribution without authorizing the whole team to walk into reach.

**When:** A brief resource or position advantage appears. **Action:** Identify which player can profit within the window and who should retain an offset position.

**Boundary:** A coordinated full engage is justified when the opening and follow-up actually support it.

**Evidence:** [P4-081](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=720s), [P4-082](https://www.youtube.com/watch?v=Y4ORvoqZ1P0&t=230s), [P4-155](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=362s), [P4-164](https://www.youtube.com/watch?v=ln2t2rl1KYw&t=1059s), [P4-187](https://www.youtube.com/watch?v=GYBpp0KM5-Q&t=369s). Visual: no selected visual window. Level: `transcript_only`.

## Space, information, and setup

### CAP-03 — Know the opponent's reach

Entering the opponent's effective engage range without a route and reply can force resources merely to survive.

**When:** Walking through a choke, corner, or staging lane toward an enemy setup. **Action:** Scout the pocket, identify the threatened angle and available counter, and cross when a chosen threat can be made.

**Boundary:** The pocket depends on hero, cooldown, sight line, and objective; distance alone is not the rule.

**Evidence:** [P4-009](https://www.youtube.com/watch?v=z9n-JNB52rk&t=39s), [P4-075](https://www.youtube.com/watch?v=ln2t2rl1KYw&t=80s), [P4-076](https://www.youtube.com/watch?v=ln2t2rl1KYw&t=620s), [P4-162](https://www.youtube.com/watch?v=ln2t2rl1KYw&t=236s), [P4-163](https://www.youtube.com/watch?v=ln2t2rl1KYw&t=421s). Visual: V6-06. Level: `illustrative_visual`.

### CAP-04 — Reset before displacement becomes forced

An early voluntary pull with cooldowns and map distance can preserve a later initiation; backing away only after an enemy finishes staging may surrender the next corner too.

**When:** A planned push is blocked or the current fight location is unfavorable. **Action:** Leave before pursuit closes, use cover or a new route to conceal the next fight, and decide where to re-engage.

**Boundary:** Do not give a critical corner or objective for free when the team can contest the enemy setup; a late forced retreat is a different action.

**Evidence:** [P4-021](https://www.youtube.com/watch?v=LpxT2dykNK0&t=40s), [P4-030](https://www.youtube.com/watch?v=Hl-nV1aF1yE&t=55s), [P4-031](https://www.youtube.com/watch?v=Hl-nV1aF1yE&t=190s), [P4-032](https://www.youtube.com/watch?v=Hl-nV1aF1yE&t=345s), [P4-133](https://www.youtube.com/watch?v=LpxT2dykNK0&t=219s), [P4-200](https://www.youtube.com/watch?v=Hl-nV1aF1yE&t=424s). Visual: V6-05, V6-06, V6-07. Level: `sampled_visual`.

### CAP-05 — Scout, then conceal

Safe forward sight can reveal the opponent's approach before the team withdraws to a less visible final setup.

**When:** Between fights, before choosing a defensive or attacking route. **Action:** Gather sight without sacrificing survival; communicate the route, then hide the final positioning or timing.

**Boundary:** Do not equate a single player's view with the entire team's knowledge; the scouting position itself can be punishable.

**Evidence:** [P4-019](https://www.youtube.com/watch?v=E1bYy6OE_OQ&t=45s), [P4-020](https://www.youtube.com/watch?v=E1bYy6OE_OQ&t=120s), [P4-132](https://www.youtube.com/watch?v=E1bYy6OE_OQ&t=321s), [P4-183](https://www.youtube.com/watch?v=cXnFhS2l47g&t=200s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-06 — Prevent a strong dive before surviving it

A completed, well-staged dive is hard to answer by support cooldown execution alone; the defense can contest the DPS angle, tank route, or approach first.

**When:** An enemy dive is assembling a short jump and supporting angles. **Action:** Clear or displace staging, rotate wide, or use a timely defensive ultimate if it prevents the setup from maturing.

**Boundary:** This is not a claim that every dive kills or that an early ultimate is always optimal; matchup and remaining threats matter.

**Evidence:** [P4-016](https://www.youtube.com/watch?v=MYW1ztAeDQc&t=55s), [P4-017](https://www.youtube.com/watch?v=MYW1ztAeDQc&t=245s), [P4-018](https://www.youtube.com/watch?v=MYW1ztAeDQc&t=600s), [P4-134](https://www.youtube.com/watch?v=MYW1ztAeDQc&t=761s), [P4-171](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=192s), [P4-175](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=1220s). Visual: V6-12, V6-13, V6-14, V6-15. Level: `sampled_visual`.

### CAP-20 — Retake routes are fight plans

A retake route should remove a dangerous setup or threaten a useful exit rather than automatically walk straight onto objective.

**When:** The defending team controls a room, choke, side lane, or pre-staged dive. **Action:** Choose a route with enough team support to establish the needed side, then time the touch to the resulting fight.

**Boundary:** A small unsupported split can be cleared before it creates pressure; clock state may force an earlier touch.

**Evidence:** [P4-018](https://www.youtube.com/watch?v=MYW1ztAeDQc&t=600s), [P4-153](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=1s), [P4-154](https://www.youtube.com/watch?v=AcAxvnAEYpg&t=184s), [P4-161](https://www.youtube.com/watch?v=TOaKp3Z44ho&t=746s), [P4-165](https://www.youtube.com/watch?v=aNBstKtsPms&t=418s), [P4-177](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=2090s). Visual: V6-13. Level: `illustrative_visual`.

## Split compositions and adaptations

### CAP-10 — Split cores trade attention

When one group is pressured, it yields while another creates timely angle, cooldown, kill, or objective value.

**When:** Playing a composition with two or more viable pressure groups. **Action:** Keep groups near enough to counterpressure, identify who carries attention, and communicate when to yield or re-enter.

**Boundary:** Advancing both pressured groups at once can discard the exchange; excessive separation makes the reply late.

**Evidence:** [P4-001](https://www.youtube.com/watch?v=JM50b3IU6-c&t=47s), [P4-003](https://www.youtube.com/watch?v=JM50b3IU6-c&t=540s), [P4-004](https://www.youtube.com/watch?v=JM50b3IU6-c&t=1120s), [P4-104](https://www.youtube.com/watch?v=JM50b3IU6-c&t=610s), [P4-107](https://www.youtube.com/watch?v=JM50b3IU6-c&t=1260s), [P4-091](https://www.youtube.com/watch?v=ijlmDdVIdtk&t=70s). Visual: V6-20, V6-21, V6-22. Level: `sampled_visual`.

### CAP-11 — Delay a predictable split

A split may begin grouped when an opponent can instantly clear an obvious outside lane, then form after the clear commits.

**When:** An enemy teleport, D.Va, or fast rotation threatens a pre-shown off angle. **Action:** Scout the clear, protect the first pressured group, and separate when the opponent's movement exposes a second lane.

**Boundary:** This is a matchup adaptation, not a rule to retake as five in every split composition.

**Evidence:** [P4-105](https://www.youtube.com/watch?v=JM50b3IU6-c&t=800s), [P4-143](https://www.youtube.com/watch?v=M8393UkZxjY&t=357s), [P4-144](https://www.youtube.com/watch?v=M8393UkZxjY&t=599s), [P4-193](https://www.youtube.com/watch?v=ijlmDdVIdtk&t=161s). Visual: V6-23. Level: `sampled_visual`.

### CAP-19 — Matchups require repeated answers

A counter composition must answer the opponent's recurring setup cycles, not merely the first teleport or engage.

**When:** Drafting or adapting against a composition with repeatable movement or cooldown threats. **Action:** Compare neutral and ultimate fights, staging routes, repeated denial, and the resources each player needs.

**Boundary:** A tournament-winning lineup or one lost fight does not establish a universally best composition.

**Evidence:** [P4-058](https://www.youtube.com/watch?v=GYBpp0KM5-Q&t=170s), [P4-070](https://www.youtube.com/watch?v=vu4KmVKp2f0&t=35s), [P4-071](https://www.youtube.com/watch?v=vu4KmVKp2f0&t=125s), [P4-072](https://www.youtube.com/watch?v=vu4KmVKp2f0&t=390s), [P4-080](https://www.youtube.com/watch?v=sqtmsbHxrLE&t=215s), [P4-204](https://www.youtube.com/watch?v=t1dnez3yuZ4&t=398s). Visual: no selected visual window. Level: `transcript_only`.

## Resources and ultimate economy

### CAP-12 — Evaluate ultimate spend by conversion

Ult count matters through the fight it wins, the objective state, the following setup, and the charge recovered, not as inventory alone.

**When:** Choosing whether to combine ultimates or judging an apparent over-spend. **Action:** Check whether the expenditure secures the fight or denies a severe retake loss, and whether the team can hold useful angles afterward.

**Boundary:** A triple spend for a panic point flip can be genuine waste. The broader OW1/OW2 era comparison remains untested.

**Evidence:** [P4-026](https://www.youtube.com/watch?v=aHwWbiUE4KQ&t=0s), [P4-029](https://www.youtube.com/watch?v=aHwWbiUE4KQ&t=440s), [P4-036](https://www.youtube.com/watch?v=GKkzCd9cvUg&t=110s), [P4-038](https://www.youtube.com/watch?v=GKkzCd9cvUg&t=390s), [P4-053](https://www.youtube.com/watch?v=QvMsOy1wFr4&t=575s), [P4-198](https://www.youtube.com/watch?v=GKkzCd9cvUg&t=722s). Visual: V6-08, V6-10, V6-11. Level: `sampled_visual`.

### CAP-13 — Economy exceptions depend on composition

Some compositions and matchups depend strongly on ultimate cycles or a particular defensive answer even when a generic inventory heuristic is weak.

**When:** A plan relies on a named ultimate interaction, teleport cycle, or near-charged defensive tool. **Action:** Plan the neutral and ultimate fights separately; farm or preserve the specific answer before committing when required.

**Boundary:** The claim that economy is generally less decisive in OW2 than OW1 is an attributed thesis, not a measured fact in this corpus.

**Evidence:** [P4-026](https://www.youtube.com/watch?v=aHwWbiUE4KQ&t=0s), [P4-086](https://www.youtube.com/watch?v=t1dnez3yuZ4&t=510s), [P4-117](https://www.youtube.com/watch?v=QvMsOy1wFr4&t=1s), [P4-147](https://www.youtube.com/watch?v=t1dnez3yuZ4&t=130s), [P4-158](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=873s). Visual: V6-09. Level: `illustrative_visual`.

### CAP-15 — Tank resources shape the next exchange

Armor, ammunition, defensive abilities, and a safe exit affect whether a tank's entry remains threatening after the first contact.

**When:** A tank is about to commit movement or an ultimate. **Action:** Restore or reserve the resource that sustains the midfight; place the engage for the team's intended follow-up.

**Boundary:** Mauga, Hazard, Winston, and Ball examples are hero- and patch-specific; do not transfer their micro literally to every tank.

**Evidence:** [P4-046](https://www.youtube.com/watch?v=V-Y0hBOI1yY&t=90s), [P4-047](https://www.youtube.com/watch?v=V-Y0hBOI1yY&t=530s), [P4-048](https://www.youtube.com/watch?v=V-Y0hBOI1yY&t=635s), [P4-065](https://www.youtube.com/watch?v=SJdCkYn6Is0&t=35s), [P4-066](https://www.youtube.com/watch?v=SJdCkYn6Is0&t=385s), [P4-127](https://www.youtube.com/watch?v=V-Y0hBOI1yY&t=374s). Visual: no selected visual window. Level: `transcript_only`.

## Role-specific execution

### CAP-07 — Match damage timing to the tank window

A tank entry creates only a short opportunity if damage players have not staged a matching sight line or burst route.

**When:** Planning a jump, clearing move, nano dive, or short burst engage. **Action:** Establish the damage angle and support path before the tank spends the entry resource; synchronize follow-up to its actual window.

**Boundary:** A soft tank move may deliberately seek information or cooldowns rather than an immediate kill.

**Evidence:** [P4-064](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=2350s), [P4-145](https://www.youtube.com/watch?v=M8393UkZxjY&t=1139s), [P4-170](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=60s), [P4-180](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=2890s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-16 — A damage angle must pressure and survive

An angle too far back removes pressure; one inside easy enemy reach becomes the next trade.

**When:** A hitscan or other damage player chooses a pre-fight angle or withdrawal path. **Action:** Keep useful sight on the walk-up and a route to leave before the enemy clear reaches the position.

**Boundary:** Do not force a flank when it adds no sight line; the 2024 hitscan ASR is garbled and requires audio for fine hero-specific claims.

**Evidence:** [P4-044](https://www.youtube.com/watch?v=nddeTxFzT6Q&t=45s), [P4-045](https://www.youtube.com/watch?v=nddeTxFzT6Q&t=635s), [P4-073](https://www.youtube.com/watch?v=aNBstKtsPms&t=160s), [P4-074](https://www.youtube.com/watch?v=aNBstKtsPms&t=295s), [P4-108](https://www.youtube.com/watch?v=z9n-JNB52rk&t=204s), [P4-192](https://www.youtube.com/watch?v=prUv2eNrGD0&t=1218s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-17 — Preserve a flex DPS exit and re-entry

Drawing attention without dying can create value; leaving before a forced clear allows a later angle or burst window.

**When:** An off-angle DPS is marked or several opponents turn toward them. **Action:** Use movement and an ally route to leave early, contribute from a safer angle, then re-enter when the clearer spends resources or retreats.

**Boundary:** An available ultimate or flank is not automatically better than the current neutral pressure.

**Evidence:** [P4-012](https://www.youtube.com/watch?v=pMPwEwNEiQA&t=115s), [P4-067](https://www.youtube.com/watch?v=xabIcyolpJA&t=115s), [P4-068](https://www.youtube.com/watch?v=xabIcyolpJA&t=295s), [P4-111](https://www.youtube.com/watch?v=pMPwEwNEiQA&t=182s), [P4-112](https://www.youtube.com/watch?v=pMPwEwNEiQA&t=696s), [P4-140](https://www.youtube.com/watch?v=jSCHyAWoUjc&t=94s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-18 — Support escape is a team setup

A support escape route or teleport destination should be planned before the first diver forces movement, while preserving useful midfight sight.

**When:** An enemy dive can reach the backline or the team prepares to flip map. **Action:** Position teammates and an offset support to provide a safe destination and early warning.

**Boundary:** Specific Kiriko–Lucio and Brigitte interactions are composition-specific; survival without contribution is not the goal.

**Evidence:** [P4-049](https://www.youtube.com/watch?v=XhcF5IzJDq4&t=200s), [P4-059](https://www.youtube.com/watch?v=GYBpp0KM5-Q&t=735s), [P4-123](https://www.youtube.com/watch?v=XhcF5IzJDq4&t=535s), [P4-124](https://www.youtube.com/watch?v=XhcF5IzJDq4&t=914s), [P4-175](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=1220s), [P4-179](https://www.youtube.com/watch?v=GIY_4hD9_M8&t=2686s), [P4-188](https://www.youtube.com/watch?v=GYBpp0KM5-Q&t=896s). Visual: V6-15. Level: `illustrative_visual`.

### CAP-23 — Aim uses prediction and context

Anticipating a likely strafe or holding a well-placed crosshair can be more consistent than chasing every movement, but over-waiting gives the opponent time to shoot.

**When:** Reviewing a hitscan duel or repeated missed follow-up shots. **Action:** Read the opponent's short or long strafe and choose whether to follow, cut off, or wait for a return.

**Boundary:** This is not a replacement for aim mechanics or a universal instruction to stop moving the cursor.

**Evidence:** [P4-078](https://www.youtube.com/watch?v=LSrm0ocaS1Q&t=65s), [P4-079](https://www.youtube.com/watch?v=LSrm0ocaS1Q&t=480s), [P4-129](https://www.youtube.com/watch?v=nddeTxFzT6Q&t=168s), [P4-151](https://www.youtube.com/watch?v=LSrm0ocaS1Q&t=182s), [P4-152](https://www.youtube.com/watch?v=LSrm0ocaS1Q&t=830s). Visual: no selected visual window. Level: `transcript_only`.

## Learning, attention, and scope

### CAP-21 — Execution and attention limit a correct plan

A sound setup can lose to missed shots, delayed attention, or failure to execute a known interaction under match pressure.

**When:** Reviewing a lost fight whose pre-fight plan appears plausible. **Action:** Separate setup, information, target choice, mechanics, and attention at the moment of decision before rewriting the entire plan.

**Boundary:** Do not use mechanics as an unfalsifiable excuse for a weak setup; outcome alone does not identify the cause.

**Evidence:** [P4-022](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=30s), [P4-023](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=110s), [P4-088](https://www.youtube.com/watch?v=FjoWkH6Sl1k&t=675s), [P4-096](https://www.youtube.com/watch?v=iLX7uqsC1jE&t=750s), [P4-150](https://www.youtube.com/watch?v=sqtmsbHxrLE&t=674s), [P4-156](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=326s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-22 — Train observation and narrow actions

Replay study should reconstruct what a player could know, compare similar situations, and practice one or two specific in-game attention tasks.

**When:** A player knows a concept in review but cannot execute it reliably. **Action:** Write the observed sequence, state a tentative reading, compare a closely matched pro example, and rehearse a small concrete cue.

**Boundary:** These are coaching recommendations, not measured proof that a training method improves rank.

**Evidence:** [P4-022](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=30s), [P4-023](https://www.youtube.com/watch?v=1OvQ5PAK0w0&t=110s), [P4-040](https://www.youtube.com/watch?v=_pv_dhja-4w&t=135s), [P4-041](https://www.youtube.com/watch?v=_pv_dhja-4w&t=310s), [P4-042](https://www.youtube.com/watch?v=_pv_dhja-4w&t=620s), [P4-097](https://www.youtube.com/watch?v=iLX7uqsC1jE&t=1110s), [P4-098](https://www.youtube.com/watch?v=iLX7uqsC1jE&t=1180s). Visual: no selected visual window. Level: `transcript_only`.

### CAP-24 — Keep design opinions separate

Balance preferences and pre-release hero predictions express a design philosophy; they are not match evidence for a particular tactical rule.

**When:** Using commentary about viability, counterplay, or hero tuning to justify gameplay advice. **Action:** Label the statement as opinion or prediction and seek actual match examples before inferring a tactical consequence.

**Boundary:** A design view can still motivate a testable hypothesis; do not silently promote it to observation.

**Evidence:** [P4-077](https://www.youtube.com/watch?v=2X_yEWyNms0&t=105s), [P4-099](https://www.youtube.com/watch?v=x2jNJeKiMUU&t=985s), [P4-159](https://www.youtube.com/watch?v=2X_yEWyNms0&t=212s), [P4-160](https://www.youtube.com/watch?v=2X_yEWyNms0&t=390s), [P4-201](https://www.youtube.com/watch?v=x2jNJeKiMUU&t=60s). Visual: no selected visual window. Level: `transcript_only`.

## Contradictions, evolution, and limits

Pass 8 found no direct unconditional reversal among its ten priority comparisons. Later accounts generally add conditions: a voluntary reset differs from forced retreat; bait can be accepted or bypassed; a temporarily grouped start can precede a split; and ultimate inventory matters through the fight and resulting setup. The April 2026 follow-up explicitly calls one triple spend wasteful while maintaining that other multi-ultimate wins can be rational. See `PASS08_CONTRADICTION_EVOLUTION_REPORT.md` and `pass08_adjudications.jsonl` for the dated comparisons.

The assertion that ultimate economy generally became less decisive from Overwatch 1 to Overwatch 2 is attributable to the speaker but remains an unmeasured empirical comparison. Edited coaching videos, automatic captions, and 480p sampled windows cannot establish every player belief, cooldown order, complete fight outcome, or counterfactual. The 2024 hitscan and September 2026 guest transcripts are particularly garbled; verify audio before relying on fine attribution. Upload dates are not match dates. Design opinions and pre-release predictions are kept separate from match evidence.

## Evidence index and next validation

- `pass09_rules.json`: every rule, trigger, action, exception, cluster membership, source URLs/dates, visual window IDs, and evidence level.
- `pass04_claims.jsonl`, `pass05_concept_index.csv`, `pass07_visual_ledger.jsonl`, and `pass08_adjudications.jsonl`: underlying claims, mappings, sampled observations, and tensions.
- `MATCH_REVIEW_PROTOTYPE.md`: apply these rules to a new player's complete match only after observing the recording; do not match a rule from the final score or an isolated still.
