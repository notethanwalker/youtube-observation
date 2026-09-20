# Grappling Video Analysis Protocol

This protocol is mandatory for all future grappling/MMA video analysis in this repository.

## 1. Identity lock before technique analysis
- Establish the target athlete from a user-provided external reference or an explicit in-video anchor timestamp.
- Confirm at least two independent visual cues where possible: clothing, hair, body proportions, starting location, and known opponent.
- Never identify the target from a cropped technique sequence alone.

## 2. Track continuously in full frame
- Perform a full-video identity pass before detailed technique analysis.
- Use full-frame continuity checkpoints throughout the entire video.
- Crops are analysis aids only after the subject track has already been established in the uncropped footage.
- If the target leaves frame, is fully occluded, or overlaps another visually similar athlete, mark the track as interrupted.

## 3. Re-entry verification
After every track interruption:
- re-establish the target against the last verified full-frame checkpoint;
- compare to the original anchor/reference;
- use opponent identity and spatial continuity as secondary evidence;
- do not resume attribution until identity is sufficiently clear.

## 4. Opponent lock
When the user provides opponent descriptions or round-start timestamps:
- track the target/opponent pair together;
- use the opponent as a second identity constraint;
- reject a candidate subject if the pairing is inconsistent with the expected round.

## 5. Attribution gate
Before attributing any named move, sweep, pass, takedown, submission, tap, or major transition to the target:
- verify the target identity in a full-frame image immediately before or during that sequence;
- verify continuity into the sequence;
- only then use cropped/high-density frames for technical classification.

## 6. Complete-sequence technique naming
- Do not name a technique from the entry shape alone.
- Follow the full chain: entry -> control/isolation -> transition -> attack/counter -> endpoint.
- For submissions, verify the final head/limb configuration and finishing mechanics.
- Review the endpoint backward when uncertain.
- Use conventional technique names when supported.
- If the family is clear but the exact variation is not, say so explicitly.
- If the view is insufficient, mark the technique unresolved rather than guessing.

## 7. Dense frames for important exchanges
- Sparse contact sheets are navigation tools, not sufficient evidence for fine-grained technique identification.
- Use dense frames or the contiguous clip for submissions, sweeps, passes, reversals, takedowns, and ambiguous scrambles.

## 8. Contextual constraints
- Respect user-provided drill rules and starting positions.
- Do not grade an intentionally conceded starting position as a mistake.
- Account for deliberate intensity management, injuries, skill disparities, or control-only/submission-free rounds when the user provides that context.

## 9. Causal analysis
For each meaningful exchange, identify:
- starting position;
- target action;
- opponent response;
- target transition/counter;
- final position/finish;
- what mechanically caused success or failure;
- technical improvements;
- confidence in identity and technique label.

## 10. Uncertainty rule
When identity or technique confidence is insufficient, do not attribute the action to the target. Mark it as uncertain and continue from the next verified checkpoint.


## 11. Infer training intention before grading decisions
Training footage must not be interpreted like competition footage by default.
For each round or major phase, consider whether the target appears to be:
- conserving energy across many rounds;
- deliberately allowing a partner to work;
- experimenting with a specific position or technique;
- avoiding strength or explosiveness because of a skill/size disparity;
- protecting an injured partner;
- choosing not to pursue an available finish;
- fatigued;
- rolling playfully or at reduced intensity;
- deliberately entering bad positions to practice escapes or counters.

Use observable evidence such as pace, breathing, facial expression, repeated voluntary concessions, disparity in effort, speed changes at decisive moments, and whether the target repeatedly escapes without urgency. Treat inferred intention as probabilistic, not certain.

Do not call an omitted action a technical mistake merely because a higher-percentage competition action existed. First ask whether the athlete plausibly chose not to take it.

## 12. Prioritize specific mechanics over generic descriptions
General positional summaries are not enough when the footage supports more detail.
For important exchanges, inspect and report specific mechanics where visible, including:
- exact hand and wrist placement;
- elbow position and inside/outside control;
- head position;
- shoulder pressure and crossface direction;
- hip angle and weight distribution;
- knee line and foot position;
- frame location and frame quality;
- underhook/overhook depth;
- hook placement;
- grip transitions;
- posting hand/foot;
- direction of force;
- timing of weight transfer;
- which control point prevents or enables the next transition.

If a detail is partially obscured but reasonably inferable, label it explicitly as likely/may be happening. Never invent precise mechanics that are not visible.

## 13. Evaluate skill from effort asymmetry, not only outcomes
Training footage can reveal elite skill even when the athlete is not aggressively scoring or submitting.
When estimating level, consider:
- how relaxed the athlete remains under pressure;
- whether the opponent is visibly working harder;
- whether the athlete can repeatedly allow progress without becoming structurally compromised;
- efficiency of movement;
- absence of unnecessary muscular effort;
- speed and precision only when needed;
- ability to recover or reverse without panic;
- breadth of technically sound options across phases;
- how often the athlete appears to be controlling the difficulty of the exchange.

Do not underrate high-level grapplers simply because the footage lacks competitive urgency or because they permit positions that they could probably prevent.

## 14. Distinguish training-room footage from competition footage
Do not assume competition incentives in ordinary sparring.
Training may prioritize experimentation, partner safety, pacing, positional learning, entertainment, or selective practice over maximizing score/submission probability.
When footage appears to be training-room rolling, explicitly analyze both:
1. what would likely be optimal under competition incentives; and
2. what the athlete appears to be choosing under the actual training context.

The difference between those two is itself analytically important.


## 15. Full visual-verification protocol
Identity tracking is a prerequisite to technical analysis, not a parallel task. The following checks are mandatory.

