"""Check follow-up manuscript values against raw native verdicts and hashes."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
source = Path(sys.argv[2]) if len(sys.argv) > 2 else root/'paper/main.tex'
text = source.read_text(encoding='utf-8')
clinical = json.loads((root/'analysis/released-clinical/receipt.json').read_text())
assert len(clinical['scenarios']) == 11
covered = controls = checks = 0
for s in clinical['scenarios']:
    assert all(x['sha256'] == x['baseline_sha256'] for x in s['alignment'])
    assert hashlib.sha256((root/'analysis/released-clinical'/s['scenario']/'candidate.cedar').read_bytes()).hexdigest() == s['candidate']['sha256']
    for r in s['records']:
        assert r['code'] == 0
        if r['name'] == 'validate':
            assert 'validation passed' in r['stdout']
        elif r['name'].startswith('original_'):
            assert ('DOES NOT HOLD' if 'always-denies' in r['command'] else 'VERIFIED') in r['stdout']
            checks += 1
        elif r['name'].startswith('probe_'):
            negative = s['scenario'] == 'clinical_remove_auditor'
            assert ('DOES NOT HOLD' if negative else 'VERIFIED') in r['stdout']
            controls += negative
            covered += not negative
    for q in s['slices']:
        probe = root/'analysis/clinical-family'/s['scenario']/(q['role']+'_'+q['action']+'.cedar')
        assert hashlib.sha256(probe.read_bytes()).hexdigest() == q['probe_sha256']
assert (checks, covered, controls) == (149,40,4)
doc = json.loads((root/'analysis/doccloud-transfer/receipt.json').read_text())
totals = {'released':0,'narrowed':0}
for r in doc['records']:
    assert r['code'] == 0
    if r['name'].endswith('_validate'):
        expected = 'validation passed'
    elif r['name'].startswith(('released_','narrowed_')):
        totals[r['name'].split('_')[0]] += 1
        expected = 'DOES NOT HOLD' if 'always-denies' in r['command'] else 'VERIFIED'
    else:
        expected = 'DOES NOT HOLD' if r['name'].endswith(('_live','_narrowed')) else 'VERIFIED'
    assert expected in r['stdout']
assert totals == {'released':43,'narrowed':43}
for row in ['Clinical released (11) & 149/149 & 40 & 0', 'Doccloud released (1) & 43/43 & 2 & 0', 'Doccloud narrowed (1) & 43/43 & 0 & 2']:
    assert row in text
print(json.dumps({'status':'passed','clinical_original_checks':checks,'clinical_positive_covered':covered,'clinical_negative_controls':controls,'doccloud_checks':totals,'doccloud_positive_probes':2,'scope':'Raw recorded native verdicts, probe hashes and manuscript table; not independent interpretation'},indent=2))
