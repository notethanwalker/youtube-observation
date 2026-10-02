"""End-to-end transport test; fake model responses do not validate coaching quality."""
import base64
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import unittest
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from match_review import analysis, server


class FakeResponses(BaseHTTPRequestHandler):
    calls = []
    quota_once = False
    rate_once = False

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        content = payload['input'][0]['content']
        self.__class__.calls.append(payload)
        if self.__class__.quota_once:
            self.__class__.quota_once = False
            raw = json.dumps({'error': {'code': 'credit_balance_exhausted',
                                        'type': 'insufficient_quota',
                                        'message': 'No prepaid API credit'}}).encode()
            self.send_response(429)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        if self.__class__.rate_once:
            self.__class__.rate_once = False
            raw = json.dumps({'error': {'code': 'rate_limit_exceeded', 'message': 'Too many requests'}}).encode()
            self.send_response(429)
            self.send_header('Retry-After', '1')
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        assert content[1]['image_url'].startswith('data:image/jpeg;base64,')
        assert base64.b64decode(content[1]['image_url'].split(',', 1)[1]).startswith(b'\xff\xd8')
        assert payload['text']['format']['strict'] is True
        if payload['text']['format']['name'] == 'match_candidates':
            value = {'overview': 'One changing scene in sampled frames.', 'candidates': [
                {'start_seconds': 1, 'end_seconds': 15, 'score': 5,
                 'visible_change': 'Turn and positioning shift', 'review_reason': 'Inspect the turn',
                 'uncertainty': 'Motion between frames unseen'}]}
        else:
            ids = re.findall(r'CAP-\d\d', content[0]['text'])
            value = {'reviewable': True, 'title': 'Position before the turn',
                     'start_seconds': 2, 'end_seconds': 12, 'player_evidence': 'POV identified from metadata and HUD',
                     'situation': 'Visible contested space', 'player_action': 'Moves to a new angle',
                     'visible_response': 'Opposing view shifts', 'observed': 'The view changes position across frames',
                     'interpretation': 'The timing may expose a response', 'impact_reason': 'A turn has a limited window',
                     'alternative': 'Check the adjacent angle first', 'when_alternative_fails': 'If immediate pressure is needed',
                     'confidence': 'high', 'uncertainty': 'Motion between frames unseen',
                     'rule_ids': [ids[0]], 'impact': 3, 'positive': False}
        raw = json.dumps({'output': [{'content': [{'type': 'output_text', 'text': json.dumps(value)}]}]}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass


class MatchReviewTest(unittest.TestCase):
    def test_upload_analysis_report_and_feedback(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            clip = folder / 'clip.mp4'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
                            '-i', 'testsrc2=size=320x180:rate=1', '-t', '16', '-c:v', 'mpeg4',
                            str(clip)], check=True)
            FakeResponses.calls = []
            fake = ThreadingHTTPServer(('127.0.0.1', 0), FakeResponses)
            local = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            old = (server.DATA, server.PASSWORD, analysis.API_URL, os.getenv('OPENAI_API_KEY'))
            server.DATA = folder / 'jobs'
            server.PASSWORD = 'secret'
            analysis.API_URL = f'http://127.0.0.1:{fake.server_port}/responses'
            os.environ['OPENAI_API_KEY'] = 'test-only'
            for instance in (fake, local):
                threading.Thread(target=instance.serve_forever, daemon=True).start()
            root = f'http://127.0.0.1:{local.server_port}'
            def call(method, path, body=None, headers=None, authorized=True):
                conn = HTTPConnection('127.0.0.1', local.server_port, timeout=30)
                headers = dict(headers or {})
                if authorized:
                    headers['Authorization'] = 'Basic ' + base64.b64encode(b'player:secret').decode()
                if isinstance(body, dict):
                    body = json.dumps(body).encode()
                    headers['Content-Type'] = 'application/json'
                conn.request(method, path, body=body, headers=headers)
                response = conn.getresponse()
                status, raw = response.status, response.read()
                conn.close()
                return status, raw
            try:
                self.assertEqual(call('GET', '/', authorized=False)[0], 401)
                self.assertEqual(call('GET', '/')[0], 200)
                status, raw = call('POST', '/api/jobs', clip.read_bytes(),
                                   {'X-Filename': 'match.mp4', 'X-Player-Hero': 'Winston'})
                self.assertEqual(status, 201, raw)
                job_id = json.loads(raw)['id']
                for _ in range(100):
                    job = json.loads(call('GET', f'/api/jobs/{job_id}')[1])
                    if job['status'] in ('complete', 'insufficient_evidence', 'failed'):
                        break
                    time.sleep(.1)
                self.assertEqual(job['status'], 'complete', job)
                report = json.loads(call('GET', f'/api/jobs/{job_id}/report')[1])
                self.assertEqual(len(report['findings']), 1)
                self.assertEqual(report['findings'][0]['confidence'], 'moderate')
                self.assertTrue(report['findings'][0]['rule_sources'][0]['sources'][0]['url'])
                self.assertEqual(len(FakeResponses.calls), 2)
                self.assertFalse((server.DATA / job_id / 'frames').exists())
                status, raw = call('GET', f'/api/jobs/{job_id}/video', headers={'Range': 'bytes=0-99'})
                self.assertEqual(status, 206)
                self.assertEqual(raw, clip.read_bytes()[:100])
                status, raw = call('POST', f'/api/jobs/{job_id}/feedback',
                    {'kind': 'wrong_player', 'at_seconds': 5, 'note': 'Wrong POV'})
                self.assertEqual(status, 201, raw)
                self.assertEqual(len(list((server.DATA / job_id / 'feedback').glob('*.json'))), 1)
                self.assertEqual(call('DELETE', f'/api/jobs/{job_id}', authorized=False)[0], 401)
                self.assertEqual(call('DELETE', f'/api/jobs/{job_id}')[0], 200)
                self.assertEqual(call('GET', f'/api/jobs/{job_id}')[0], 404)
                FakeResponses.quota_once = True
                status, raw = call('POST', '/api/jobs', clip.read_bytes(), {'X-Filename': 'match.mp4'})
                self.assertEqual(status, 201, raw)
                retry_id = json.loads(raw)['id']
                for _ in range(100):
                    failed = json.loads(call('GET', f'/api/jobs/{retry_id}')[1])
                    if failed['status'] == 'failed':
                        break
                    time.sleep(.1)
                self.assertEqual(failed['status'], 'failed', failed)
                self.assertIn('billing balance', failed['message'])
                self.assertEqual(call('POST', f'/api/jobs/{retry_id}/retry')[0], 202)
                for _ in range(100):
                    retried = json.loads(call('GET', f'/api/jobs/{retry_id}')[1])
                    if retried['status'] in ('complete', 'insufficient_evidence', 'failed'):
                        break
                    time.sleep(.1)
                self.assertEqual(retried['status'], 'complete', retried)
                self.assertEqual(call('GET', f'/api/jobs/{retry_id}/report')[0], 200)
                self.assertEqual(call('DELETE', f'/api/jobs/{retry_id}')[0], 200)
                FakeResponses.rate_once = True
                status, raw = call('POST', '/api/jobs', clip.read_bytes(), {'X-Filename': 'match.mp4'})
                self.assertEqual(status, 201, raw)
                rate_id = json.loads(raw)['id']
                for _ in range(100):
                    rate_job = json.loads(call('GET', f'/api/jobs/{rate_id}')[1])
                    if rate_job['status'] in ('complete', 'insufficient_evidence', 'failed'):
                        break
                    time.sleep(.1)
                self.assertEqual(rate_job['status'], 'complete', rate_job)
                self.assertEqual(call('DELETE', f'/api/jobs/{rate_id}')[0], 200)
            finally:
                for instance in (local, fake):
                    instance.shutdown()
                    instance.server_close()
                server.DATA, server.PASSWORD, analysis.API_URL, original_key = old
                if original_key is None:
                    os.environ.pop('OPENAI_API_KEY', None)
                else:
                    os.environ['OPENAI_API_KEY'] = original_key


if __name__ == '__main__':
    unittest.main()
