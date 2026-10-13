"""Start the shared pilot behind a host's HTTPS proxy, with durable storage."""
import os
import signal
import sys
import threading
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from server import create_server


def main():
    address=os.environ.get('STEPSTONE_PUBLIC_URL') or os.environ.get('RENDER_EXTERNAL_URL','')
    data=os.environ.get('STEPSTONE_DATA_DIR','')
    if not address or not data or not Path(data).is_absolute():
        raise SystemExit('Configure the HTTPS app address and an absolute persistent STEPSTONE_DATA_DIR first.')
    if not Path(data).is_dir():
        raise SystemExit('STEPSTONE_DATA_DIR does not exist. Use a folder on the persistent disk; Stepstone will not create an empty one there.')
    existing=(Path(data)/'stepstone.sqlite3').is_file()
    app=create_server(host='0.0.0.0',port=int(os.environ.get('PORT','10000')),
                      data=data,secure=True,public_url=address,trust_forwarded=True)
    def stop(*_):
        threading.Thread(target=app.shutdown,daemon=True).start()
    signal.signal(signal.SIGTERM,stop)
    print('Stepstone shared host ready. '+('Opened the existing records in' if existing else 'Started a NEW empty database in')+' the configured persistent directory.',flush=True)
    try:app.serve_forever()
    except KeyboardInterrupt:pass
    finally:app.server_close()


if __name__=='__main__':main()
