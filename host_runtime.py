"""Desktop lifetime policy. Does not change networking, sleep or Windows startup."""
import time
from urllib.parse import urlparse


def shared_address(value, secure):
    if not value:
        return ''
    u = urlparse(value)
    if (not secure or u.scheme != 'https' or not u.hostname or u.username or
            u.password or u.query or u.fragment or u.path not in ('', '/') or
            u.hostname in ('localhost', '127.0.0.1', '::1')):
        raise ValueError('A shared address needs HTTPS, secure cookies, and an app hosted at the root of its own domain.')
    # Read port here as well: malformed ports must fail at startup, not in a link.
    _ = u.port
    return 'https://' + u.netloc.lower()


class HostRuntime:
    idle_seconds = 180

    def __init__(self, desktop=False, keep_running=True, clock=time.monotonic):
        self.desktop = desktop
        self.keep_running = keep_running
        self.clock = clock
        self.last_seen = clock()
        self.stopping = False

    def touch(self):
        self.last_seen = self.clock()

    def set_background(self, enabled):
        self.keep_running = enabled
        self.touch()  # Changing a preference never shuts the current page down.

    def due(self):
        return (self.desktop and not self.keep_running and not self.stopping and
                self.clock() - self.last_seen >= self.idle_seconds)
