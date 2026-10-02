"""Broad-to-dense video review grounded in the Pass 9 Capitology rules.

Uses sampled stills for navigation and closer windows for findings. It never
claims to inspect unsampled motion or audio. Supports local Ollama vision models
or the OpenAI API; no mock review is exposed in the player-facing service.
"""

from __future__ import annotations

import base64
import json
import os
import random
import re
import subprocess
import time
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "research/capitology-model/pass09_rules.json"
API_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/responses"
BROAD_MODEL = os.getenv("MATCH_REVIEW_BROAD_MODEL", "gpt-5-mini")
DENSE_MODEL = os.getenv("MATCH_REVIEW_DENSE_MODEL", "gpt-5-mini")
LOCAL_MODEL = os.getenv("MATCH_REVIEW_LOCAL_MODEL", "qwen3-vl:4b-instruct")
OLLAMA_URL = os.getenv("MATCH_REVIEW_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
GEMINI_MODEL = os.getenv("MATCH_REVIEW_GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_URL = os.getenv("MATCH_REVIEW_GEMINI_URL", "https://generativelanguage.googleapis.com/v1beta/models").rstrip("/")
MAX_DURATION = int(os.getenv("MATCH_REVIEW_MAX_DURATION_SECONDS", "3600"))
MAX_BROAD_CALLS = int(os.getenv("MATCH_REVIEW_MAX_BROAD_CALLS", "30"))
MAX_DENSE_CALLS = int(os.getenv("MATCH_REVIEW_MAX_DENSE_CALLS", "8"))


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
         "-show_entries", "stream=codec_type,width,height", "-of", "json", str(path)],
        text=True, capture_output=True, check=True,
    )
    data = json.loads(result.stdout)
    if not any(s.get("codec_type") == "video" for s in data.get("streams", [])):
        raise ValueError("The upload does not contain a video stream.")
    duration = float(data["format"]["duration"])
    if not 15 <= duration <= MAX_DURATION:
        raise ValueError(f"Recording duration must be between 15 and {MAX_DURATION} seconds.")
    return {"duration_seconds": round(duration, 3), "size_bytes": int(data["format"].get("size", path.stat().st_size))}


def frame(video: Path, seconds: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{seconds:.3f}",
         "-i", str(video), "-frames:v", "1", "-vf", "scale='min(960,iw)':-2",
         "-q:v", "3", str(dest)], check=True, capture_output=True,
    )
    if not dest.exists() or dest.stat().st_size < 1000:
        raise ValueError(f"Could not sample recording at {seconds:.1f}s")
    return dest


def image_content(path: Path) -> dict:
    return {"type": "input_image", "image_url": "data:image/jpeg;base64," +
            base64.b64encode(path.read_bytes()).decode("ascii"), "detail": "high"}


def provider_ready() -> bool:
    provider = os.getenv("MATCH_REVIEW_PROVIDER", "openai").lower()
    if provider == "ollama":
        return True  # The local server/model are checked when analysis starts.
    if provider == "gemini":
        return bool(os.getenv("GEMINI_API_KEY"))
    return provider == "openai" and bool(os.getenv("OPENAI_API_KEY"))


def wait_for_gemini(exc: HTTPError, attempt: int) -> None:
    retry_after = exc.headers.get("Retry-After", "")
    delay = float(retry_after) if retry_after.isdigit() else 2 ** (attempt + 1) + random.uniform(0, 1)
    time.sleep(min(30, max(1, delay)))


