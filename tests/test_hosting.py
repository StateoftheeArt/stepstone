"""Packaging and HTTPS-proxy contract. This does not claim an internet deployment."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
import zipfile
import test_server as base
from tools.package_hosting import package


class HostingTests(unittest.TestCase):
    def test_allowlisted_package_runs_without_private_workspace_files(self):
        with tempfile.TemporaryDirectory(prefix='stepstone-package-') as tmp:
            root=Path(tmp);archive=root/'host.zip'
            receipt=package(archive)
            self.assertFalse(receipt['privateRecordsIncluded'])
            with zipfile.ZipFile(archive) as z:
                names=z.namelist()
                self.assertFalse(any(n.startswith(('data/','tests/')) or n.endswith('.sqlite3') for n in names))
                manifest=json.loads(z.read('DEPLOYMENT_MANIFEST.json'))
                self.assertIn('backups.py',manifest)
                self.assertIn('.python-version',manifest)
                self.assertEqual(z.read('.python-version').decode().strip(),'3.12')
                z.extractall(root/'app') # Locally created allowlisted archive only.
            proc=subprocess.run([sys.executable,'-B','server.py','--help'],cwd=root/'app',capture_output=True,text=True,timeout=20)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertIn('--public-url',proc.stdout)
            with self.assertRaises(ValueError):package(archive)

    def test_hosted_start_refuses_a_missing_data_folder(self):
        with tempfile.TemporaryDirectory(prefix='stepstone-hosted-') as tmp:
            missing=Path(tmp)/'typo-outside-the-disk'
            env={**os.environ,'STEPSTONE_PUBLIC_URL':'https://pilot.example.invalid','STEPSTONE_DATA_DIR':str(missing),'PORT':'0'}
            root=Path(__file__).resolve().parents[1]
            proc=subprocess.run([sys.executable,'-B','tools/hosted_server.py'],cwd=root,env=env,capture_output=True,text=True,timeout=20)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('does not exist',proc.stderr)
            self.assertFalse(missing.exists())

    def test_secure_cookie_canonical_link_and_remote_setup_boundary(self):
        with tempfile.TemporaryDirectory(prefix='stepstone-proxy-') as tmp:
            app=base.server.create_server(port=0,data=tmp,secure=True,public_url='https://pilot.example.invalid')
            t=threading.Thread(target=app.serve_forever,daemon=True);t.start()
            url=f'http://127.0.0.1:{app.server_address[1]}'
            c=base.Client(url)
            try:
                fields=dict(username='hosted-mentor',name='Hosted mentor',device='Test device',passphrase='test-only-passphrase')
                self.assertEqual(c.request('/api/mentor/setup',{**fields,'claimExisting':True},headers={'Host':'pilot.example.invalid'})[0],403)
                status,_,headers=c.request('/api/mentor/setup',fields,headers={'Host':'pilot.example.invalid'})
                self.assertEqual(status,200)
                cookie=headers['Set-Cookie']
                for flag in ('Secure','HttpOnly','SameSite=Strict'):self.assertIn(flag,cookie)
                # Test protocol explicitly, not a browser bypass or real TLS test.
                status,result,_=c.request('/api/mentor/invite',{},headers={'Host':'pilot.example.invalid','Origin':'https://pilot.example.invalid','Cookie':cookie.split(';',1)[0]})
                self.assertEqual(status,200)
                self.assertTrue(result['url'].startswith('https://pilot.example.invalid/#join/'))
                self.assertEqual(c.request('/api/mentor',headers={'Host':'bad.invalid'})[0],403)
                for path,host,expected in [('/index.html','bad.invalid',403),('/data/stepstone.sqlite3',f'127.0.0.1:{app.server_address[1]}',404)]:
                    req=urllib.request.Request(url+path,method='HEAD',headers={'Host':host})
                    try: response=urllib.request.urlopen(req)
                    except urllib.error.HTTPError as error: response=error
                    with response:self.assertEqual(response.status,expected);self.assertEqual(response.read(),b'')
            finally:app.shutdown();app.server_close();t.join()


if __name__=='__main__':unittest.main()
