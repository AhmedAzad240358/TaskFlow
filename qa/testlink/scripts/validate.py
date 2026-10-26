"""Check data quality and bidirectional coverage before importing anything."""
import importlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

TECHNIQUES = ('EP', 'BVA', 'Decision Table', 'State Transition', 'Use Case', 'Error Guessing')

def validate_module(data):
    letter = data.LETTER
    assert re.fullmatch(r'[a-z][a-z0-9_]{0,29}', data.AUTHOR), 'Unsafe AUTHOR login'
    reqs, specs, ids, used, names = set(), set(), set(), set(), set()
    for spec in data.REQ_SPECS:
        assert spec['doc_id'].startswith(f'SRS-{letter}-')
        assert spec['doc_id'] not in specs
        specs.add(spec['doc_id'])
        assert spec['scope'] and spec['title']
        for rid, title, desc in spec['reqs']:
            assert rid.startswith(f'REQ-{letter}-') and rid not in reqs, rid
            assert title and 'README.md' in desc and 'src/' in desc, f'Missing source: {rid}'
            reqs.add(rid)
    for n, suite in enumerate(data.SUITES, 1):
        assert suite['name'].startswith(f'TS-{letter}{n}'), suite['name']
        assert suite['details'] and suite['cases']
        for case in suite['cases']:
            cid = case['id']
            assert re.fullmatch(f'TC-{letter}-[0-9]{{3}}', cid) and cid not in ids, cid
            assert case['name'].startswith(cid) and case['name'] not in names
            assert any(t in case['technique'] for t in TECHNIQUES), cid
            assert case['pre'].strip() and case['steps'] and case['reqs'], cid
            assert case['importance'] in (1, 2, 3)
            for action, expected in case['steps']:
                assert action.strip() and expected.strip(), cid
            assert not set(case['reqs']) - reqs, f'{cid}: unknown requirements'
            ids.add(cid); names.add(case['name']); used.update(case['reqs'])
    assert reqs == used, f'Uncovered requirements: {sorted(reqs-used)}'
    return {'author': data.AUTHOR, 'letter': letter, 'specifications':len(specs),
            'requirements':len(reqs), 'suites':len(data.SUITES), 'test_cases':len(ids),
            'covered_requirements':len(used), 'coverage_percent':100}

if __name__ == '__main__':
    args = sys.argv[1:]
    paths = sorted(Path(__file__).parent.glob('*_testdata.py')) if args == ['all'] else [Path(f'{n}_testdata.py') for n in args]
    results = [validate_module(importlib.import_module(p.stem)) for p in paths]
    assert len({r['letter'] for r in results}) == len(results), 'Duplicate member letters'
    assert len({r['author'] for r in results}) == len(results), 'Duplicate authors'
    print(json.dumps(results, indent=2))
