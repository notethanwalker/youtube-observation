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
