# Capitology Fight-Analysis Training Session — 2026-10-05

## Purpose
This file preserves the key model corrections and accepted analysis patterns from the New Junk City fight-analysis training session.

## Core workflow rules learned

### 1. Corrections must be hero- and ult-aware
Do not generate corrections from abstract concepts alone. Always evaluate:
- exact hero capabilities,
- exact ult availability / near-availability,
- map geometry,
- staging,
- split assignments,
- pathing,
- resulting 1v1 / 4v4 or other local fight shapes.

### 2. Farming ultimates is conditional
"Farm ults" is not a universal delay rule.
It is correct only when:
- important ults are close enough to come online quickly,
- the team can safely deny a clean enemy engage,
- the future fight shape suits those ults,
- enemy ults do not improve even more from the delay.

Accepted New Junk City example:
CR could have denied TM a clean engage long enough to farm Mauga + Juno ult, then punish TM's forward walk with a close, stacked fight those ults strongly favor.

### 3. Simple player-error mode
Do not force every pro mistake into a deep tactical abstraction.
Procedure:
- briefly inspect how the mistake developed,
- if no meaningful setup/pathing/system cause exists, mark it as a simple player error and stop.

Accepted example:
Vigilante on Juno becomes far too split after CR rotates. Nothing meaningful appears to force this; this is primarily an individual pathing/rotation mistake.

### 4. Exact hero identification is mandatory
Hero identity must be verified before hero-specific reasoning.
Canonical icon reference:
- see `research/capitology-model/HERO_ICON_REFERENCE.md`
- direct HUD crop -> exact icon comparison -> high-confidence match only
- cross-check against lobby composition
- if uncertain, mark uncertain and stop hero-specific reasoning

Validated example:
Quartz = Sojourn.

### 5. Setup + ult = fight plan
Do not analyze staging in isolation from ultimate use.
Fight plans frequently depend on:
- setup geometry,
- intended target(s),
- target escape routes,
- ult timing,
- ult ordering,
- distance between teams.

### 6. Exact ult ordering is a hard prerequisite
For every serious fight:
1. verify all hero identities,
2. reconstruct exact chronological ult order from fine-grained footage,
3. identify which ults are direct responses,
4. note team spacing at each ult activation,
5. only then infer intent or correction.

Sparse-frame inference is not acceptable for chained ult sequences.

## Fight 3 (~39:00) accepted findings
CR plan:
- split setup,
- Vigilante Juno ult through main,
- side DPS collapse inward,
- intended to catch exposed point targets.

Failure:
- CR DPS did not scout escape routes well enough,
- did not block likely exits,
- Quartz (Sojourn) and Simple (Moira) escaped,
- TVNT read the split and pressured main early, making Juno ult more awkward/early.

Ideal structure:
split -> locate targets -> seal exits -> Juno ult -> collapse

Actual:
split -> incomplete scouting/exit control -> TVNT pressures main -> Juno ult under pressure -> targets escape -> collapse fails

Later phase:
The opening interaction mostly decides the fight.
CR is left awkward with weak follow-up resources; TM later uses Ramattra + Sojourn ult pressure and finds Bastion.
Possible full kite/re-engage or chance play exists, but both are low-percentage; do not overanalyze cleanup.

## Fight 4 (~42:08 onward) verified ult order
1. Stalk3r — Sojourn Overclock
2. FunnyAstro — Sound Barrier
3. Vigilante — Orbital Ray
4. HeeSang — Pulse Bomb
5. MAX — Cage Fight
6. TVNT — Annihilation
7. Simple — Coalescence

Important:
- Overclock starts from FAR AWAY.
- This creates a high-level uncertainty choice for TM:
  - kite and concede space/point,
  - or Beat and risk spending a defensive ult without being close enough to immediately kill CR.
- When a defensive ult answers an offensive ult, check whether the defending team is close enough to convert the defensive ult into aggression.

### Why Orbital Ray gets low value
- TM already has retreat space.
- Beat gives temporary durability.
- Lucio speed + distance allow TM to kite Ray instead of fighting inside it.
- CR wins space/point access, but not a kill.
- CR's side pressure does not sufficiently punish the retreat route.
- Therefore Ray becomes mostly a positional ult rather than a kill ult.

### Later ult interaction
- Pulse Bomb is high variance; do not overread it.
- Cage Fight later removes remaining space.
- TVNT's Annihilation comes after Cage compresses the fight and is especially strong in that close-range shape.
- Simple later gets Coalescence as a late resource layer.

## Analysis style
- Brief, player-usable wording.
- Use annotated pictures for critical concepts.
- Do not overcomplicate language.
- Treat every meaningful action as potentially important before pruning.
- Do not tunnel on similarity to the prior fight; each fight must be rebuilt from its own hero/ult/setup state.

## Confidence / truthfulness rule
Never state a low-confidence inference as fact.
If hero ID, ult order, or causal interpretation is uncertain:
- say so,
- verify,
- only then proceed.

