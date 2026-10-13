"""WSGI configuration template for a free PythonAnywhere US account.

Place reviewed app source at ~/stepstone and create ~/stepstone-records first.
Copy this file into the WSGI configuration linked from the host's Web page.
The account name is obtained on that host; no credential belongs in this file.
Enable Force HTTPS and keep one web worker. For the EU system, change the
address suffix below to .eu.pythonanywhere.com.
"""
import atexit
from pathlib import Path
import sys

account_home = Path.home()
sys.path.insert(0, str(account_home / 'stepstone'))
from wsgi_app import create_wsgi_app

application = create_wsgi_app(
    public_url='https://' + account_home.name + '.pythonanywhere.com',
    data=account_home / 'stepstone-records')
atexit.register(application.close)
