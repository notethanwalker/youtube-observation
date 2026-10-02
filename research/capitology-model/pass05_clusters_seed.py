"""Manual, provisional concept clustering of the Pass 4 claim ledger.

IDs below are editorial assignments, not a keyword model or independent
gameplay verification. Rebuild the index and registry from the claim ledger.
"""

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent

# A single primary home makes omissions visible. A claim can additionally have
# secondary links, which do not increase the primary cluster count.
CLUSTERS = {
    "C01_turns": ("Turns and initiative", "When to spend a turn, reset, or chain another one", "5-8 14 33 55 100 109 118 196 197 206"),
    "C02_information": ("Information and concealment", "See the opposing setup while controlling what opponents can see", "19 20 39 87 132 183 202"),
    "C03_geometry": ("Reach, corners, and voluntary space", "Threaten from outside effective reach and distinguish planned withdrawal from forced retreat", "9 11 30-32 75 76 103 108 110 162 163 200"),
    "C04_splits": ("Split cores and attention exchange", "Coordinate distinct groups so pressure on one enables the other", "1-4 91 101 102 104-107 143 144 193"),
    "C05_setup": ("Engage staging and prevention", "Create a favorable entry or disrupt it before it becomes a good dive", "16-18 21 60 63 64 119 133-139 145 146 171 175 178 180 205"),
    "C06_bait": ("Bait and opponent choices", "Offer a credible option, anticipate the response, and preserve a counter", "15 34 35 54 92 95 125 126 189 190 194 199"),
    "C07_windows": ("Cooldown and role windows", "Match the size and beneficiary of a window to the size of the commitment", "25 81 82 155 164 187"),
    "C08_ultimates": ("Ultimate use and economy", "Evaluate ultimates with fight state, spacing, sequencing, and composition exceptions", "26-29 36 37 53 86 121 147 158 176 198"),
    "C09_compositions": ("Composition and matchup adaptation", "Compare win conditions, target allocation, bans, counterplay, and resource needs", "10 24 58 61 70-72 80 117 120 149 167 170 172-174 181 182 184-186 195 204"),
    "C10_objective": ("Objective and retake routes", "Turn a point flip or retake into a useful subsequent setup", "38 153 154 161 165 177"),
    "C11_tank": ("Tank execution", "Manage armor, ammunition, mobility, defensive tools, and target choice", "46-48 56 57 65 66 114-116 127 128"),
    "C12_dps": ("Damage-role execution", "Maintain threatening angles and escapes while selecting useful targets and duel timing", "44 45 50-52 67 68 73 74 78 79 83-85 89 93 94 111-113 122 129-131 140-142 148 151 152 166 169 191 192"),
    "C13_support": ("Support positioning and escape", "Preserve contribution while managing exposure, peel, and safe movement", "43 49 59 123 124 179 188"),
    "C14_execution": ("Attention and match execution", "Maintain awareness and execute known plans under pressure", "12 13 96 150 156 157"),
    "C15_learning": ("Observation and coaching method", "Reconstruct available information, compare evidence, and practice specific actions", "22 23 40-42 62 69 88 90 97 98 168 203"),
    "C16_design": ("Balance and design views", "Role alternatives and opponent counterplay in hero design", "77 99 159 160 201"),
}


def expand(spec):
    out = []
    for item in spec.split():
        if "-" in item:
            a, b = map(int, item.split("-"))
            out.extend(range(a, b + 1))
        else:
            out.append(int(item))
    return [f"P4-{n:03}" for n in out]


# Selective additional membership for ideas that genuinely bridge clusters.
# Missing secondary links mean only that no additional label was adjudicated.
SECONDARY = {
    "C01_turns": "3 25 32 53 81 82 86 92 95 143 147 155 176 187 194 199",
    "C02_information": "12 19 21 39 64 75 76 84 87 103 132 135 156 157 183 202 205",
    "C03_geometry": "3 4 15 17 18 20 21 28 39 45 61 74 101 115 125 130 133 141 148 153 177 189 190",
    "C04_splits": "19 24 27 67 70 91 145 146 166 169 170 173 180 181 186 204",
    "C05_setup": "19 20 30 39 55 70 71 75 76 83 84 85 92 95 114 115 125 132 141 142 167 171 183 184 187 193",
    "C06_bait": "7 8 11 25 28 30 32 54 55 70 71 76 81 85 109 116 117 118 120 126 142 166 171 189 190 193 194 206",
    "C07_windows": "8 34 35 47 50 51 52 55 64 66 68 73 85 86 114 118 136 137 139 142 147 158 169 174 175 178 180 194 197 198 206",
    "C08_ultimates": "28 38 48 51 52 100 112 117 122 128 134 170 171 175 197 202",
    "C09_compositions": "1 10 16 26 43 44 46 51 57 59 61 72 73 80 91 95 101 102 119 120 125 143 144 145 146 148 153 159 164 165 167 173 180 193 195 204",
    "C10_objective": "7 18 29 38 53 70 72 86 100 105 121 143 158 161 165 167 170 177 183 197 198",
    "C11_tank": "7 17 24 28 34 37 48 60 61 63 64 75 95 103 109 133 134 139 145 157 170 175 178 185 187 189 190 195",
    "C12_dps": "4 12 13 19 22 25 51 55 64 67 68 73 74 75 76 78 79 83 84 85 87 89 94 96 101 103 111 112 113 115 125 136 145 151 152 166 169 174 180 192",
    "C13_support": "9 11 15 17 18 28 37 44 45 49 53 59 73 74 82 86 108 117 121 123 124 126 130 131 134 155 158 166 175 179 188 189 204",
    "C14_execution": "12 13 22 23 40 41 42 62 64 65 66 78 79 88 90 93 94 96 97 98 129 135 136 150 151 152 156 157 169 191 192 202 203",
    "C15_learning": "12 13 19 22 23 40 41 42 62 69 78 79 88 90 93 94 96 97 98 150 156 157 168 191 203",
}