def gemini_call(prompt: str, images: list[Path], schema: dict) -> dict:
    key = os.getenv("GEMINI_API_KEY", "").strip().strip("\"'")
    if not key:
        raise RuntimeError("Enter your free Gemini API key in the launcher, then retry the saved recording.")
    parts = [{"text": prompt}] + [
        {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(path.read_bytes()).decode("ascii")}}
        for path in images]
    payload = {"contents": [{"role": "user", "parts": parts}],
               "generationConfig": {"responseMimeType": "application/json", "responseJsonSchema": schema}}
    request = Request(GEMINI_URL + "/" + quote(GEMINI_MODEL, safe="") + ":generateContent",
                      data=json.dumps(payload).encode("utf-8"),
                      headers={"x-goog-api-key": key, "Content-Type": "application/json"}, method="POST")
    for attempt in range(5):
        try:
            with urlopen(request, timeout=240) as response:
                data = json.load(response)
            break
        except HTTPError as exc:
            detail = exc.read(2048).decode("utf-8", errors="replace")
            if exc.code in (400, 401, 403) and ("API_KEY_INVALID" in detail or "API key not valid" in detail):
                raise RuntimeError("Google rejected the Gemini API key. In AI Studio, copy the full active key using its Copy button (not the project ID or key name), restart the launcher, and retry the saved recording. Keep the key private.") from exc
            if exc.code == 404 and ("model" in detail.lower() or "not found" in detail.lower()):
                raise RuntimeError(f"Gemini model {GEMINI_MODEL} is unavailable for this project. Download the latest Capitology ZIP, then retry the saved recording. Google details: {detail[:180]}") from exc
            if exc.code == 429:
                if attempt < 2:
                    wait_for_gemini(exc, attempt)
                    continue
                raise RuntimeError("Gemini free-tier limit reached. Check your AI Studio usage and retry this saved recording later.") from exc
            if exc.code in (500, 502, 503, 504):
                if attempt < 4:
                    wait_for_gemini(exc, attempt)
                    continue
                raise RuntimeError("Gemini is temporarily overloaded and did not recover after several retries. Try Retry saved recording later; completed sections will be preserved.") from exc
            if exc.code in (401, 403):
                raise RuntimeError("Gemini key was rejected or has no access. Check the AI Studio key, then restart the launcher.") from exc
            raise RuntimeError(f"Gemini analysis request failed (HTTP {exc.code}): {detail[:300]}") from exc
        except (URLError, TimeoutError) as exc:
            raise RuntimeError("Gemini could not be reached. Check your internet connection, then retry the saved recording.") from exc
    try:
        return json.loads("".join(p["text"] for p in data["candidates"][0]["content"]["parts"] if "text" in p))
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError("Gemini returned no valid structured review. Try the saved recording again.") from exc


