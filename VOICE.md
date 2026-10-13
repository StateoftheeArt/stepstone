# Stepstone read-aloud

**Soft voice** is the default: Kokoro's American-English female **Heart (`af_heart`)** voice. The laptop generates narration locally; connected phones play the returned audio. It reads supplied lesson text and has no chat, grading, messaging, or reward permissions. No speech API key or subscription is used. Voice preference is saved in the existing Reading & comfort settings.

Read aloud works before onboarding is complete. **Stop reading**, another page, closing the voice sample, and hiding the page cancel playback. Audio is unlocked by the learner's tap. Longer text is split into short sections; the following section prepares during playback. A cancelled response cannot start playing late. Nothing speaks automatically on first open.

Soft voice needs a connection to the running Stepstone host. If it is unavailable, narration uses an English voice the browser identifies as local to the device. Online browser voices are not offered or used, including when an older saved preference selects one. If no local English voice is available, Stepstone keeps the text on screen and explains that narration is unavailable. The public browser demo uses only local device voices and never requests host narration.

## Host installation

On a Windows host, run from the Stepstone folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools\install-voice.ps1
```

The installer uses `python` from PATH, or an explicit `-PythonExecutable` path to create an isolated virtual environment. It installs `kokoro-onnx==0.6.1` and downloads the official model and voices, checking SHA-256 before use. Runtime/model files live under local app data, outside OneDrive and `public/`. `data/voice-runtime.json` records their resolved machine-specific location; run the installer on a different host to create that host's configuration. `STEPSTONE_VOICE_HOME` can explicitly override the location. The phone needs no model download or Python installation.

| File | Official release | SHA-256 |
|---|---|---|
| `kokoro-v1.0.onnx` | `model-files-v1.1` | `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a` |
| `voices-v1.0.bin` | `model-files-v1.1` | `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d` |

The full-precision model plus voices total about 354 MB, excluding the isolated Python packages. The worker uses four CPU threads. On the development i7-14650HX, the same roughly three-second greeting took 0.65 seconds to generate warm with this model, versus 12 seconds for the smaller INT8 model. Actual first browser playback, including cold process/model startup, took 3.23 seconds. Device load and text length affect timing. The unused INT8 model and temporary benchmark were removed.

## Data and process boundaries

`/api/read-aloud` applies the existing Host and Origin checks and accepts at most 600 characters. It returns `audio/wav` with `Cache-Control: no-store`; it does not open a learning-record write transaction. There is one serialized worker per app process, a 40-second generation timeout, and a bounded 12 MB in-memory audio cache. Spoken text/audio is not written to application logs or disk. The worker's input closes with its parent. Core lessons still run without the optional runtime.

Shared HTTPS hosting remains a separate pilot step. A public host must have its own voice runtime, capacity and request limits; the private Wi-Fi test does not establish public capacity or physical-phone compatibility.

## Sources and licences

- [Kokoro model card and Apache-2.0 licence](https://huggingface.co/hexgrad/Kokoro-82M), [voice reference](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).
- [kokoro-onnx source and MIT licence](https://github.com/thewh1teagle/kokoro-onnx), [official model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1).
- The installed runtime also includes its own dependencies and their licences, including [ONNX Runtime](https://github.com/microsoft/onnxruntime) and [eSpeak NG](https://github.com/espeak-ng/espeak-ng). These are installed locally, not relicensed as Stepstone code.

Voice pleasantness is for the learner to judge. Verification uses real generated audio decoded and started by native Web Audio in a mobile browser emulation; listening on the actual phone remains a user check. [verification scope](VERIFICATION.md).
