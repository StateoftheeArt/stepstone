"""Private pipe worker: exits when the app closes its input. Never logs spoken text."""
import base64
import io
import json
from pathlib import Path
import sys
import wave
import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro

home = Path(sys.argv[1])
options = ort.SessionOptions()
options.intra_op_num_threads = 4
options.inter_op_num_threads = 1
options.log_severity_level = 3
# The full-precision model is much faster than INT8 on this Windows CPU.
session = ort.InferenceSession(str(home/'kokoro-v1.0.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
voice = Kokoro.from_session(session, str(home/'voices-v1.0.bin'))
for line in sys.stdin:
    try:
        text = json.loads(line)['text']
        if not isinstance(text, str) or not 0 < len(text) <= 600:
            raise ValueError('Invalid text length')
        samples, rate = voice.create(text, voice='af_heart', speed=.98, lang='en-us')
        target = io.BytesIO()
        with wave.open(target, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(rate)
            wav.writeframes((np.clip(samples, -1, 1)*32767).astype('<i2').tobytes())
        print(json.dumps({'audio':base64.b64encode(target.getvalue()).decode()}), flush=True)
    except Exception:
        print('{"error":"Voice generation failed"}', flush=True)
