# Fight 4 — Verified Ultimate Timeline (~42:04–42:36)

Method:
- Rebuilt from the 4 fps fine-grained clip.
- Ultimate activation timing is based on HUD state transitions, checked against the fight visuals.
- Timing precision is approximately ±0.25 s.
- Do not infer order from sparse frames.

## Verified order

1. **Stalk3r — Doomfist Meteor Strike**
   - Activates between 42:06.25 and 42:06.50.
   - HUD shows Meteor Strike active from ~42:06.50 until ~42:14.50, then ult charge resets at ~42:14.75.
   - This is the FIRST ultimate in the sequence.

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
- Stalk3r is Doomfist, not Sojourn.
- Stalk3r uses Meteor Strike first.
- Sound Barrier comes second and occurs while Meteor Strike is active.
- Orbital Ray comes after Beat, while Meteor Strike is still active.
- Therefore the early response chain is:
  **Meteor Strike -> Sound Barrier -> Orbital Ray**
  not
  **Orbital Ray -> Sound Barrier**.

## Analysis rule reinforced
For every serious fight:
1. verify player hero identity,
2. build exact ult chronology from fine-grained footage,
3. mark which ults are direct responses,
4. record team spacing at each activation,
5. only then infer strategic intent.
