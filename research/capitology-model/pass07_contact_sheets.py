"""Create timestamped contact sheets from retrieved Pass 6 clips for visual triage."""

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
MEDIA = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
REGISTRY = json.loads((ROOT / "pass06_retrieval_registry.json").read_text())["windows"]
QUEUE = {r["window_id"]: r for r in csv.DictReader((ROOT / "pass06_retrieval_queue.csv").open())}
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)


def timecode(t):
    return f"{t // 60:02d}:{t % 60:02d}"


for wid in sorted(REGISTRY):
    item = REGISTRY[wid]
    q = QUEUE[wid]
    clip = MEDIA / ("batch-trial-01" if wid in ("V6-01", "V6-02", "V6-05") else
                    "local-proof" if wid in ("V6-06", "V6-07") else
                    "batch-02" if item["archive"].endswith("part2.zip") else
                    "batch-03" if item["archive"].endswith("part3.zip") else "batch-04") / item["clip"]
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(clip),
                        "-vf", "fps=1/10,scale=480:270", "-q:v", "4", f"{td}/%03d.jpg"],
                       check=True)
        frames = sorted(Path(td).glob("*.jpg"))
        cols = 4
        rows = (len(frames) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * 480, rows * 304 + 42), "#10151d")
        d = ImageDraw.Draw(canvas)
        d.text((12, 9), f"{wid}  {q['video_title']}  {q['start']}–{q['end']}", font=FONT, fill="white")
        for i, frame in enumerate(frames):
            x, y = i % cols * 480, 42 + i // cols * 304
            canvas.paste(Image.open(frame), (x, y))
            d.text((x + 9, y + 273), f"{timecode(item['start_seconds'] + i * 10)}  +{i * 10}s", font=FONT, fill="white")
        canvas.save(OUT / f"{wid}.jpg", quality=85)
    print(wid, len(frames), flush=True)
