"""Run the existing Stepstone routes on a one-worker WSGI host.

No listener, background thread, external database or new authentication stack
is created. Set the host's HTTPS-only switch before inviting real users.
"""
from email.message import Message
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import quote, urlparse
from wsgiref.util import is_hop_by_hop

from host_runtime import shared_address
from server import Handler, PUBLIC, ROOT, configure_server
from voice import VoiceError


class LocalVoiceOnly:
    available = False

    def speak(self, _text):
        raise VoiceError('This host uses local device voices. Choose a local voice in your profile.')

    def close(self):
        pass


class WSGIHandler(Handler):
    def __init__(self, context, environ):
        # Reuse dispatch, authorization, grading and file allowlisting directly.
        # BaseHTTPRequestHandler.__init__ would try to read a socket.
        self.server = context
        self.directory = str(PUBLIC)
        self.client_address = (environ.get('REMOTE_ADDR') or 'unknown', 0)
        self.command = environ.get('REQUEST_METHOD', 'GET').upper()
        path = environ.get('PATH_INFO', '/') or '/'
        # WSGI decodes path bytes as latin-1. Restore UTF-8 before URL quoting.
        try:
            path = path.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        self.path = quote(path, safe='/')
        query = environ.get('QUERY_STRING', '')
        if query:
            self.path += '?' + query
        self.request_version = 'HTTP/1.1'
        self.requestline = self.command + ' ' + self.path + ' HTTP/1.1'
        self.close_connection = True
        self.headers = Message()
        for key, value in environ.items():
            if key.startswith('HTTP_') and key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH') and isinstance(value, str):
                self.headers[key[5:].replace('_', '-')] = value
        for key, name in [('CONTENT_TYPE', 'Content-Type'), ('CONTENT_LENGTH', 'Content-Length')]:
            if key in environ:
                self.headers[name] = str(environ[key])
        if not self.headers.get('Host'):
            self.headers['Host'] = environ.get('SERVER_NAME', '')
        self.rfile = environ['wsgi.input']
        self.wfile = BytesIO()
        self.status = 200
        self.reason = 'OK'
        self.response_headers = []

    def log_message(self, *_args):
        # The provider owns access logs. Never log learner content or tokens here.
        pass

    def send_response(self, code, message=None):
        self.status = code
        self.reason = message or self.responses.get(code, ('Unknown',))[0]
        self.response_headers = [('Date', self.date_time_string())]

    def send_header(self, keyword, value):
        if not is_hop_by_hop(keyword):
            self.response_headers.append((keyword, str(value)))

    def end_headers(self):
        self.security_headers()


class StepstoneApplication:
    def __init__(self, public_url, data):
        address = shared_address(public_url, True)
        if not address:
            raise ValueError('Configure the canonical HTTPS app address first.')
        directory = Path(data)
        if not directory.is_absolute() or not directory.is_dir():
            raise ValueError('Create an absolute persistent records directory before starting the app.')
        directory = directory.resolve()
        if directory.is_relative_to(ROOT.resolve()):
            raise ValueError('Keep the persistent records directory outside the uploaded app source.')
        self.context = configure_server(
            SimpleNamespace(server_address=('wsgi', 443)), data=directory,
            secure=True, public_url=address, trust_forwarded=True, voice=LocalVoiceOnly())
        # Public WSGI requests can never claim legacy records or manage a laptop.
        self.context.local_hosts = set()
        self.context.allowed_hosts = {urlparse(address).netloc}

    def __call__(self, environ, start_response):
        handler = WSGIHandler(self.context, environ)
        try:
            # A clear-origin mutation on this host must originate from HTTPS.
            origin = handler.headers.get('Origin')
            if handler.command == 'POST' and origin and origin != self.context.public_url:
                handler.respond({'error': 'Request origin does not match this app.'}, 403)
            elif handler.command in ('GET', 'HEAD', 'POST'):
                getattr(handler, 'do_' + handler.command)()
            else:
                handler.respond({'error': 'This request method is not supported.'}, 405)
                handler.send_header('Allow', 'GET, HEAD, POST')
        except Exception:
            # Do not send exception details, local paths or private records to clients.
            handler.wfile = BytesIO()
            handler.respond({'error': 'The request did not finish. Please try again.'}, 500)
        # No scheduled task or thread is needed. A visited workspace gets its
        # consistent daily recovery copy after the database transaction closes.
        try:
            handler.store.backups.tick(background=False)
        except Exception:
            handler.store.backups.error = 'Automatic recovery copies stopped. Check host storage.'
        body = handler.wfile.getvalue() if handler.command != 'HEAD' else b''
        start_response(f'{handler.status} {handler.reason}', handler.response_headers)
        return [body]

    def close(self):
        self.context.voice.close()
        for store in self.context.accounts.stores:
            store.backups.close()


def create_wsgi_app(*, public_url, data):
    return StepstoneApplication(public_url, data)
