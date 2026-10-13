"""Run the repeatable release checks with disposable records only."""
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]

def main():
    node=shutil.which('node')
    if not node:
        raise SystemExit('Node.js 22 or newer is required for release checks; using Stepstone itself needs only Python.')
    report=[]
    scratch=(ROOT/'.test-output').resolve()
    if not scratch.is_relative_to(ROOT.resolve()):
        raise SystemExit('The disposable test folder is outside the source directory.')
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='release-',dir=scratch) as temporary:
        test_root=Path(temporary).resolve()
        if not test_root.is_relative_to(scratch):
            raise SystemExit('The disposable test run is outside its intended directory.')
        env={**os.environ,'TMP':str(test_root),'TEMP':str(test_root),'TMPDIR':str(test_root),'PYTHONIOENCODING':'utf-8'}
        def step(label,args,cwd=ROOT,timeout=420):
            print(label,flush=True)
            started=time.monotonic()
            result=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
            log=test_root/(str(len(report)+1)+'.log')
            log.write_text(result.stdout+result.stderr,encoding='utf-8')
            report.append({'step':label,'passed':result.returncode==0,'seconds':round(time.monotonic()-started,2)})
            if result.returncode:
                print(result.stdout+result.stderr,file=sys.stderr)
                (scratch/'latest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
                raise SystemExit(result.returncode)
            print('Passed',flush=True)
            return result.stdout+result.stderr
        step('Build public assets',[sys.executable,'-B','tools/build_assets.py'])
        backend=step('Backend and private-record boundaries',[sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test_*.py'])
        backend_count=re.search(r'Ran (\d+) tests?',backend)
        suites=sorted((ROOT/'tests').glob('test_*.mjs'))
        for suite in suites:
            step(suite.name,[node,str(suite)],timeout=60)
        step('Curriculum content',[node,'tests/test_content.cjs'],timeout=60)
        for asset in sorted((ROOT/'public').glob('*.js')):
            step('Syntax '+asset.name,[node,'--check',str(asset)],timeout=30)
        step('Build browser demo',[node,'browser-demo/build.mjs'],timeout=60)
        step('All demo question samplers',[node,'check-demo.mjs'],cwd=ROOT/'browser-demo',timeout=60)
        step('Demo privacy boundaries',[node,'check-release-security.mjs'],cwd=ROOT/'browser-demo',timeout=60)
        step('Allowlisted hosting archive',[sys.executable,'-B','tools/package_hosting.py',str(test_root/'stepstone-host.zip')],timeout=60)
    (scratch/'latest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':True,'steps':len(report),'backendTests':int(backend_count.group(1)) if backend_count else None,'javascriptSuites':len(suites)+1,'realLearnerRecordsUsed':False}),flush=True)

if __name__=='__main__':
    main()
