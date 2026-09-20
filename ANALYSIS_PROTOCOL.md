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
