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


## Human adjudication — why Overclock distance matters
CR opens with **Stalk3r's Sojourn Overclock from far away**.

This creates a high-level decision problem for TM rather than an immediate forced fight:

### TM option A — kite
- Back away from Overclock.
- Potentially survive without spending a defensive ultimate.
- Cost: concede space / likely give CR point control.
- Consequence: TM must later retake from a worse objective position.

### TM option B — match with a defensive ultimate
- Use Sound Barrier / Transcendence-type resource to survive the enemy ult.
- General high-level principle: when countering an offensive ult with a defensive ult, the defending team often wants to **use the defensive ult to close distance and kill**, rather than merely absorb damage.
- If CR were already close, TM could Beat and immediately run them down.
- Because CR starts Overclock from far away, TM cannot automatically convert Beat into a kill; there is too much space.

### Key concept: uncertainty window
Using Overclock from range creates a **position of uncertainty** for TM:
- kite and give up space,
- or spend Beat without a guaranteed close-range punish.

This kind of uncertainty is common in high-level Overwatch and is a major reason exact ult order + team spacing at activation must be reconstructed accurately.

### Model lesson
Do not evaluate an ult only by whether it gets kills.
A ranged offensive ult can be valuable because it forces an opponent into a bad choice between:
- resource expenditure,
- positional concession,
- or objective loss.

When a defensive ult answers an offensive ult, always ask:
1. how far apart are the teams?
2. can the defending team use the defensive ult to close distance and threaten kills?
3. if not, is the defensive ult only buying survival while still conceding space?


## Human adjudication — why Orbital Ray gets little conversion
After CR opens with long-range Sojourn Overclock and TM answers with Sound Barrier, Vigilante uses Orbital Ray.

Key read:
- TM already has enough space to kite before Ray starts.
- Beat gives TM the temporary durability to survive CR's first pressure while continuing to retreat.
- Lucio speed and the existing distance let TM leave Ray's strongest fight area rather than stand and brawl inside it.
- Orbital Ray therefore wins CR space / point access, but does not force a kill.
- TM spreads and retreats away from the beam path rather than matching CR in the close fight Ray wants.
- CR's outside pressure does not make those retreat paths expensive enough; nobody is positioned well enough to catch TM where Ray is pushing them.

Useful abstraction:
> Ray becomes mostly a positional ult rather than a kill ult when the opponent has enough distance, speed, survivability, and retreat geometry to kite its path.

Important nuance:
- Pulse Bomb in the following phase is a relatively hit-or-miss ult and should not be overinterpreted.
- The important structural question is why a high-value ultimate like Orbital Ray failed to convert despite CR's pressure.

## Current Fight 4 understanding
1. Stalk3r opens with long-range Sojourn Overclock, creating an uncertainty choice for TM.
2. TM answers with Sound Barrier.
3. Because the teams are still far apart, TM cannot simply Beat and immediately kill CR; the distance preserves CR from that punishment.
4. Vigilante adds Orbital Ray.
5. TM kites the Ray using space + Beat durability + Lucio speed, conceding space but avoiding the close fight.
6. HeeSang's Pulse Bomb does not meaningfully decide the structural read.
7. MAX later uses Cage Fight to remove the remaining space.
8. TVNT answers with Annihilation in the now-compressed close-range fight.
9. Simple later reaches/uses Coalescence as another late resource layer.

Status: satisfactory for current training pass; deeper Cage/Annihilation inspection can resume later if useful.
