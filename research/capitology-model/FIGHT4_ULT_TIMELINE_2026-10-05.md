# Fight 4 — Verified Ultimate Timeline (~42:04–42:36)

Method:
- Rebuilt from the 4 fps fine-grained clip.
- Ultimate activation timing is based on HUD state transitions, checked against the fight visuals.
- Timing precision is approximately ±0.25 s.
- Do not infer order from sparse frames.

## Verified order

1. **Stalk3r — Sojourn Overclock**
   - Activates first, around ~42:06.5.
   - This is the FIRST ultimate in the sequence.
   - Prior identification of Stalk3r as Doomfist was incorrect.

2. **FunnyAstro — Lucio Sound Barrier**
   - Activates between 42:07.75 and 42:08.00.
   - This occurs while Stalk3r is already in Meteor Strike.
   - Strong working interpretation: Beat is a direct defensive response to the incoming Meteor Strike / CR first engage.
   - Teams still have meaningful space between them at this point.

3. **Vigilante — Juno Orbital Ray**
   - Activates between 42:12.00 and 42:12.50, best estimate ~42:12.25.
   - This is used while Meteor Strike is still active and CR is still closing distance.
   - Important: Orbital Ray is NOT the first ult, and Beat is NOT a response to Orbital Ray.

4. **HeeSang — Tracer Pulse Bomb**
   - Activates between 42:21.00 and 42:21.50, best estimate ~42:21.5.
   - Ult charge resets by ~42:22.5.

5. **MAX — Mauga Cage Fight**
   - Activates between 42:23.00 and 42:23.50, best estimate ~42:23.5.
   - Cage remains active until roughly 42:30.0–42:30.5.

6. **TVNT — Ramattra Annihilation**
   - Activates between 42:26.00 and 42:26.50, best estimate ~42:26.5.
   - This is after Cage Fight begins.
   - Strong working interpretation: Annihilation is a response to the close-range fight shape created by Cage.

7. **Simple — Moira Coalescence**
   - Reaches 100% around 42:33.5.
   - Activates around 42:34.0.
   - This is a late-fight resource, not part of the initial ult exchange.

## Ults NOT used in this verified window
- Chorong reaches Rally around 42:31.5 but does not use it in the checked window.
- Quartz does not reach/use Overclock in this sequence.
- Youbi reaches Pulse Bomb only late and does not use it in the checked window.

## Critical corrections to prior analysis
- Stalk3r is Sojourn.
- Stalk3r uses Overclock first.
- Sound Barrier comes second and is best read as TM's response to the incoming Sojourn Overclock / first engage.
- Orbital Ray comes after Beat.
- Therefore the early response chain is:
  **Overclock -> Sound Barrier -> Orbital Ray**
  not
  **Orbital Ray -> Sound Barrier**.

## Analysis rule reinforced
For every serious fight:
1. verify player hero identity,
2. build exact ult chronology from fine-grained footage,
3. mark which ults are direct responses,
4. record team spacing at each activation,
5. only then infer strategic intent.


## Critical model-safety correction
A prior pass confused Stalk3r's Sojourn with Doomfist. This is not an acceptable hero-identification failure mode, especially where visual identity cues could be conflated with race or skin tone.

Required safeguard:
- Never infer hero identity from a player's appearance, skin tone, or vague facial resemblance.
- Hero identity must come from direct HUD-icon matching against the canonical hero-icon reference set, plus cross-checking against the lobby composition when available.
- If icon confidence is not high, mark identity uncertain and do not do hero-specific reasoning.
- Composition consistency check: if a claimed hero does not exist in the observed lobby, treat that as a hard contradiction and re-verify before continuing.
