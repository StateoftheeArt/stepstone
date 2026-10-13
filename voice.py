"""Optional local narration. No learner text is sent to a speech provider or saved."""
import base64
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
from collections import OrderedDict

ROOT = Path(__file__).resolve().parent


def voice_home():
    if os.environ.get('STEPSTONE_VOICE_HOME'):
        return Path(os.environ['STEPSTONE_VOICE_HOME'])
    try:
        return Path(json.loads((ROOT/'data/voice-runtime.json').read_text(encoding='utf-8-sig'))['home'])
    except (OSError, ValueError, KeyError):
        return Path(os.environ.get('LOCALAPPDATA', Path.home()/'.local/share'))/'Stepstone/voice'


class VoiceError(Exception):
    pass


class VoiceEngine:
    def __init__(self, home=None):
        self.home = Path(home) if home else voice_home()
        self.python = self.home/'runtime'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        self.lock = threading.Lock()
        self.process = None
        self.cache = OrderedDict()
        self.cache_size = 0

    @property
    def available(self):
        return all(p.is_file() for p in (self.python, self.home/'kokoro-v1.0.onnx', self.home/'voices-v1.0.bin'))

    def close(self):
        process, self.process = self.process, None
        if process:
            try:
                process.terminate()
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
            finally:
                for stream in (process.stdin, process.stdout):
                    if stream:
                        stream.close()

    def start(self):
        if self.process and self.process.poll() is None:
            return
        self.close()
        self.process = subprocess.Popen(
            [str(self.python), '-X', 'utf8', '-B', str(ROOT/'tools/voice_worker.py'), str(self.home)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding='utf-8', bufsize=1,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        replies = self.replies = queue.Queue()
        process = self.process
        def listen():
            try:
                for line in process.stdout:
                    replies.put(line)
            except (OSError, ValueError):
                pass
            finally:
                replies.put(None)
        threading.Thread(target=listen, daemon=True).start()

    def speak(self, text):
        if not isinstance(text, str) or not text.strip() or len(text) > 600:
            raise ValueError('Read a short section of up to 600 characters at a time.')
        if not self.available:
            raise VoiceError('The soft voice is not installed on this host. Choose a device voice in Reading & comfort.')
        if not self.lock.acquire(timeout=1):
            raise VoiceError('The voice is busy for a moment. Please try again.')
        try:
            key = hashlib.sha256(text.encode()).hexdigest()
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            self.start()
            try:
                self.process.stdin.write(json.dumps({'text': text})+'\n')
                self.process.stdin.flush()
                line = self.replies.get(timeout=40)
                result = json.loads(line) if line else {}
                audio = base64.b64decode(result.get('audio', ''), validate=True)
                if not audio.startswith(b'RIFF') or len(audio) > 6_000_000:
                    raise ValueError('Voice output was not audio.')
            except (OSError, ValueError, queue.Empty):
                self.close()
                raise VoiceError('The soft voice could not start. Try again, or choose a device voice in Reading & comfort.') from None
            self.cache[key] = audio
            self.cache_size += len(audio)
            while self.cache_size > 12_000_000:
                self.cache_size -= len(self.cache.popitem(last=False)[1])
            return audio
        finally:
            self.lock.release()
