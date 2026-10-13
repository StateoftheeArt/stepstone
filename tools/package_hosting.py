"""Create an allowlisted hosting archive, excluding learner data and local setup."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=('preview_checks.py','pip_rewards.py','human_text.py','ai_support.py','backups.py','check_sampling.py','course_access.py','daily_tasks.py','laptop_finder.py','device_work.py','foundation.py',
         'host_runtime.py','mentor_accounts.py','mentor_messages.py','placement.py','projects.py','reward_program.py','gift_cards.py','server.py',
         'text_filter.py','tutorial.py','typing_evidence.py','voice.py','wsgi_app.py')
TOOLS=('build_assets.py','hosted_server.py','pythonanywhere_wsgi.py','backup_records.py','text_filter_terms.py','voice_worker.py')


def source_files(root=ROOT):
    files=[root/name for name in (*RUNTIME,'.python-version','render.yaml','LICENSE','FREE_HOSTING.md','HOSTING.md','OPERATIONS.md')]
    files += [root/'tools'/name for name in TOOLS]
    files += [root/'content/checkpoints.json']
    for path in (root/'public').rglob('*'):
        if path.is_symlink():
            raise ValueError('A public symlink must be reviewed before packaging.')
        if path.is_file():
            if path.name!='LICENSE' and path.suffix.lower() not in ('.html','.js','.css','.json','.svg','.webmanifest','.woff2','.txt','.png','.ico','.md'):
                raise ValueError('Review the unrecognised public file type: '+path.name)
            files.append(path)
    for path in files:
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing or linked deployment input: '+path.name)
    return sorted(files)


def package(output, root=ROOT):
    output=Path(output).resolve()
    if output.exists():
        raise ValueError('Choose a new archive name; existing files are never replaced.')
    files=source_files(root)
    manifest={str(p.relative_to(root)).replace('\\','/'):{'bytes':p.stat().st_size,
              'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:archive.write(path,path.relative_to(root).as_posix())
        archive.writestr('DEPLOYMENT_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
        archive.writestr('.gitignore','data/\nrecovery/\n*.sqlite3\n*.sqlite3-*\n*.partial\n__pycache__/\n*.pyc\n.env\n')
    with zipfile.ZipFile(output) as archive:
        if archive.testzip():raise ValueError('The archive failed its integrity check.')
        for name,details in manifest.items():
            if hashlib.sha256(archive.read(name)).hexdigest()!=details['sha256']:
                raise ValueError('The archive does not match its manifest.')
    return dict(archive=output.name,files=len(manifest),bytes=output.stat().st_size,
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),privateRecordsIncluded=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    print(json.dumps(package(args.output),indent=2))