def local_call(prompt: str, images: list[Path], schema: dict) -> dict:
    # Do not permit a mistaken URL override to send private recording frames away.
    url = urlsplit(OLLAMA_URL)
    if url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost", "::1"} or url.username or url.password or url.path not in {"", "/"}:
        raise RuntimeError("The local Ollama URL must point to loopback HTTP on this PC.")
    payload = {
        "model": LOCAL_MODEL, "stream": False, "format": schema,
        "options": {"temperature": 0, "num_ctx": 16384},
        "messages": [{"role": "user", "content": prompt + "\nReturn only JSON matching the requested schema.",
                      "images": [base64.b64encode(path.read_bytes()).decode("ascii") for path in images]}],
    }
    request = Request(OLLAMA_URL + "/api/chat", data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=1200) as response:
            data = json.load(response)
    except HTTPError as exc:
        detail = exc.read(512).decode("utf-8", errors="replace")
        if exc.code == 404:
            raise RuntimeError(f"Local model {LOCAL_MODEL} is missing. Run 'ollama pull {LOCAL_MODEL}', then retry the saved recording.") from exc
        raise RuntimeError(f"Local Ollama analysis failed (HTTP {exc.code}): {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("Cannot reach local Ollama. Start Ollama on this PC, then retry the saved recording.") from exc
    try:
        return json.loads(data["message"]["content"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Local vision model did not return a valid structured review. Retry or try a larger local model.") from exc


def structured_call(model: str, prompt: str, images: list[Path], schema: dict, name: str) -> dict:
    provider = os.getenv("MATCH_REVIEW_PROVIDER", "openai").lower()
    if provider == "ollama":
        return local_call(prompt, images, schema)
    if provider == "gemini":
        return gemini_call(prompt, images, schema)
    if provider != "openai":
        raise RuntimeError(f"Unknown analysis provider: {provider}")
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for match analysis.")
    content = [{"type": "input_text", "text": prompt}] + [image_content(path) for path in images]
    payload = {"model": model, "store": False,
               "input": [{"role": "user", "content": content}],
               "text": {"format": {"type": "json_schema", "name": name,
                                    "strict": True, "schema": schema}}}
    request = Request(API_URL, data=json.dumps(payload).encode("utf-8"),
                      headers={"Authorization": f"Bearer {key}",
                               "Content-Type": "application/json"}, method="POST")
    for attempt in range(5):
        try:
            with urlopen(request, timeout=180) as response:
                data = json.load(response)
            break
        except HTTPError as exc:
            try:
                detail = json.loads(exc.read(4096)).get("error", {})
            except (ValueError, UnicodeDecodeError):
                detail = {}
            code = str(detail.get("code") or detail.get("type") or "")
            message = str(detail.get("message") or "")
            if exc.code == 429:
                if code in {"insufficient_quota", "credit_balance_exhausted"} or "quota" in message.lower():
                    raise RuntimeError("OpenAI API credits are unavailable. Check your Platform billing balance, then retry this saved recording.") from exc
                if code in {"organization_spend_limit_exceeded", "project_spend_limit_exceeded",
                            "organization_usage_limit_exceeded"}:
                    raise RuntimeError(f"OpenAI API limit ({code}) reached. Check Platform limits, then retry this saved recording.") from exc
                if attempt < 4:
                    retry_after = exc.headers.get("Retry-After", "")
                    delay = float(retry_after) if retry_after.isdigit() else 2 ** (attempt + 1)
                    time.sleep(min(30, max(1, delay)))
                    continue
                raise RuntimeError("OpenAI API rate limit persisted after retries. Check your Platform limits and try this saved recording later.") from exc
            if exc.code in {401, 403}:
                raise RuntimeError("OpenAI API key was rejected or lacks access. Check the key and project permissions, then restart the launcher.") from exc
            raise RuntimeError(f"OpenAI API rejected the analysis request (HTTP {exc.code}, {code or 'unknown code'}).") from exc
    chunks = [c.get("text", "") for item in data.get("output", [])
              for c in item.get("content", []) if c.get("type") == "output_text"]
    if not chunks:
        raise RuntimeError("Analysis model returned no structured text output.")
    return json.loads("".join(chunks))


OBJECT = {"type": "object", "additionalProperties": False}
CANDIDATE_SCHEMA = {**OBJECT, "properties": {
    "overview": {"type": "string"},
    "candidates": {"type": "array", "items": {**OBJECT, "properties": {
        "start_seconds": {"type": "number"}, "end_seconds": {"type": "number"},
        "score": {"type": "integer"}, "visible_change": {"type": "string"},
        "review_reason": {"type": "string"}, "uncertainty": {"type": "string"}},
        "required": ["start_seconds", "end_seconds", "score", "visible_change", "review_reason", "uncertainty"]}},
}, "required": ["overview", "candidates"]}
FINDING_SCHEMA = {**OBJECT, "properties": {
    "reviewable": {"type": "boolean"}, "title": {"type": "string"},
    "start_seconds": {"type": "number"}, "end_seconds": {"type": "number"},
    "player_evidence": {"type": "string"}, "situation": {"type": "string"},
    "player_action": {"type": "string"}, "visible_response": {"type": "string"},
    "observed": {"type": "string"}, "interpretation": {"type": "string"},
    "impact_reason": {"type": "string"},
    "alternative": {"type": "string"}, "when_alternative_fails": {"type": "string"},
    "confidence": {"type": "string", "enum": ["low", "moderate", "high"]},
    "uncertainty": {"type": "string"}, "rule_ids": {"type": "array", "items": {"type": "string"}},
    "impact": {"type": "integer"}, "positive": {"type": "boolean"},
}, "required": ["reviewable", "title", "start_seconds", "end_seconds", "player_evidence", "situation",
                "player_action", "visible_response", "observed", "interpretation", "impact_reason",
                "alternative", "when_alternative_fails", "confidence", "uncertainty", "rule_ids", "impact", "positive"]}


def candidate_windows(video: Path, duration: float, frame_dir: Path, player: dict, progress,
                      checkpoint: dict | None = None, save=None) -> tuple[list[dict], list[str]]:
    # Twelve frames per two-minute chunk cover the full recording at 10s steps.
    windows = list(checkpoint.get("candidates", [])) if checkpoint else []
    overviews = list(checkpoint.get("overviews", [])) if checkpoint else []
    chunks = min(MAX_BROAD_CALLS, int((duration + 119) // 120))
    if chunks * 120 < duration:
        raise ValueError("Recording exceeds the configured broad-pass capacity.")
    for i in range(chunks):
        if i < len(overviews):
            continue
        start, end = i * 120.0, min(duration, (i + 1) * 120.0)
        times = [start + 5 + 10 * j for j in range(12) if start + 5 + 10 * j < end]
        if not times:
            times = [(start + end) / 2]
        images = [frame(video, t, frame_dir / f"broad_{i:03d}_{j:02d}.jpg") for j, t in enumerate(times)]
        prompt = (
            "You are navigating an Overwatch recording using sparse still frames, not continuous video. "
            f"Target metadata: {json.dumps(player)}. This chunk is {start:.1f}–{end:.1f}s of the original recording. "
            f"Frames in order have original times {times}. Identify up to TWO promising 15–35 second windows "
            "for a closer tactical review: objective changes, deaths/kill-feed changes, positioning shifts, "
            "a lost or won fight, or a meaningful setup. Skip menus, replays, and long static screens. "
            "Set score 1–5 for coaching value. Return original recording timestamps within this chunk. "
            "Describe only changes visible across the sampled stills; state what the gaps prevent you from knowing. "
            "Do not claim to see an exact ability order or infer a player's intention."
        )
        result = structured_call(BROAD_MODEL, prompt, images, CANDIDATE_SCHEMA, "match_candidates")
        overviews.append(result["overview"])
        for item in result["candidates"][:2]:
            a, b = float(item["start_seconds"]), float(item["end_seconds"])
            if start <= a < b <= end and 1 <= int(item["score"]) <= 5:
                windows.append(item)
        if checkpoint is not None:
            checkpoint.update(candidates=windows, overviews=overviews)
            save(checkpoint)
        progress("scanning", round(10 + 45 * (i + 1) / chunks), f"Scanned {i + 1} of {chunks} sections")
    return windows, overviews


def rule_matches(text: str, rules: list[dict], limit: int = 8) -> list[dict]:
    words = set(re.findall(r"[a-z0-9]{3,}", text.lower()))
    ranked = sorted(rules, key=lambda r: (sum(3 for t in r["tags"] if any(w in t.lower() for w in words)) +
                                         len(words & set(re.findall(r"[a-z0-9]{3,}", (r["title"] + " " + r["statement"]).lower()))),
                                         r["id"]), reverse=True)
    return ranked[:limit]


def select_windows(items: list[dict], limit: int) -> list[dict]:
    chosen = []
    for item in sorted(items, key=lambda c: (-int(c["score"]), float(c["start_seconds"]))):
        center = (float(item["start_seconds"]) + float(item["end_seconds"])) / 2
        if all(abs(center - (float(x["start_seconds"]) + float(x["end_seconds"])) / 2) >= 35 for x in chosen):
            chosen.append(item)
        if len(chosen) >= limit:
            break
    return sorted(chosen, key=lambda x: float(x["start_seconds"]))


def review_window(video: Path, duration: float, frame_dir: Path, candidate: dict,
                  player: dict, rules: list[dict], index: int) -> dict | None:
    center = (float(candidate["start_seconds"]) + float(candidate["end_seconds"])) / 2
    start, end = max(0.0, center - 16), min(duration - .1, center + 16)
    times = [start + j * 2.5 for j in range(14) if start + j * 2.5 <= end]
    images = [frame(video, t, frame_dir / f"dense_{index:02d}_{j:02d}.jpg") for j, t in enumerate(times)]
    selected = rule_matches(candidate["visible_change"] + " " + candidate["review_reason"] + " " +
                            player.get("hero", "") + " " + player.get("role", ""), rules)
    compact = [{k: r[k] for k in ("id", "title", "statement", "trigger", "action", "exception", "evidence")}
               for r in selected]
    prompt = (
        "Review one Overwatch recording interval from sampled frames. The player requested a coach-style report. "
        f"Player metadata: {json.dumps(player)}. Original frame times: {times}. Candidate reason: "
        f"{candidate['review_reason']}. Relevant Capitology rules: {json.dumps(compact)}. "
        "Only claim visible facts when frames support them. Do not infer which side is the player's team if unclear. "
        "Separate observation from tactical interpretation; name a conditional alternative and when it would fail. "
        "State how the target player was identified, the visible situation, their visible action, and a visible response. "
        "Use 'unclear' where needed. If identity, POV, event sequence, or objective is too unclear for a meaningful player finding, set reviewable=false. "
        "Do not infer exact cooldowns, hidden enemy knowledge, audio comms, full fight result, or intent through the frame gaps. "
        "Use only supplied rule IDs, and do not imply that the source match is the uploaded match. "
        "Explain why the decision could matter independently of the fight result. "
        "Return recording timestamps inside this inspected interval, impact 1–5, and an honest confidence."
    )
    result = structured_call(DENSE_MODEL, prompt, images, FINDING_SCHEMA, "match_finding")
    if not result.get("reviewable"):
        return None
    a, b = float(result["start_seconds"]), float(result["end_seconds"])
    allowed = {r["id"] for r in selected}
    ids = [rid for rid in result["rule_ids"] if rid in allowed]
    if (not start <= a < b <= end or not ids or
            any(not result[k].strip() or result[k].strip().lower() == "unclear"
                for k in ("player_evidence", "player_action", "observed", "impact_reason"))):
        return None
    result["rule_ids"] = ids
    result["impact"] = max(1, min(5, int(result["impact"])))
    # Sparse stills cannot justify a high-confidence claim about a sequence.
    if result["confidence"] == "high":
        result["confidence"] = "moderate"
    return result


def analyze(video: Path, job_dir: Path, player: dict, progress) -> dict:
    meta = probe(video)
    rules = json.loads(RULES_PATH.read_text())["rules"]
    duration = meta["duration_seconds"]
    frame_dir = job_dir / "frames"
    checkpoint_path = job_dir / "analysis_checkpoint.json"
    model_identity = {"provider": os.getenv("MATCH_REVIEW_PROVIDER", "openai").lower(),
                      "broad": BROAD_MODEL, "dense": DENSE_MODEL,
                      "local": LOCAL_MODEL, "gemini": GEMINI_MODEL}
    try:
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        checkpoint = {}
    if checkpoint.get("model_identity") != model_identity:
        checkpoint = {"model_identity": model_identity}

    def save_checkpoint(state: dict) -> None:
        temporary = checkpoint_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state), encoding="utf-8")
        temporary.replace(checkpoint_path)

    progress("scanning", 8, "Scanning the full recording")
    try:
        candidates, overviews = candidate_windows(video, duration, frame_dir, player, progress,
                                                  checkpoint, save_checkpoint)
        selected = select_windows(candidates, MAX_DENSE_CALLS)
        results = list(checkpoint.get("dense_results", []))
        for i, candidate in enumerate(selected):
            if i < len(results):
                continue
            finding = review_window(video, duration, frame_dir, candidate, player, rules, i)
            results.append(finding)
            checkpoint["dense_results"] = results
            save_checkpoint(checkpoint)
            progress("reviewing", round(56 + 38 * (i + 1) / max(1, len(selected))),
                     f"Reviewed {i + 1} of {len(selected)} candidate moments")
    finally:
        # Derived frames are transient; retain only the upload and report.
        import shutil
        shutil.rmtree(frame_dir, ignore_errors=True)
    findings = [finding for finding in results if finding]
    # Keep the most useful moments, then display in match order.
    findings = sorted(sorted(findings, key=lambda f: (-f["impact"], f["start_seconds"]))[:6],
                      key=lambda f: f["start_seconds"])
    rule_map = {r["id"]: r for r in rules}
    for finding in findings:
        finding["rule_sources"] = [{"rule_id": rid, "title": rule_map[rid]["title"],
                                    "evidence": rule_map[rid]["evidence"],
                                    "sources": rule_map[rid]["sources"][:3]} for rid in finding["rule_ids"]]
    counts = Counter(rid for f in findings for rid in f["rule_ids"])
    recurring = [{"rule_id": rid, "title": rule_map[rid]["title"], "moments": count}
                 for rid, count in counts.most_common() if count >= 2]
    report = {"status": "complete" if findings else "insufficient_evidence",
            "review_type": "clip" if duration < 300 else "match",
            "duration_seconds": duration, "player": player,
            "method": "Full recording sampled every 10 seconds; selected moments sampled every 2.5 seconds. Audio and intervening motion were not analyzed.",
            "scope": "Provisional Capitology coaching model; findings are hypotheses grounded in visible frames and source-linked rules. " +
                     ("This short recording cannot establish earlier resource cycles or decisions." if duration < 300 else ""),
            "broad_overviews": overviews, "candidate_count": len(candidates),
            "findings": findings, "recurring_patterns": recurring,
            "next_match_cues": [f["alternative"] for f in sorted(findings, key=lambda x: -x["impact"])[:2]],
            "limits": ["Single-POV information and hidden cooldowns cannot be established from sampled frames.",
                       "A fight result alone does not prove the decision was correct or incorrect."]}
    checkpoint_path.unlink(missing_ok=True)
    return report
