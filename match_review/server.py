"""Small private upload and report server for the match review prototype."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import re
import shutil
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .analysis import analyze, probe


HERE = Path(__file__).resolve().parent
DATA = Path(os.getenv("MATCH_REVIEW_DATA_DIR", HERE.parent / "match-review-data")).resolve()
MAX_UPLOAD = int(os.getenv("MATCH_REVIEW_MAX_UPLOAD_BYTES", str(2 * 1024 ** 3)))
PASSWORD = os.getenv("MATCH_REVIEW_PASSWORD", "")
POOL = ThreadPoolExecutor(max_workers=1)
LOCK = threading.Lock()
ID_RE = re.compile(r"^[a-f0-9]{32}$")
ALLOWED = {".mp4", ".mov", ".mkv", ".webm"}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def job_path(job_id: str) -> Path:
    if not ID_RE.fullmatch(job_id):
        raise ValueError("Invalid job identifier")
    return DATA / job_id


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    with LOCK:
        temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temporary.replace(path)


def read_job(job_id: str) -> dict:
    path = job_path(job_id) / "job.json"
    if not path.is_file():
        raise FileNotFoundError(job_id)
    return json.loads(path.read_text(encoding="utf-8"))


def update_job(job_id: str, **updates) -> None:
    with LOCK:
        path = job_path(job_id) / "job.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(updates, updated_at=timestamp())
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temporary.replace(path)


def work(job_id: str) -> None:
    job = read_job(job_id)
    folder = job_path(job_id)
    video = folder / job["source_file"]

    def progress(stage: str, percentage: int, message: str) -> None:
        update_job(job_id, status=stage, percentage=percentage, message=message)

    try:
        progress("starting", 3, "Preparing the recording")
        report = analyze(video, folder, job["player"], progress)
        write_json(folder / "report.json", report)
        update_job(job_id, status=report["status"], percentage=100,
                   message="Review ready" if report["findings"] else "No reliable finding could be made")
    except Exception as exc:
        update_job(job_id, status="failed", percentage=100, message=str(exc)[:300])


class Handler(BaseHTTPRequestHandler):
    server_version = "CapitologyReview/0.1"

    def authorized(self) -> bool:
        if not PASSWORD:
            return True
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return False
        try:
            raw = base64.b64decode(auth[6:], validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            return False
        return hmac.compare_digest(raw, "player:" + PASSWORD)

    def require_auth(self) -> bool:
        if self.authorized():
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Private match reviews"')
        self.send_header("Content-Length", "0")
        self.end_headers()
        return False

    def json_response(self, status: int, obj: dict) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def serve_file(self, path: Path, content_type: str, ranged: bool = False) -> None:
        if not path.is_file():
            self.send_error(404)
            return
        size = path.stat().st_size
        start, end = 0, size - 1
        raw_range = self.headers.get("Range") if ranged else None
        if raw_range:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", raw_range.strip())
            if not match:
                self.send_error(416)
                return
            if match.group(1):
                start = int(match.group(1))
                end = min(int(match.group(2)), size - 1) if match.group(2) else end
            elif match.group(2):
                start = max(0, size - int(match.group(2)))
            if start >= size or end < start:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
        self.send_response(206 if raw_range else 200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes" if ranged else "none")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if raw_range:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with path.open("rb") as f:
            f.seek(start)
            remaining = end - start + 1
            while remaining:
                chunk = f.read(min(256 * 1024, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    break
                remaining -= len(chunk)

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/healthz":
            self.json_response(200, {"ok": True})
            return
        if not self.require_auth():
            return
        if path == "/":
            self.serve_file(HERE / "static/index.html", "text/html; charset=utf-8")
            return
        if path == "/app.css":
            self.serve_file(HERE / "static/app.css", "text/css; charset=utf-8")
            return
        if path == "/app.js":
            self.serve_file(HERE / "static/app.js", "text/javascript; charset=utf-8")
            return
        parts = path.strip("/").split("/")
        if len(parts) >= 3 and parts[:2] == ["api", "jobs"]:
            try:
                job = read_job(parts[2])
            except (FileNotFoundError, ValueError):
                self.send_error(404)
                return
            if len(parts) == 3:
                self.json_response(200, job)
            elif len(parts) == 4 and parts[3] == "report":
                report = job_path(parts[2]) / "report.json"
                if report.is_file():
                    self.serve_file(report, "application/json; charset=utf-8")
                else:
                    self.json_response(404, {"error": "Report is not ready"})
            elif len(parts) == 4 and parts[3] == "video":
                suffix = Path(job["source_file"]).suffix.lower()
                self.serve_file(job_path(parts[2]) / job["source_file"],
                                {".mp4": "video/mp4", ".mov": "video/quicktime",
                                 ".webm": "video/webm", ".mkv": "video/x-matroska"}.get(suffix, "application/octet-stream"),
                                ranged=True)
            else:
                self.send_error(404)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if not self.require_auth():
            return
        parts = urlsplit(self.path).path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "jobs"] and parts[3] == "feedback":
            try:
                job = read_job(parts[2])
            except (FileNotFoundError, ValueError):
                self.send_error(404)
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 4096 or job["status"] not in {"complete", "insufficient_evidence"}:
                    raise ValueError("Feedback is unavailable for this job")
                payload = json.loads(self.rfile.read(size))
                kind = payload.get("kind")
                if kind not in {"wrong_player", "wrong_pov", "missed_information", "intentional_choice", "other"}:
                    raise ValueError("Choose a correction type")
                note = str(payload.get("note", "")).strip()[:1000]
                if not note:
                    raise ValueError("Describe the correction")
                at = float(payload.get("at_seconds", 0))
                if not 0 <= at <= job["duration_seconds"]:
                    raise ValueError("Timestamp is outside the recording")
            except (ValueError, TypeError, AttributeError, KeyError):
                self.json_response(400, {"error": "Provide a valid correction, timestamp, and note"})
                return
            feedback = {"id": uuid.uuid4().hex, "created_at": timestamp(),
                        "kind": kind, "at_seconds": at, "note": note}
            write_json(job_path(parts[2]) / "feedback" / (feedback["id"] + ".json"), feedback)
            self.json_response(201, {"saved": True})
            return
        if urlsplit(self.path).path != "/api/jobs":
            self.send_error(404)
            return
        if not os.getenv("OPENAI_API_KEY"):
            self.json_response(503, {"error": "Analysis service is not configured yet"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if not 0 < length <= MAX_UPLOAD:
            self.json_response(413, {"error": "Recording exceeds upload limit or has no content"})
            return
        suffix = Path(self.headers.get("X-Filename", "")).suffix.lower()
        if suffix not in ALLOWED:
            self.json_response(415, {"error": "Use MP4, MOV, MKV, or WebM recording"})
            return
        player = {field: self.headers.get("X-Player-" + field.title(), "").strip()[:100]
                  for field in ("hero", "role", "team", "perspective", "concern")}
        if not player["perspective"]:
            player["perspective"] = "unknown"
        job_id = uuid.uuid4().hex
        folder = job_path(job_id)
        folder.mkdir(parents=True)
        source = "source" + suffix
        digest = hashlib.sha256()
        try:
            with (folder / source).open("wb") as f:
                remaining = length
                while remaining:
                    chunk = self.rfile.read(min(1024 * 1024, remaining))
                    if not chunk:
                        raise ConnectionError("Upload ended early")
                    f.write(chunk)
                    digest.update(chunk)
                    remaining -= len(chunk)
            meta = probe(folder / source)
        except Exception as exc:
            shutil.rmtree(folder, ignore_errors=True)
            self.json_response(422, {"error": f"Could not read the recording: {str(exc)[:200]}"})
            return
        job = {"id": job_id, "status": "queued", "percentage": 0, "message": "Queued for analysis",
               "created_at": timestamp(), "updated_at": timestamp(), "source_file": source,
               "sha256": digest.hexdigest(), "duration_seconds": meta["duration_seconds"],
               "size_bytes": meta["size_bytes"], "player": player}
        write_json(folder / "job.json", job)
        POOL.submit(work, job_id)
        self.json_response(201, job)

    def do_DELETE(self) -> None:
        if not self.require_auth():
            return
        parts = urlsplit(self.path).path.strip("/").split("/")
        if len(parts) != 3 or parts[:2] != ["api", "jobs"]:
            self.send_error(404)
            return
        try:
            job = read_job(parts[2])
        except (FileNotFoundError, ValueError):
            self.send_error(404)
            return
        if job["status"] not in {"complete", "insufficient_evidence", "failed"}:
            self.json_response(409, {"error": "Wait for processing to finish before deleting"})
            return
        shutil.rmtree(job_path(parts[2]))
        self.json_response(200, {"deleted": True})


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8080")))
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not PASSWORD:
        raise SystemExit("Set MATCH_REVIEW_PASSWORD before binding to a network interface")
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"Missing {binary}")
    DATA.mkdir(parents=True, exist_ok=True)
    # A process restart requeues unfinished jobs after their upload has completed.
    for p in DATA.glob("*/job.json"):
        try:
            job = json.loads(p.read_text())
            if job["status"] not in {"complete", "insufficient_evidence", "failed"}:
                POOL.submit(work, job["id"])
        except (ValueError, KeyError):
            continue
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Match review listening at http://{args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