# Concept-level relationships point to representative source claims. These are
# hypotheses to test in Passes 6-8, never gameplay-verified conclusions.
RELATIONSHIPS = [
    ("C02_information", "enables", "C05_setup", "19 20 132 183", "Information gained before the fight helps determine and conceal the final setup."),
    ("C03_geometry", "constrains", "C01_turns", "11 31 32 75 76 109", "A first move can spend resources without entering effective reach; voluntary retreat preserves a later move."),
    ("C04_splits", "implements", "C06_bait", "3 4 91 143 144 193", "Pressure on one group can invite pursuit while a second group gains a different option."),
    ("C05_setup", "qualifies", "C13_support", "16 17 18 134 175", "Whether a backline lives a dive depends on whether the attack was allowed to stage well."),
    ("C06_bait", "has_counterplay", "C01_turns", "34 35 199 206", "The first-moving side can decline the obvious chase or stack another advantage; bait may fail."),
    ("C07_windows", "qualifies", "C01_turns", "81 82 155 164 187", "An opening for the frontline need not be an all-team turn."),
    ("C08_ultimates", "depends_on", "C10_objective", "26 29 36 38 53 158 198", "Ult counts alone omit the fight result, point position, subsequent setup, and charge gained."),
    ("C09_compositions", "qualifies", "C08_ultimates", "26 58 72 80 86 117 147", "Economy and cooldown-cycle importance vary with composition and matchup."),
    ("C11_tank", "creates_window_for", "C12_dps", "47 51 57 64 139 145 170 180", "A tank's entry matters partly through what damage players can do during its brief window."),
    ("C12_dps", "trades_off", "C03_geometry", "44 45 73 74 108 130 131", "Excessive safety removes pressure; excessive reach makes the damage dealer an easy trade."),
    ("C14_execution", "limits", "C15_learning", "22 23 96 97 98 150 156", "Knowing the right explanation after a fight differs from seeing and executing it during play."),
    ("C16_design", "separate_scope", "C09_compositions", "77 80 99 159 160 201", "Hero-balance opinions and pre-release predictions are not evidence that a matchup actually works."),
]


def main():
    claims = [json.loads(line) for line in (ROOT / "pass04_claims.jsonl").open()]
    ids = {c["claim_id"] for c in claims}
    assert len(ids) == len(claims) == 206
    primary = {}
    for key, (_, _, spec) in CLUSTERS.items():
        for claim_id in expand(spec):
            assert claim_id not in primary, f"duplicate primary: {claim_id}"
            primary[claim_id] = key
    assert set(primary) == ids, f"missing={sorted(ids-set(primary))}, extra={sorted(set(primary)-ids)}"
    secondary = {claim_id: [] for claim_id in ids}
    for key, spec in SECONDARY.items():
        assert key in CLUSTERS
        for claim_id in expand(spec):
            assert claim_id in ids
            if key == primary[claim_id]:
                continue
            if key not in secondary[claim_id]:
                secondary[claim_id].append(key)
    rows = []
    for c in claims:
        rows.append({
            "claim_id": c["claim_id"], "primary_cluster": primary[c["claim_id"]],
            "secondary_clusters": ";".join(sorted(secondary[c["claim_id"]])),
            "upload_date": c["upload_date"], "video_id": c["video_id"],
            "start": c["start"], "url": c["url"], "claim_class": c["claim_class"],
            "scope": c["scope"], "claim": c["claim"],
            "transcript_confidence": c["transcript_confidence"],
            "visual_dependency": c["visual_dependency"],
            "gameplay_verified": c["gameplay_verified"],
        })
    with (ROOT / "pass05_concept_index.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    registry = []
    for key, (title, working_question, _) in CLUSTERS.items():
        group = [c for c in claims if primary[c["claim_id"]] == key]
        registry.append({
            "cluster_id": key, "title": title, "working_question": working_question,
            "primary_claim_count": len(group),
            "secondary_claim_count": sum(key in secondary[c["claim_id"]] for c in claims),
            "primary_claim_ids": [c["claim_id"] for c in group],
            "year_counts": dict(sorted(Counter(c["upload_date"][:4] for c in group).items())),
            "distinct_videos": len({c["video_id"] for c in group}),
            "high_visual_count": sum(c["visual_dependency"] == "high" for c in group),
        })
    (ROOT / "pass05_cluster_registry.json").write_text(json.dumps({
        "status": "provisional_transcript_only", "source": "pass04_claims.jsonl",
        "primary_membership_total": len(rows), "clusters": registry,
    }, indent=2) + "\n")
    relation_rows = []
    for source, relation, target, spec, question in RELATIONSHIPS:
        evidence = expand(spec)
        assert source in CLUSTERS and target in CLUSTERS and set(evidence) <= ids
        relation_rows.append({"source_cluster": source, "relationship": relation,
                              "target_cluster": target, "evidence_claim_ids": ";".join(evidence),
                              "working_interpretation": question, "status": "open_visual_and_contradiction_review"})
    with (ROOT / "pass05_relationships.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=relation_rows[0].keys())
        writer.writeheader()
        writer.writerows(relation_rows)
    print(f"{len(rows)} claims, {len(registry)} primary clusters, "
          f"{sum(map(len, secondary.values()))} secondary memberships, {len(relation_rows)} relationships")


if __name__ == "__main__":
    main()
