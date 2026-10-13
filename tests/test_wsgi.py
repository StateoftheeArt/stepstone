"""Exercise real Stepstone routes through WSGI using disposable records."""
from http.cookies import SimpleCookie
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

import test_server as base
from wsgi_app import create_wsgi_app

ADDRESS = 'https://stepstone-pilot.pythonanywhere.com'


class WSGIClient:
    def __init__(self, app):
        self.app = app
        self.cookies = {}

    def request(self, path, data=None, headers=None, method=None, body=None, **environment):
        environ = {}
        setup_testing_defaults(environ)
        raw = body if body is not None else json.dumps(data).encode() if data is not None else b''
        environ.update(REQUEST_METHOD=method or ('POST' if data is not None or body is not None else 'GET'),
                       PATH_INFO=path, QUERY_STRING='', SERVER_NAME='stepstone-pilot.pythonanywhere.com',
                       HTTP_HOST='stepstone-pilot.pythonanywhere.com', REMOTE_ADDR='127.0.0.1',
                       HTTP_X_FORWARDED_FOR='spoofed-client, 198.51.100.10',
                       CONTENT_LENGTH=str(len(raw)), CONTENT_TYPE='application/json',
                       HTTP_COOKIE='; '.join(k + '=' + v for k, v in self.cookies.items()),
                       **{'wsgi.url_scheme': 'https', 'wsgi.input': BytesIO(raw)})
        for name, value in (headers or {}).items():
            key = name.upper().replace('-', '_')
            environ[key if key in ('CONTENT_TYPE', 'CONTENT_LENGTH') else 'HTTP_' + key] = value
        environ.update(environment)
        response = {}

        def start(status, fields, exc_info=None):
            response.update(status=int(status.split()[0]), headers=fields)

        result = validator(self.app)(environ, start)
        try:
            raw_result = b''.join(result)
        finally:
            if hasattr(result, 'close'):
                result.close()
        for key, value in response['headers']:
            if key.lower() == 'set-cookie':
                parsed = SimpleCookie(value)
                for name, cookie in parsed.items():
                    if cookie['max-age'] == '0':
                        self.cookies.pop(name, None)
                    else:
                        self.cookies[name] = cookie.value
        try:
            payload = json.loads(raw_result)
        except ValueError:
            payload = raw_result
        return response['status'], payload, response['headers']


