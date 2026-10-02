"""Curated Pass 9 rule index with checked links to source claims and visual reviews."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CLAIMS = {r["claim_id"]: r for r in map(json.loads, (ROOT / "pass04_claims.jsonl").open())}
VISUAL = {r["window_id"]: r for r in map(json.loads, (ROOT / "pass07_visual_ledger.jsonl").open())}
CLUSTERS = {r["cluster_id"] for r in json.loads((ROOT / "pass05_cluster_registry.json").read_text())["clusters"]}

# A rule describes the speaker's qualified advice. Confidence in the spoken
# interpretation is distinct from empirical confidence in its effectiveness.
RULES = [
    dict(id="CAP-01", title="A turn is a bounded opportunity", clusters=["C01_turns"],
         statement="A turn spends cooldowns or takes space for proactive value; first, second, and neutralizing turns describe timing, not a complete plan.",
         trigger="Before a team commits resources or chooses to wait for the opponent.",
         action="Name the specific space, cooldown, target, or response the turn should gain, and the next move if it does not finish the fight.",
         exception="A first turn can be soft pressure rather than an all-team engage; a role window may be smaller than a team turn.",
         claims=["P4-005", "P4-006", "P4-033", "P4-081", "P4-109"], visual=["V6-01", "V6-03"], tags=["turn", "tempo", "initiative"], evidence="sampled_visual"),
    dict(id="CAP-02", title="Preserve a useful next response", clusters=["C01_turns", "C06_bait"],
         statement="The first exchange should create or retain an answer to the opponent's likely reply; inducing a cooldown alone does not win the fight.",
         trigger="After pressure forces an enemy cooldown, rotation, or ultimate.",
         action="Check whether the team has distance, angle, resources, and time to punish the actual response; delay commitment to stack advantages when needed.",
         exception="A fast finish can be correct when the response is already exposed; the opponent may decline the offered route.",
         claims=["P4-008", "P4-015", "P4-035", "P4-118", "P4-199", "P4-206"], visual=["V6-02", "V6-04", "V6-17", "V6-18"], tags=["turn", "bait", "counterplay", "cooldown"], evidence="sampled_visual"),
    dict(id="CAP-03", title="Know the opponent's reach", clusters=["C03_geometry"],
         statement="Entering the opponent's effective engage range without a route and reply can force resources merely to survive.",
         trigger="Walking through a choke, corner, or staging lane toward an enemy setup.",
         action="Scout the pocket, identify the threatened angle and available counter, and cross when a chosen threat can be made.",
         exception="The pocket depends on hero, cooldown, sight line, and objective; distance alone is not the rule.",
         claims=["P4-009", "P4-075", "P4-076", "P4-162", "P4-163"], visual=["V6-06"], tags=["space", "corner", "reach", "walkup"], evidence="illustrative_visual"),
    dict(id="CAP-04", title="Reset before displacement becomes forced", clusters=["C03_geometry", "C01_turns"],
         statement="An early voluntary pull with cooldowns and map distance can preserve a later initiation; backing away only after an enemy finishes staging may surrender the next corner too.",
         trigger="A planned push is blocked or the current fight location is unfavorable.",
         action="Leave before pursuit closes, use cover or a new route to conceal the next fight, and decide where to re-engage.",
         exception="Do not give a critical corner or objective for free when the team can contest the enemy setup; a late forced retreat is a different action.",
         claims=["P4-021", "P4-030", "P4-031", "P4-032", "P4-133", "P4-200"], visual=["V6-05", "V6-06", "V6-07"], tags=["retreat", "reset", "space", "corner"], evidence="sampled_visual"),
    dict(id="CAP-05", title="Scout, then conceal", clusters=["C02_information"],
         statement="Safe forward sight can reveal the opponent's approach before the team withdraws to a less visible final setup.",
         trigger="Between fights, before choosing a defensive or attacking route.",
         action="Gather sight without sacrificing survival; communicate the route, then hide the final positioning or timing.",
         exception="Do not equate a single player's view with the entire team's knowledge; the scouting position itself can be punishable.",
         claims=["P4-019", "P4-020", "P4-132", "P4-183"], visual=[], tags=["scouting", "information", "concealment"], evidence="transcript_only"),
    dict(id="CAP-06", title="Prevent a strong dive before surviving it", clusters=["C05_setup", "C13_support"],
         statement="A completed, well-staged dive is hard to answer by support cooldown execution alone; the defense can contest the DPS angle, tank route, or approach first.",
         trigger="An enemy dive is assembling a short jump and supporting angles.",
         action="Clear or displace staging, rotate wide, or use a timely defensive ultimate if it prevents the setup from maturing.",
         exception="This is not a claim that every dive kills or that an early ultimate is always optimal; matchup and remaining threats matter.",
         claims=["P4-016", "P4-017", "P4-018", "P4-134", "P4-171", "P4-175"], visual=["V6-12", "V6-13", "V6-14", "V6-15"], tags=["dive", "staging", "support", "defense"], evidence="sampled_visual"),
    dict(id="CAP-07", title="Match damage timing to the tank window", clusters=["C05_setup", "C11_tank", "C12_dps"],
         statement="A tank entry creates only a short opportunity if damage players have not staged a matching sight line or burst route.",
         trigger="Planning a jump, clearing move, nano dive, or short burst engage.",
         action="Establish the damage angle and support path before the tank spends the entry resource; synchronize follow-up to its actual window.",
         exception="A soft tank move may deliberately seek information or cooldowns rather than an immediate kill.",
         claims=["P4-064", "P4-145", "P4-170", "P4-180"], visual=[], tags=["dive", "tank", "dps", "timing"], evidence="transcript_only"),
    dict(id="CAP-08", title="Bait needs a punish and a fallback", clusters=["C06_bait"],
         statement="Offering a cooldown, player, or lane can shape an opponent's choice only if the offer is credible and the baiting side can survive and answer it.",
         trigger="A team intends to play second or lure an engage.",
         action="State the desired enemy action, the cost of the offer, the counter, and a response if the opponent clears a different lane.",
         exception="The first mover may correctly accept the bait and win; a passive kite with no counterpressure is not enough.",
         claims=["P4-015", "P4-034", "P4-035", "P4-054", "P4-125", "P4-199"], visual=["V6-03", "V6-16", "V6-17", "V6-18", "V6-19"], tags=["bait", "playing second", "counterpressure"], evidence="sampled_visual"),
    dict(id="CAP-09", title="Use objective pressure to force a choice", clusters=["C10_objective", "C01_turns"],
         statement="Cart or point pressure can create an enemy response that opens an angle or later turn, but occupying objective is not automatically the best fight location.",
         trigger="A retake or attack stalls against a strong hold.",
         action="Choose whether touching, threatening a route, or clearing an exit makes the defender move; set up the fight that follows the touch.",
         exception="A panic flip without defensible angles or follow-up may leave the team worse off.",
         claims=["P4-007", "P4-038", "P4-153", "P4-154", "P4-177"], visual=["V6-01", "V6-11"], tags=["objective", "retake", "cart", "point"], evidence="sampled_visual"),
    dict(id="CAP-10", title="Split cores trade attention", clusters=["C04_splits"],
         statement="When one group is pressured, it yields while another creates timely angle, cooldown, kill, or objective value.",
         trigger="Playing a composition with two or more viable pressure groups.",
         action="Keep groups near enough to counterpressure, identify who carries attention, and communicate when to yield or re-enter.",
         exception="Advancing both pressured groups at once can discard the exchange; excessive separation makes the reply late.",
         claims=["P4-001", "P4-003", "P4-004", "P4-104", "P4-107", "P4-091"], visual=["V6-20", "V6-21", "V6-22"], tags=["split", "off angle", "attention", "push pull"], evidence="sampled_visual"),
    dict(id="CAP-11", title="Delay a predictable split", clusters=["C04_splits", "C09_compositions"],
         statement="A split may begin grouped when an opponent can instantly clear an obvious outside lane, then form after the clear commits.",
         trigger="An enemy teleport, D.Va, or fast rotation threatens a pre-shown off angle.",
         action="Scout the clear, protect the first pressured group, and separate when the opponent's movement exposes a second lane.",
         exception="This is a matchup adaptation, not a rule to retake as five in every split composition.",
         claims=["P4-105", "P4-143", "P4-144", "P4-193"], visual=["V6-23"], tags=["split", "teleport", "retake", "adaptation"], evidence="sampled_visual"),
    dict(id="CAP-12", title="Evaluate ultimate spend by conversion", clusters=["C08_ultimates", "C10_objective"],
         statement="Ult count matters through the fight it wins, the objective state, the following setup, and the charge recovered, not as inventory alone.",
         trigger="Choosing whether to combine ultimates or judging an apparent over-spend.",
         action="Check whether the expenditure secures the fight or denies a severe retake loss, and whether the team can hold useful angles afterward.",
         exception="A triple spend for a panic point flip can be genuine waste. The broader OW1/OW2 era comparison remains untested.",
         claims=["P4-026", "P4-029", "P4-036", "P4-038", "P4-053", "P4-198"], visual=["V6-08", "V6-10", "V6-11"], tags=["ultimate", "economy", "objective", "conversion"], evidence="sampled_visual"),
    dict(id="CAP-13", title="Economy exceptions depend on composition", clusters=["C08_ultimates", "C09_compositions"],
         statement="Some compositions and matchups depend strongly on ultimate cycles or a particular defensive answer even when a generic inventory heuristic is weak.",
         trigger="A plan relies on a named ultimate interaction, teleport cycle, or near-charged defensive tool.",
         action="Plan the neutral and ultimate fights separately; farm or preserve the specific answer before committing when required.",
         exception="The claim that economy is generally less decisive in OW2 than OW1 is an attributed thesis, not a measured fact in this corpus.",
         claims=["P4-026", "P4-086", "P4-117", "P4-147", "P4-158"], visual=["V6-09"], tags=["ultimate", "composition", "matchup"], evidence="illustrative_visual"),
    dict(id="CAP-14", title="Size a window to the role that can use it", clusters=["C07_windows", "C01_turns"],
         statement="A missing cooldown can permit a tank step, DPS angle, or distant support contribution without authorizing the whole team to walk into reach.",
         trigger="A brief resource or position advantage appears.",
         action="Identify which player can profit within the window and who should retain an offset position.",
         exception="A coordinated full engage is justified when the opening and follow-up actually support it.",
         claims=["P4-081", "P4-082", "P4-155", "P4-164", "P4-187"], visual=[], tags=["cooldown", "role", "window", "backline"], evidence="transcript_only"),
    dict(id="CAP-15", title="Tank resources shape the next exchange", clusters=["C11_tank"],
         statement="Armor, ammunition, defensive abilities, and a safe exit affect whether a tank's entry remains threatening after the first contact.",
         trigger="A tank is about to commit movement or an ultimate.",
         action="Restore or reserve the resource that sustains the midfight; place the engage for the team's intended follow-up.",
         exception="Mauga, Hazard, Winston, and Ball examples are hero- and patch-specific; do not transfer their micro literally to every tank.",
         claims=["P4-046", "P4-047", "P4-048", "P4-065", "P4-066", "P4-127"], visual=[], tags=["tank", "resource", "engage", "armor"], evidence="transcript_only"),
    dict(id="CAP-16", title="A damage angle must pressure and survive", clusters=["C12_dps", "C03_geometry"],
         statement="An angle too far back removes pressure; one inside easy enemy reach becomes the next trade.",
         trigger="A hitscan or other damage player chooses a pre-fight angle or withdrawal path.",
         action="Keep useful sight on the walk-up and a route to leave before the enemy clear reaches the position.",
         exception="Do not force a flank when it adds no sight line; the 2024 hitscan ASR is garbled and requires audio for fine hero-specific claims.",
         claims=["P4-044", "P4-045", "P4-073", "P4-074", "P4-108", "P4-192"], visual=[], tags=["dps", "hitscan", "angle", "position"], evidence="transcript_only"),
    dict(id="CAP-17", title="Preserve a flex DPS exit and re-entry", clusters=["C12_dps", "C14_execution"],
         statement="Drawing attention without dying can create value; leaving before a forced clear allows a later angle or burst window.",
         trigger="An off-angle DPS is marked or several opponents turn toward them.",
         action="Use movement and an ally route to leave early, contribute from a safer angle, then re-enter when the clearer spends resources or retreats.",
         exception="An available ultimate or flank is not automatically better than the current neutral pressure.",
         claims=["P4-012", "P4-067", "P4-068", "P4-111", "P4-112", "P4-140"], visual=[], tags=["dps", "genji", "attention", "exit"], evidence="transcript_only"),
    dict(id="CAP-18", title="Support escape is a team setup", clusters=["C13_support"],
         statement="A support escape route or teleport destination should be planned before the first diver forces movement, while preserving useful midfight sight.",
         trigger="An enemy dive can reach the backline or the team prepares to flip map.",
         action="Position teammates and an offset support to provide a safe destination and early warning.",
         exception="Specific Kiriko–Lucio and Brigitte interactions are composition-specific; survival without contribution is not the goal.",
         claims=["P4-049", "P4-059", "P4-123", "P4-124", "P4-175", "P4-179", "P4-188"], visual=["V6-15"], tags=["support", "escape", "teleport", "peel"], evidence="illustrative_visual"),
    dict(id="CAP-19", title="Matchups require repeated answers", clusters=["C09_compositions"],
         statement="A counter composition must answer the opponent's recurring setup cycles, not merely the first teleport or engage.",
         trigger="Drafting or adapting against a composition with repeatable movement or cooldown threats.",
         action="Compare neutral and ultimate fights, staging routes, repeated denial, and the resources each player needs.",
         exception="A tournament-winning lineup or one lost fight does not establish a universally best composition.",
         claims=["P4-058", "P4-070", "P4-071", "P4-072", "P4-080", "P4-204"], visual=[], tags=["composition", "matchup", "teleport", "draft"], evidence="transcript_only"),
    dict(id="CAP-20", title="Retake routes are fight plans", clusters=["C10_objective", "C05_setup"],
         statement="A retake route should remove a dangerous setup or threaten a useful exit rather than automatically walk straight onto objective.",
         trigger="The defending team controls a room, choke, side lane, or pre-staged dive.",
         action="Choose a route with enough team support to establish the needed side, then time the touch to the resulting fight.",
         exception="A small unsupported split can be cleared before it creates pressure; clock state may force an earlier touch.",
         claims=["P4-018", "P4-153", "P4-154", "P4-161", "P4-165", "P4-177"], visual=["V6-13"], tags=["retake", "route", "objective", "setup"], evidence="illustrative_visual"),
    dict(id="CAP-21", title="Execution and attention limit a correct plan", clusters=["C14_execution", "C15_learning"],
         statement="A sound setup can lose to missed shots, delayed attention, or failure to execute a known interaction under match pressure.",
         trigger="Reviewing a lost fight whose pre-fight plan appears plausible.",
         action="Separate setup, information, target choice, mechanics, and attention at the moment of decision before rewriting the entire plan.",
         exception="Do not use mechanics as an unfalsifiable excuse for a weak setup; outcome alone does not identify the cause.",
         claims=["P4-022", "P4-023", "P4-088", "P4-096", "P4-150", "P4-156"], visual=[], tags=["execution", "attention", "mechanics", "review"], evidence="transcript_only"),
    dict(id="CAP-22", title="Train observation and narrow actions", clusters=["C15_learning"],
         statement="Replay study should reconstruct what a player could know, compare similar situations, and practice one or two specific in-game attention tasks.",
         trigger="A player knows a concept in review but cannot execute it reliably.",
         action="Write the observed sequence, state a tentative reading, compare a closely matched pro example, and rehearse a small concrete cue.",
         exception="These are coaching recommendations, not measured proof that a training method improves rank.",
         claims=["P4-022", "P4-023", "P4-040", "P4-041", "P4-042", "P4-097", "P4-098"], visual=[], tags=["coaching", "learning", "replay", "practice"], evidence="transcript_only"),
    dict(id="CAP-23", title="Aim uses prediction and context", clusters=["C12_dps"],
         statement="Anticipating a likely strafe or holding a well-placed crosshair can be more consistent than chasing every movement, but over-waiting gives the opponent time to shoot.",
         trigger="Reviewing a hitscan duel or repeated missed follow-up shots.",
         action="Read the opponent's short or long strafe and choose whether to follow, cut off, or wait for a return.",
         exception="This is not a replacement for aim mechanics or a universal instruction to stop moving the cursor.",
         claims=["P4-078", "P4-079", "P4-129", "P4-151", "P4-152"], visual=[], tags=["aim", "hitscan", "duel", "mechanics"], evidence="transcript_only"),
    dict(id="CAP-24", title="Keep design opinions separate", clusters=["C16_design"],
         statement="Balance preferences and pre-release hero predictions express a design philosophy; they are not match evidence for a particular tactical rule.",
         trigger="Using commentary about viability, counterplay, or hero tuning to justify gameplay advice.",
         action="Label the statement as opinion or prediction and seek actual match examples before inferring a tactical consequence.",
         exception="A design view can still motivate a testable hypothesis; do not silently promote it to observation.",
         claims=["P4-077", "P4-099", "P4-159", "P4-160", "P4-201"], visual=[], tags=["design", "balance", "scope"], evidence="transcript_only"),
]

assert len(RULES) == len({r["id"] for r in RULES})
assert set().union(*(set(r["clusters"]) for r in RULES)) == CLUSTERS
for rule in RULES:
    assert rule["claims"] and all(cid in CLAIMS for cid in rule["claims"]), rule["id"]
    assert all(wid in VISUAL for wid in rule["visual"]), rule["id"]
    assert all(c in CLUSTERS for c in rule["clusters"]), rule["id"]
    rule["sources"] = [{"claim_id": cid, "url": CLAIMS[cid]["url"],
                        "upload_date": CLAIMS[cid]["upload_date"]} for cid in rule.pop("claims")]
    rule["visual_window_ids"] = rule.pop("visual")
    rule["confidence"] = {"speaker_model": "moderate" if rule["evidence"] == "transcript_only" else "moderate_to_high",
                          "general_gameplay_effectiveness": "not_established"}

out = ROOT / "pass09_rules.json"
out.write_text(json.dumps({"status": "provisional_synthesis", "rule_count": len(RULES),
                           "rules": RULES}, indent=2, ensure_ascii=False) + "\n")

SECTIONS = [
    ("Core decision model", ["CAP-01", "CAP-02", "CAP-08", "CAP-09", "CAP-14"]),
    ("Space, information, and setup", ["CAP-03", "CAP-04", "CAP-05", "CAP-06", "CAP-20"]),
    ("Split compositions and adaptations", ["CAP-10", "CAP-11", "CAP-19"]),
    ("Resources and ultimate economy", ["CAP-12", "CAP-13", "CAP-15"]),
    ("Role-specific execution", ["CAP-07", "CAP-16", "CAP-17", "CAP-18", "CAP-23"]),
    ("Learning, attention, and scope", ["CAP-21", "CAP-22", "CAP-24"]),
]
section_ids = [rid for _, ids in SECTIONS for rid in ids]
assert len(section_ids) == len(RULES) and set(section_ids) == {r["id"] for r in RULES}
by_id = {r["id"]: r for r in RULES}
lines = [
    "# Capitology's Overwatch model — provisional synthesis",
    "",
    "This reconstructs the speaker's stated decision framework from 54 known uploads, 206 selected caption-grounded claims, 16 clusters, 23 selectively reviewed video windows, and ten Pass 8 adjudications. The 24 rules below cite 120 distinct claim anchors. They are conditional coaching hypotheses, not measured laws or a claim that the selected fights prove causation.",
    "",
    "**How to use it in a match review:** establish player/POV and observable fight state first; identify which rule's trigger actually occurred; compare the observed action and response with its conditional alternative; report the exception and uncertainty. A bad outcome alone is not proof of a bad choice. The machine-readable companion is `pass09_rules.json`.",
    "",
    "## Vocabulary and evidence", "",
    "- **Turn:** a bounded opportunity to spend resources or space proactively. First/second describes timing, not a full fight instruction.",
    "- **Pocket / reach:** the map region where the opponent can initiate an effective hit, varying by heroes, resources, and sight lines.",
    "- **Staging:** the route, angles, information, and resources set before a decisive engage.",
    "- **Split / core:** separated pressure groups that can exchange enemy attention and counterpressure; their exact formation depends on matchup.",
    "- **Evidence tags:** `sampled_visual` means selected edited 480p windows were inspected; `illustrative_visual` means mostly diagrams or limited POV; `transcript_only` means no selected visual test. None means full replay validation. Speaker-model confidence and gameplay effectiveness are separate.",
    "",
    "## Candidate unifying structure", "",
    "A team uses space, sight, objective pressure, and resource timing to change the opponent's available responses, then needs a useful answer to the actual response. This connects turns, bait, retreat, dive prevention, splits, and ultimate conversion. It is a synthesis of selected explanations, not a universal rule or a substitute for mechanics, role duties, matchup, and objective clock.",
    "",
]
for heading, ids in SECTIONS:
    lines += [f"## {heading}", ""]
    for rid in ids:
        r = by_id[rid]
        anchors = ", ".join(f"[{s['claim_id']}]({s['url']})" for s in r["sources"])
        windows = ", ".join(r["visual_window_ids"]) or "no selected visual window"
        lines += [f"### {rid} — {r['title']}", "", r["statement"], "",
                  f"**When:** {r['trigger']} **Action:** {r['action']}", "",
                  f"**Boundary:** {r['exception']}", "",
                  f"**Evidence:** {anchors}. Visual: {windows}. Level: `{r['evidence']}`.", ""]
lines += [
    "## Contradictions, evolution, and limits", "",
    "Pass 8 found no direct unconditional reversal among its ten priority comparisons. Later accounts generally add conditions: a voluntary reset differs from forced retreat; bait can be accepted or bypassed; a temporarily grouped start can precede a split; and ultimate inventory matters through the fight and resulting setup. The April 2026 follow-up explicitly calls one triple spend wasteful while maintaining that other multi-ultimate wins can be rational. See `PASS08_CONTRADICTION_EVOLUTION_REPORT.md` and `pass08_adjudications.jsonl` for the dated comparisons.",
    "",
    "The assertion that ultimate economy generally became less decisive from Overwatch 1 to Overwatch 2 is attributable to the speaker but remains an unmeasured empirical comparison. Edited coaching videos, automatic captions, and 480p sampled windows cannot establish every player belief, cooldown order, complete fight outcome, or counterfactual. The 2024 hitscan and September 2026 guest transcripts are particularly garbled; verify audio before relying on fine attribution. Upload dates are not match dates. Design opinions and pre-release predictions are kept separate from match evidence.",
    "",
    "## Evidence index and next validation", "",
    "- `pass09_rules.json`: every rule, trigger, action, exception, cluster membership, source URLs/dates, visual window IDs, and evidence level.",
    "- `pass04_claims.jsonl`, `pass05_concept_index.csv`, `pass07_visual_ledger.jsonl`, and `pass08_adjudications.jsonl`: underlying claims, mappings, sampled observations, and tensions.",
    "- `MATCH_REVIEW_PROTOTYPE.md`: apply these rules to a new player's complete match only after observing the recording; do not match a rule from the final score or an isolated still.",
    "",
]
(ROOT / "model.md").write_text("\n".join(lines), encoding="utf-8")
print(len(RULES), "rules covering", len(CLUSTERS), "clusters and",
      len({s["claim_id"] for r in RULES for s in r["sources"]}), "distinct source claims")
