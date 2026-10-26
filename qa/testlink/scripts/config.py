"""Shared local-only TestLink configuration. No lecturer-server project is created."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

KIT = Path(__file__).resolve().parents[1]
ROOT = KIT.parents[1]
BASE = os.environ.get('TESTLINK_URL', f"http://localhost:{os.environ.get('TESTLINK_PORT', '8090')}")
if urlsplit(BASE).hostname not in ('localhost', '127.0.0.1', '::1'):
    raise ValueError('This kit creates projects only in local TestLink. Import XML into the lecturer\'s existing project.')
PROJECT = 'TaskFlow'
PREFIX = 'TF'
PLAN = 'Project 1 - Test Case Design'
SOURCE_COMMIT = '5133a6c'
BUILD = f'TaskFlow main@{SOURCE_COMMIT}'
REPO = 'https://github.com/aland99/TaskFlow'
GROUP = 'TaskFlow'

def roster():
    return json.loads((ROOT / 'qa/project1/team.json').read_text())

def refresh_header():
    """Resolve slot labels from independently authored member data modules."""
    import importlib
    members = {m['letter']: m['name'] for m in roster()}
    for file in sorted((KIT / 'scripts').glob('*_testdata.py')):
        data = importlib.import_module(file.stem)
        members[data.LETTER] = data.FULL_NAME
    names = ', '.join(members[k] for k in sorted(members))
    title = f'UTM SECJ3343 Software Quality Assurance - Group {GROUP} ({names})'.replace("'", "\\'")
    content = "<?php\n$tlCfg->document_generator->company_name = '" + title + "';\n"
    content += f"$tlCfg->document_generator->company_copyright = '2026 Group {GROUP} - Project 1 Test Case Design';\n"
    (KIT / 'overlay/custom_config.inc.php').write_text(content)
    if (KIT / 'app').exists():
        (KIT / 'app/custom_config.inc.php').write_text(content)