class WSGITests(unittest.TestCase):
    def setUp(self):
        scratch = (Path(__file__).resolve().parents[2] / '.test-output').resolve()
        if not scratch.is_relative_to(Path(__file__).resolve().parents[2]):
            raise ValueError('Disposable records must stay in the candidate workspace.')
        scratch.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='stepstone-wsgi-', dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.app = create_wsgi_app(public_url=ADDRESS, data=self.tmp.name)
        self.mentor = WSGIClient(self.app)
        status, self.account, _ = self.mentor.request('/api/mentor/setup', dict(
            username='wsgi-mentor', name='Test mentor', device='Test browser',
            passphrase='test-only-wsgi-passphrase'))
        self.assertEqual(status, 200, self.account)

    def tearDown(self):
        self.app.close()
        self.tmp.cleanup()

    def learner(self):
        status, invite, _ = self.mentor.request('/api/mentor/invite', {})
        self.assertEqual(status, 200)
        self.assertTrue(invite['url'].startswith(ADDRESS + '/#join/'))
        learner = WSGIClient(self.app)
        status, person, _ = learner.request('/api/join', dict(code=invite['code'], alias='Test learner', share=True))
        self.assertEqual(status, 200, person)
        base.complete_tutorial(learner)
        return learner, person

    def test_mentor_report_feedback_and_restart_keep_real_route_records(self):
        learner, person = self.learner()
        status, attempt, _ = learner.request('/api/attempt', dict(unit='math-1'))
        self.assertEqual(status, 200, attempt)
        self.assertTrue(all('answer' not in q and 'explanation' not in q for q in attempt['questions']))
        status, report, _ = learner.request('/api/submit', dict(
            id=attempt['id'], answers=base.right_answers('math-1', attempt),
            reflection='Fictional WSGI fixture: I counted the packed cartons and checked the difference.',
            support='myself', ink=[], practiceRetries=0))
        self.assertEqual(status, 200, report)
        self.assertEqual(report['report']['score'], 6)
        status, dashboard, _ = self.mentor.request('/api/mentor')
        self.assertEqual(status, 200)
        self.assertEqual(dashboard['reports'][0]['id'], attempt['id'])
        note = 'Try a different order and explain what changes.'
        self.assertEqual(self.mentor.request('/api/mentor/review', dict(id=attempt['id'], note=note))[0], 200)
        self.assertEqual(learner.request('/api/me')[1]['attempts'][0]['note'], note)
        self.app.close()
        self.app = create_wsgi_app(public_url=ADDRESS, data=self.tmp.name)
        self.mentor.app = self.app
        learner.app = self.app
        self.assertEqual(self.mentor.request('/api/mentor')[1]['reports'][0]['note'], note)
        self.assertEqual(learner.request('/api/me')[1]['id'], person['id'])
        self.assertEqual(learner.request('/api/me')[1]['attempts'][0]['note'], note)

    def test_groups_are_private_and_new_browser_needs_approval(self):
        learner, person = self.learner()
        second = WSGIClient(self.app)
        self.assertEqual(second.request('/api/mentor/setup', dict(
            username='other-wsgi-mentor', name='Other mentor', device='Other browser',
            passphrase='other-test-only-passphrase'))[0], 200)
        self.assertEqual(second.request('/api/mentor')[1]['learners'], [])
        self.assertEqual(second.request('/api/mentor/recovery', dict(id=person['id']))[0], 404)
        fresh = WSGIClient(self.app)
        status, pending, _ = fresh.request('/api/mentor/login', dict(
            username='wsgi-mentor', passphrase='test-only-wsgi-passphrase', device='New browser'))
        self.assertEqual(status, 200)
        self.assertTrue(pending['pending'])
        self.assertEqual(fresh.request('/api/mentor')[0], 401)
        request = self.mentor.request('/api/mentor')[1]['requests'][0]
        self.assertEqual(request['code'], pending['code'])
        self.assertEqual(self.mentor.request('/api/mentor/device-review', dict(id=request['id'], status='approved'))[0], 200)
        self.assertTrue(fresh.request('/api/mentor/device-status', {})[1]['ok'])
        self.assertEqual(fresh.request('/api/mentor')[1]['account']['username'], 'wsgi-mentor')
        self.assertEqual(learner.request('/api/me')[1]['id'], person['id'])

    def test_secure_cookies_no_private_static_files_and_head_has_no_body(self):
        self.assertTrue(self.mentor.cookies['stepstone_mentor'])
        other = WSGIClient(self.app)
        status, _, headers = other.request('/api/mentor/setup', dict(
            username='cookie-test', name='Cookie test', device='Cookie browser',
            passphrase='cookie-test-only-passphrase'))
        self.assertEqual(status, 200)
        for _, value in [pair for pair in headers if pair[0].lower() == 'set-cookie']:
            for flag in ('Secure', 'HttpOnly', 'SameSite=Strict'):
                self.assertIn(flag, value)
        for path in ('/data/stepstone.sqlite3', '/content/checkpoints.json', '/server.py', '/vendor/', '/../server.py'):
            self.assertEqual(other.request(path)[0], 404, path)
        status, body, headers = other.request('/index.html', method='HEAD')
        self.assertEqual(status, 200)
        self.assertEqual(body, b'')
        self.assertEqual(dict(headers)['X-Frame-Options'], 'DENY')
        self.assertIn("frame-ancestors 'none'", dict(headers)['Content-Security-Policy'])
        self.assertFalse(any(k.lower() in ('connection', 'transfer-encoding') for k, _ in headers))
        self.assertEqual(WSGIClient(self.app).request('/api/me')[0], 401)

    def test_host_origin_request_size_and_content_type_guards(self):
        for headers in ({'Host': 'bad.example'}, {'Origin': 'https://bad.example'}, {'Origin': ADDRESS.replace('https:', 'http:')}):
            self.assertEqual(self.mentor.request('/api/mentor/invite', {}, headers=headers)[0], 403)
        self.assertEqual(self.mentor.request('/api/mentor/invite', {}, headers={'Content-Type': 'text/plain'})[0], 415)
        class Unreadable(BytesIO):
            def read(self, *_):
                raise AssertionError('Oversized request body was read')
        status, _, _ = self.mentor.request('/api/mentor/invite', {}, CONTENT_LENGTH='180001', **{'wsgi.input': Unreadable()})
        self.assertEqual(status, 413)
        self.assertEqual(self.mentor.request('/api/mentor/invite', body=b'{invalid')[0], 400)
        self.assertEqual(self.mentor.request('/index.html', method='DELETE')[0], 405)

    def test_proxy_loopback_cannot_claim_existing_data_or_manage_host(self):
        client = WSGIClient(self.app)
        status, health, _ = client.request('/api/health')
        self.assertEqual(status, 200)
        self.assertFalse(health['localClaim'])
        self.assertEqual(client.request('/api/mentor/setup', dict(
            username='claim-test', name='Claim test', device='Claim browser',
            passphrase='claim-test-only-passphrase', claimExisting=True),
            headers={'X-Forwarded-For': '127.0.0.1, 198.51.100.11'})[0], 403)
        settings = self.mentor.request('/api/mentor')[1]['settings']
        self.assertFalse(settings['desktop'])
        self.assertFalse(settings['canManageHost'])
        self.assertEqual(self.mentor.request('/api/mentor/settings', dict(keepRunning=False))[0], 403)

    def test_local_device_voice_and_synchronous_recovery_need_no_threads(self):
        self.assertFalse(self.mentor.request('/api/health')[1]['softVoice'])
        self.assertEqual(self.mentor.request('/api/read-aloud', dict(text='Fictional voice fixture'))[0], 503)
        store = self.app.context.accounts.by_name['wsgi-mentor']
        self.assertTrue(store.backups.records())
        self.assertIsNone(store.backups.worker)
        self.assertEqual(self.mentor.request('/api/mentor/backup', {})[0], 200)
        self.assertFalse(store.backups.error)

    def test_invalid_data_configuration_never_creates_new_empty_folder(self):
        missing = Path(self.tmp.name) / 'missing'
        with self.assertRaises(ValueError):
            create_wsgi_app(public_url=ADDRESS, data=missing)
        self.assertFalse(missing.exists())
        for address in ('', 'http://example.com', 'https://localhost'):
            with self.assertRaises(ValueError):
                create_wsgi_app(public_url=address, data=self.tmp.name)
        with self.assertRaises(ValueError):
            create_wsgi_app(public_url=ADDRESS, data=base.server.ROOT)

    def test_gateway_errors_do_not_disclose_private_details(self):
        with patch('wsgi_app.WSGIHandler.do_GET', side_effect=RuntimeError('private fixture detail')):
            status, result, _ = self.mentor.request('/api/me')
        self.assertEqual(status, 500)
        self.assertNotIn('private fixture detail', json.dumps(result))


if __name__ == '__main__':
    unittest.main()
