"""Narration must not bypass request boundaries or write learning records."""
import base64
import io
import json
import queue
import tempfile
import unittest
import urllib.error
import urllib.request
import wave
from unittest.mock import patch
import test_server as fixtures
from voice import VoiceEngine, VoiceError


def wav_sample():
    output=io.BytesIO()
    with wave.open(output,'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000)
        wav.writeframes(b'\0\0'*240)
    return output.getvalue()


class VoiceRouteTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown

    def test_guest_narration_is_audio_without_record_changes(self):
        with self.app.store.db() as db: before=list(db.iterdump())
        audio=wav_sample()
        with patch.object(self.app.voice,'speak',return_value=audio) as speak:
            req=urllib.request.Request(self.url+'/api/read-aloud',data=json.dumps({'text':'Add one carton.'}).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.headers['Content-Type'],'audio/wav')
                self.assertEqual(response.headers['Cache-Control'],'no-store')
                self.assertEqual(response.read(),audio)
            speak.assert_called_once_with('Add one carton.')
        with self.app.store.db() as db: self.assertEqual(list(db.iterdump()),before)

    def test_request_boundaries_and_unavailable_voice(self):
        with patch.object(self.app.voice,'speak') as speak:
            for headers in ({'Origin':'https://unrelated.example'},{'Host':'unrelated.example'}):
                self.assertEqual(self.mentor.request('/api/read-aloud',{'text':'Hello'},headers)[0],403)
            speak.assert_not_called()
        for text in (None,'',' ',7,'x'*601):
            self.assertEqual(self.mentor.request('/api/read-aloud',{'text':text})[0],400)
        with patch.object(self.app.voice,'speak',side_effect=VoiceError('Not installed')):
            status,body,_=self.mentor.request('/api/read-aloud',{'text':'Hello'})
            self.assertEqual(status,503);self.assertEqual(body['error'],'Not installed')


class VoiceWorkerTests(unittest.TestCase):
    def test_cache_reuses_audio_and_invalid_output_is_not_cached(self):
        voice=VoiceEngine();audio=wav_sample()
        with patch.object(VoiceEngine,'available',new_callable=unittest.mock.PropertyMock,return_value=True),patch.object(voice,'start'),patch.object(voice,'close') as close:
            voice.process=unittest.mock.Mock();voice.replies=queue.Queue()
            voice.replies.put(json.dumps({'audio':base64.b64encode(audio).decode()}))
            self.assertEqual(voice.speak('Hello'),audio)
            self.assertEqual(voice.speak('Hello'),audio)
            voice.process.stdin.write.assert_called_once()
            voice.replies.put(json.dumps({'audio':'bm90LWF1ZGlv'}))
            with self.assertRaises(VoiceError):voice.speak('Other text')
            close.assert_called_once();self.assertEqual(len(voice.cache),1)

    def test_missing_optional_runtime_does_not_launch_any_process(self):
        with tempfile.TemporaryDirectory(prefix='stepstone-voice-test-') as folder:
            voice=VoiceEngine(folder)
            self.assertFalse(voice.available)
            with patch('voice.subprocess.Popen') as launch:
                with self.assertRaises(VoiceError):voice.speak('Hello')
                launch.assert_not_called()


if __name__=='__main__':unittest.main()
