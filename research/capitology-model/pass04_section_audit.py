"""Build an honest Pass 4 section-level transcript review queue.

FULL_READ is a manually maintained list of complete Pass 3 caption sections read
in order for Pass 4. A claim interval alone only proves a sampled evidence window.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parent

FULL_READ = {
    "c92ESPjlveI": {5},
    "JM50b3IU6-c": {2, 3, 5, 6, 7, 9, 10},
    "z9n-JNB52rk": {2, 3, 5, 6},
    "pMPwEwNEiQA": {2, 5, 6, 7},
    "p609brPyPzg": {3, 4, 6},
    "QvMsOy1wFr4": {1, 2, 5, 6, 8, 9, 10},
    "STbH6hH8emk": {5, 6},
    "XhcF5IzJDq4": {3, 4, 5, 6, 7},
    "K6Ayz-NHVe4": {4, 5, 6},
    "V-Y0hBOI1yY": {2, 3, 5},
    "nddeTxFzT6Q": {2, 3, 5, 6},
    "GjlM3r948EI": {1},
    "pQcjwEjo6us": {1},
    "UC8D2vBDf_0": {1, 2},
    "E1bYy6OE_OQ": {3},
    "LpxT2dykNK0": {2, 3},
    "MYW1ztAeDQc": {3, 5},
    "1UNctVbRS3M": {3, 4, 5, 6, 7, 8},
    "jSCHyAWoUjc": {1, 3, 4, 5},
    "M8393UkZxjY": {1, 2, 3, 4, 7, 8},
    "t1dnez3yuZ4": {1, 2, 5},
    "Y4ORvoqZ1P0": {3, 4, 5},
    "sqtmsbHxrLE": {1, 3, 4, 5, 6},
    "LSrm0ocaS1Q": {2, 5, 6},
    "AcAxvnAEYpg": {1, 2, 3, 4},
    "1OvQ5PAK0w0": {3, 4, 5, 6, 7},
    "2X_yEWyNms0": {2, 3},
    "TOaKp3Z44ho": {2, 3, 4, 5},
    "ln2t2rl1KYw": {2, 3, 5, 6, 7},
    "aNBstKtsPms": {3, 4, 5},
    "vu4KmVKp2f0": {2},
    "x5ej22cA7G0": {1, 4, 5},
    "xabIcyolpJA": {3},
    "GIY_4hD9_M8": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18},
    "n-t2m7R_Gho": {1, 2, 3, 6, 7},
    "cXnFhS2l47g": {2, 3, 4, 5, 7, 8, 9},
    "GYBpp0KM5-Q": {3, 4, 6},
    "N5fHwbNE-SQ": {1, 3, 4, 5},
    "prUv2eNrGD0": {1, 2, 3, 4, 7, 9, 10},
    "ijlmDdVIdtk": {2, 3, 4},
    "AtmKIdmLLQ8": {1, 2, 3, 5, 6},
    "GKkzCd9cvUg": {4, 5},
    "KlcWDgdXrZk": {3, 5},
    "x2jNJeKiMUU": {1, 2, 3, 4},
    "Hl-nV1aF1yE": {4, 5},
    "FjoWkH6Sl1k": {1, 2, 3, 6},
    "iLX7uqsC1jE": {1, 2, 3, 4, 6},
}


def main():
    claims = [json.loads(line) for line in (ROOT / "pass04_claims.jsonl").open()]
    sections = [json.loads(line) for line in (ROOT / "pass03_segments.jsonl").open()]
    assert sum(map(len, FULL_READ.values())) == 180
    section_keys = {(s["video_id"], s["segment_number"]) for s in sections}
    assert all((v, n) in section_keys for v, nums in FULL_READ.items() for n in nums)
    rows = []
    for section in sections:
        video = section["video_id"]
        overlapping = [c["claim_id"] for c in claims if c["video_id"] == video
                       and c["start_seconds"] * 1000 < section["end_ms"]
                       and c["end_seconds"] * 1000 > section["start_ms"]]
        if section["segment_number"] in FULL_READ.get(video, set()):
            status = "full_transcript_section_read"
        elif overlapping:
            status = "sampled_claim_window_only"
        else:
            status = "not_yet_reviewed"
        rows.append({
            "segment_id": section["segment_id"],
            "video_id": video,
            "upload_date": section["upload_date"],
            "start": section["start"],
            "end": section["end"],
            "review_status": status,
            "overlapping_claim_ids": ";".join(overlapping),
            "review_basis": "automatic captions; gameplay not visually checked" if status != "not_yet_reviewed" else "",
        })
    with (ROOT / "pass04_section_audit.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(Counter(r["review_status"] for r in rows))


if __name__ == "__main__":
    main()
