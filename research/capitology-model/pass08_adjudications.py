"""Build the manually adjudicated Pass 8 ledger with source provenance checks."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CLAIMS = {c["claim_id"]: c for c in map(json.loads, (ROOT / "pass04_claims.jsonl").open())}
VISUAL = {v["window_id"]: v for v in map(json.loads, (ROOT / "pass07_visual_ledger.jsonl").open())}
QUEUE = {q["window_id"]: q for q in csv.DictReader((ROOT / "pass06_retrieval_queue.csv").open())}

# Classifications concern the speaker's stated model, not whether its match
# diagnosis is true. An open test never inherits certainty from an illustration.
CASES = [
    dict(id="P8-01", question="Does the later criticism of first/second turns retract the 2023 definition?",
         claims=["P4-005", "P4-007", "P4-014", "P4-033", "P4-035", "P4-206"], windows=["V6-01", "V6-02", "V6-03", "V6-04"],
         classification="elaboration_not_retraction", confidence="moderate_for_spoken_relationship",
         finding="A turn remains an opportunity for proactive value. The 2026 criticism targets first/second as instructions without a plan for opponent choices; it adds delayed rotations and counterplay rather than retracting the earlier vocabulary.",
         open_test="The edited examples cannot establish that any first move forced a specific enemy belief or every cooldown exchange."),
    dict(id="P8-02", question="Does backing up to go forward conflict with fighting the setup?",
         claims=["P4-021", "P4-133", "P4-030", "P4-031", "P4-032", "P4-039", "P4-200"], windows=["V6-05", "V6-06", "V6-07"],
         classification="conditional_distinction", confidence="moderate_for_spoken_relationship_limited_visual",
         finding="He rejects a retreat forced after the opponent has angles and reach, while recommending an early voluntary reset that retains distance, cooldowns, concealment, and a later fight location. The 2026 video explicitly contrasts its advice with the earlier example.",
         open_test="V6-05 ends before the losing sequence, and V6-07 does not verify the eventual win; exact distances and pursuit require a fuller replay."),
    dict(id="P8-03", question="Does the ultimate-economy thesis rule out multi-ultimate fight plans?",
         claims=["P4-053", "P4-117", "P4-147", "P4-158", "P4-026", "P4-027", "P4-029", "P4-036", "P4-038", "P4-198"], windows=["V6-08", "V6-09", "V6-10", "V6-11"],
         classification="qualified_thesis_and_example_correction", confidence="high_for_spoken_scope_limited_visual",
         finding="The title overstates the spoken thesis: economy still matters, especially in named compositions. Spending two or three to secure a consequential retake is consistent with that view. The April follow-up concedes one triple spend was waste while distinguishing another failure of position and conversion after spending.",
         open_test="The claimed OW1-to-OW2 change in relative explanatory weight is unmeasured here; V6-08 omits the prior full spend and V6-11 does not yield reliable exact HUD counts."),
    dict(id="P8-04", question="Does proactive setup denial contradict defensive survival or ultimate conservation?",
         claims=["P4-016", "P4-017", "P4-018", "P4-134", "P4-171", "P4-175", "P4-147"], windows=["V6-12", "V6-13", "V6-14", "V6-15"],
         classification="phase_and_matchup_distinction", confidence="moderate_for_spoken_relationship_limited_visual",
         finding="The claim that a completed good dive is hard to survive motivates acting before setup is complete. A wide clear or early defensive ultimate is one option, while conserving or layering ultimates remains sensible when the team can preserve a useful answer to later threats.",
         open_test="The earlier-Rally choice is counterfactual, and a single edited POV cannot establish the whole team's information or a universal optimal response."),
    dict(id="P8-05", question="Can playing second or baiting coexist with attacking first when surrounded?",
         claims=["P4-015", "P4-054", "P4-034", "P4-035", "P4-199", "P4-206", "P4-189", "P4-190"], windows=["V6-03", "V6-04", "V6-16", "V6-17", "V6-18", "V6-19"],
         classification="conditional_failure_boundary", confidence="moderate_for_spoken_relationship_limited_visual",
         finding="A credible offer must preserve counterpressure and enough resources for a second move. The opponent can accept it, clear the offered player, or use another route. A later guest discussion raises initiating before a pinch completes as a plausible limit, but it is not decisive evidence of Capitology's own rule.",
         open_test="V6-17 overlaps V6-04 and is not another match; the September guest transcript is garbled, so P4-189/190 need audio before attributing each statement."),
    dict(id="P8-06", question="Does a grouped start contradict the earlier rule to retake with split cores?",
         claims=["P4-001", "P4-003", "P4-004", "P4-104", "P4-105", "P4-143", "P4-144", "P4-091", "P4-193"], windows=["V6-20", "V6-21", "V6-22", "V6-23"],
         classification="matchup_specific_adaptation_with_common_mechanism", confidence="moderate_for_spoken_relationship_limited_visual",
         finding="The 2023 lesson requires timely counterpressure from separated cores. The 2026 example delays the initial split specifically against a fast teleport/D.Va clear, then separates after the clear commits. Repeated attention exchange extends the earlier push/pull account; identical tactics across eras or compositions are not established.",
         open_test="Two windows are mostly static diagrams; V6-21 and V6-23 do not show complete outcomes or all five starting positions."),
    dict(id="P8-07", question="Does forward scouting conflict with hiding the final setup?",
         claims=["P4-183", "P4-019", "P4-020", "P4-132"], windows=[],
         classification="sequential_phases", confidence="moderate_for_spoken_relationship_only",
         finding="A team may show briefly to learn the walk-up, then withdraw and hide the final position. Broad sight and concealment occur at different moments; the claims do not instruct simultaneous exposure and hiding.",
         open_test="No selected visual window independently verifies information held by both teams in these examples."),
    dict(id="P8-08", question="Must a damage player take an early angle or delay the obvious flank?",
         claims=["P4-073", "P4-074", "P4-083", "P4-084", "P4-089", "P4-192"], windows=[],
         classification="visibility_and_timing_condition", confidence="moderate_for_spoken_relationship_only",
         finding="The early-angle advice concerns being useful before an intended early fight. Delaying an obvious flank or shot can preserve surprise when the position would otherwise be pre-cleared or its sight line adds nothing. There is no fixed flank quota in the later account.",
         open_test="The ledger has no paired visual test of these DPS choices; P4-192 includes guest speech and needs careful attribution."),
    dict(id="P8-09", question="Do proactive defensive ultimates conflict with holding them for later threats?",
         claims=["P4-134", "P4-158", "P4-171", "P4-175", "P4-147", "P4-176"], windows=["V6-14", "V6-15"],
         classification="resource_sequence_condition", confidence="moderate_for_spoken_relationship_limited_visual",
         finding="Spending early to prevent a nearly finished setup and saving an ultimate after a successful kite answer different threat sequences. The shared question is whether the resource preserves a usable fight and next response, not whether earlier or later is intrinsically best.",
         open_test="The optimal counterfactual spend and exact ability order are not established by the sampled, single-POV footage."),
    dict(id="P8-10", question="Did ultimate economy become generally less decisive from OW1 to OW2?",
         claims=["P4-026", "P4-027", "P4-028", "P4-029", "P4-036"], windows=["V6-08", "V6-09"],
         classification="unresolved_empirical_comparison", confidence="high_for_speaker_attribution_low_for_empirical_test",
         finding="The speaker explicitly proposes an era-level difference, with composition exceptions. The selected clips illustrate possible mechanisms but do not estimate the relative contribution of ultimate inventory to wins across eras.",
         open_test="A controlled, patch-aware set of comparable fights or a clearly defined quantitative measure is needed; the juxtaposed OW1/OW2 footage changes teams and metas."),
]

seen = set()
for case in CASES:
    assert case["id"] not in seen
    seen.add(case["id"])
    assert len(case["claims"]) == len(set(case["claims"]))
    assert len(case["windows"]) == len(set(case["windows"]))
    for cid in case["claims"]:
        assert cid in CLAIMS, (case["id"], cid)
    for wid in case["windows"]:
        assert wid in VISUAL and wid in QUEUE, (case["id"], wid)
    case["source_claims"] = [
        {k: CLAIMS[cid][k] for k in ("claim_id", "video_id", "upload_date", "start", "end", "url")}
        for cid in case.pop("claims")
    ]
    case["visual_sources"] = [
        {"window_id": wid, "video_id": QUEUE[wid]["video_id"], "url": QUEUE[wid]["url"],
         "review_status": VISUAL[wid]["review_status"]} for wid in case.pop("windows")
    ]

out = ROOT / "pass08_adjudications.jsonl"
out.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in CASES))
print(len(CASES), "adjudications;", len({s["claim_id"] for c in CASES for s in c["source_claims"]}),
      "unique claims;", len({s["window_id"] for c in CASES for s in c["visual_sources"]}), "unique visual windows")