### 15.1 Establish a canonical target reference
Before analyzing technique:
- save at least one full-frame reference where the target is unambiguous;
- record distinctive visual cues such as sleeve length, shirt/rashguard pattern, shorts/pants, hair, body proportions, and any user-provided location in frame;
- record the expected opponent for that segment when known;
- prefer several cues rather than relying on one feature alone.

A user-provided in-video anchor or external reference should remain the canonical reference for the entire analysis.

### 15.2 Track the person, not the most prominent pair
- Never assume the foreground, center, largest, or most visually salient pair contains the target.
- Before analyzing a new section, confirm that the target athlete is actually present in that pair.
- If another pair becomes more prominent while the target moves toward the edge or background, continue tracking the target rather than switching attention.
- If the target cannot be resolved confidently, stop attribution until the target is found again.

### 15.3 Preserve full-frame context
- Identity and continuity checks must use the uncropped frame.
- Cropping is permitted only after the target and opponent have been verified in the full frame.
- Do not use a crop to decide who the athlete is.
- Keep enough surrounding context to determine which pair is being followed and whether another nearby pair could be confused with them.

### 15.4 Check identity before every major exchange
Immediately before attributing a major action—submission, sweep, pass, takedown, reversal, back take, dominant pin, or prolonged defensive sequence:
- re-check the full frame;
- confirm target clothing/body cues;
- confirm opponent cues;
- confirm which athlete is top/bottom, standing/seated, or otherwise occupying the relevant orientation;
- then proceed to dense technical inspection.

Do not assume that an identity verified 30–60 seconds earlier remains sufficient through a complex scramble.

### 15.5 Re-check after every reversal, inversion, roll, or rotational scramble
Fast grappling can preserve the same pair while swapping which athlete is on top or which side of the frame they occupy.
After any:
- inversion;
- granby/rolling escape;
- sweep;
- reversal;
- rolling submission sequence;
- scramble around turtle;
- rotational takedown;
- off-camera transition;
re-confirm both:
1. which athlete is the target; and
2. the target's current positional role/orientation.

A correct pair identification is not enough if the two athletes have been swapped mentally.

### 15.6 Sleeve-length / clothing-role check when available
When two athletes wear similar colors, use structural clothing differences as high-priority cues.
Examples include:
- short sleeves vs long sleeves;
- rashguard panel pattern;
- shorts vs spats;
- distinctive logos/stripes;
- shoe/sock/knee-pad differences where visible.

If the user has specified a cue such as “short sleeves” or “purple lower half with gold/black/white upper half,” explicitly verify it again after ambiguous scrambles.

### 15.7 Cut detection and re-lock
Edited videos require a new identity lock after every visible cut, camera jump, angle change, replay, title card, or discontinuity.
After a cut:
- do not carry spatial assumptions across the edit;
- find the target again from canonical visual cues;
- find the expected opponent again;
- confirm the pair before resuming technique attribution.

### 15.8 Occlusion and off-camera handling
If the target:
- leaves frame;
- is hidden behind another pair/person;
- is only partially visible;
- becomes too small to distinguish;
- or is obscured during a decisive transition;
mark the identity track as interrupted.

Do not infer the outcome through the gap unless the post-occlusion re-entry makes the sequence unambiguous. When necessary, mark the technique or role swap as unresolved.

### 15.9 Pair continuity plus individual continuity
Use two simultaneous tracks:
- target identity;
- target-opponent pairing.

The expected opponent is a secondary constraint, not a substitute for target verification.
Reject a visual candidate if either:
- the target cues do not match; or
- the opponent/pairing is inconsistent with the known round.

### 15.10 Spatial continuity is supporting evidence only
Frame-to-frame movement and prior location can help track the athlete, but spatial continuity must not override contradictory visual cues.
A nearby athlete after a scramble or cut is not automatically the same person.

### 15.11 Orientation ledger for complex exchanges
For ambiguous or important sequences, maintain a simple mental/explicit ledger:
- timestamp;
- target side/location in frame;
- target clothing cue;
- opponent cue;
- target role: top/bottom/standing/turtle/back;
- confidence.

Update the ledger after every major positional swap.
This prevents the specific failure mode where the correct pair is followed but the athletes are mentally reversed.

### 15.12 Dense verification around taps and resets
A reset, disengagement, or apparent tap is not proof of who submitted whom.
For every apparent finish:
- verify target identity before the attack;
- verify target identity during the finishing mechanics;
- verify who taps/releases/resets;
- trace the finishing sequence backward if needed.

Never infer the submitter solely from who appears dominant in the final still frame.

### 15.13 Confidence threshold for attribution
Use three identity-confidence levels:
- High: target and opponent are both clearly verified and continuity is intact.
- Moderate: target likely verified, but one cue or transition is partially obscured.
- Low: identity, pairing, or top/bottom role is uncertain.

Only make definitive technical attribution at high confidence.
At moderate confidence, qualify the attribution.
At low confidence, do not assign the action to the target.

### 15.14 Do not repair identity gaps with technical plausibility
Never reason:
“this looks like something the target would do, therefore it must be the target.”
Technique style, skill level, body language, or expected strategy cannot substitute for visual identity evidence.

### 15.15 Correct visual attribution before interpreting intent
Intent analysis is downstream of identity.
Do not infer that the target is relaxed, conserving energy, allowing a position, or struggling until the athlete in that sequence has been visually verified.

### 15.16 Mandatory final consistency pass
Before delivering the final analysis:
- revisit every section containing a major claim;
- confirm the correct pair;
- confirm the target is not confused with the opponent;
- confirm top/bottom orientation after scrambles;
- confirm that no other foreground pair was accidentally analyzed;
- downgrade or remove any section that fails the check.

Visual attribution errors take priority over preserving a previously written interpretation.
