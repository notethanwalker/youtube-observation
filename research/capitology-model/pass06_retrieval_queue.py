"""Build a bounded, balanced visual retrieval queue from Pass 4 claim anchors.

This selects candidate windows. It does not assert that video bytes were retrieved
or that the depicted gameplay was verified.
"""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CLAIMS = {c["claim_id"]: c for c in map(json.loads, (ROOT / "pass04_claims.jsonl").open())}

# Each question has an older or framing example and a later, limiting, or
# counterexample. A/B priority controls retrieval order, not evidential weight.
# Times are deliberately short replay windows around the spoken anchors.
WINDOWS = [
    ("turns", "A", "early-turn example", "P4-007", "06:20", "07:40", "Track which cooldown and space exchange constitutes the first turn; identify the threatened cart and DPS angles."),
    ("turns", "B", "soft-dive extension", "P4-008", "09:00", "10:35", "Locate the enemy Winston exit and the second entry; check whether the attackers actually retained resources."),
    ("turns", "A", "later bait mechanism", "P4-034", "02:05", "04:45", "Identify the offered cooldown or position, both teams' options, and whether the response was forced."),
    ("turns", "B", "later counterplay", "P4-206", "09:05", "11:15", "Check the clear, delayed rotation, accumulated advantage, and whether a later turn still exists."),
    ("retreat", "A", "late forced retreat", "P4-021", "00:30", "01:50", "Measure who holds the angles before contact and what resources remain when the retreat starts."),
    ("retreat", "A", "early voluntary withdrawal", "P4-031", "03:00", "05:20", "Mark the original corner, retreat distance, available cooldowns, and new route before contact."),
    ("retreat", "B", "reset after first turn", "P4-032", "05:35", "06:55", "Check whether the first turn failed and the team regained a usable angle after backing out."),
    ("ultimate_economy", "A", "qualified economy thesis", "P4-027", "01:30", "04:20", "Record ultimate counts, fight winner, and the actual playmaking route; distinguish illustration from measured frequency."),
    ("ultimate_economy", "B", "kite example", "P4-028", "04:15", "06:50", "Locate front and backline spacing, the ultimate trigger, escape path, and next engagement."),
    ("ultimate_economy", "A", "spend to secure retake", "P4-053", "09:20", "10:20", "Check objective and charge state when multiple ultimates are committed; verify the fight outcome."),
    ("ultimate_economy", "A", "failed triple-ultimate distinction", "P4-198", "11:52", "14:43", "Compare the two discussed failures: spent ultimates, point flip, following setup, and losing cause."),
    ("dive_survival", "A", "prevent strong setup", "P4-017", "03:55", "05:52", "Map Tracer angle and Winston staging before support cooldowns are tested; identify available clear."),
    ("dive_survival", "B", "wide clearing route", "P4-018", "09:50", "11:50", "Follow the retake route and check whether the enemy jump becomes long or poorly staged."),
    ("dive_survival", "A", "defensive ultimate before setup", "P4-134", "12:31", "15:39", "Check attacker angles, Winston distance, ultimate timing, objective, and defender alternatives."),
    ("dive_survival", "B", "scouting support exception", "P4-175", "20:10", "24:50", "Verify what the offset support can see and whether Rush or Beat occurs before the dive is complete."),
    ("bait", "A", "failed passive kite", "P4-015", "06:30", "07:50", "Check whether the baiting team has counterpressure and enough cooldowns to stand and punish."),
    ("bait", "A", "first mover accepts bait", "P4-035", "10:25", "12:25", "Trace cooldown trade, immediate response, and whether the baiting side can still answer."),
    ("bait", "B", "choice after forced cooldown", "P4-199", "06:00", "09:29", "Compare chasing the front player with attacking exposed teammates; record the chosen route and result."),
    ("bait", "B", "clear the attention holder", "P4-125", "12:43", "16:56", "Check whether the bait player's space is actually cleared before pursuing a distant backline."),
    ("splits", "A", "2023 push and pull", "P4-003", "08:50", "10:14", "Map both cores, their distance, enemy commitment, retreat, and simultaneous counterpressure."),
    ("splits", "B", "2023 failure or limit", "P4-004", "18:30", "20:00", "Check whether the pressured off angle survives and whether advancing both cores wastes the exchange."),
    ("splits", "A", "2026 attention exchange", "P4-091", "01:00", "02:45", "Map contemporary split positions and whether pressure alternates rather than remaining on one group."),
    ("splits", "B", "2026 delayed split adaptation", "P4-193", "02:31", "05:56", "Identify teleport/D.Va clear threat and whether the team begins together then splits later."),
]


def seconds(s):
    parts = [int(v) for v in s.split(":")]
    return parts[-2] * 60 + parts[-1]


rows = []
for i, (question, priority, role, cid, start, end, check) in enumerate(WINDOWS, 1):
    c = CLAIMS[cid]
    a, b = seconds(start), seconds(end)
    assert a < b and a <= c["start_seconds"] <= b, (cid, start, end)
    rows.append({
        "window_id": f"V6-{i:02d}", "question": question, "priority": priority,
        "evidence_role": role, "claim_ids": cid, "video_id": c["video_id"],
        "video_title": c["video_title"], "upload_date": c["upload_date"],
        "start": start, "end": end, "start_seconds": a, "end_seconds": b,
        "duration_seconds": b-a,
        "url": f'https://www.youtube.com/watch?v={c["video_id"]}&t={a}s',
        "visual_check": check,
        "retrieval_status": "queued_not_retrieved",
        "visual_review_status": "not_reviewed",
    })

assert len(rows) == 23 and len({r["window_id"] for r in rows}) == len(rows)
assert len({r["video_id"] for r in rows}) == 12
assert {r["question"] for r in rows} == {"turns", "retreat", "ultimate_economy", "dive_survival", "bait", "splits"}

with (ROOT / "pass06_retrieval_queue.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

print(f'{len(rows)} windows, {len({r["video_id"] for r in rows})} videos, '
      f'{sum(r["duration_seconds"] for r in rows)/60:.1f} minutes')
