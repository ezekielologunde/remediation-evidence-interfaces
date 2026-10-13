"""Independent raw-verdict and manuscript-value checks; no solver claims added."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--receipt', type=Path, required=True)
a = p.parse_args()
d = json.loads(a.receipt.read_text())
text = a.source.read_text(encoding='utf-8')
counts = {'original_checks': 0, 'positive_covered': 0, 'positive_omitted': 0,
          'negative_control_probes': 0, 'equivalent_rewrites': 0, 'probe_validations': 0, 'probe_liveness': 0}
for s in d['scenarios']:
    raw = {r['name']: r for r in s['records']}
    orig = [r for r in s['records'] if r['name'].startswith('original_') and r['name'] != 'original_validate']
    assert len(orig) == s['original_checks']
    for r in orig:
        expected = 'DOES NOT HOLD' if 'always-denies' in r['command'] else 'VERIFIED'
        assert r['code'] == 0 and expected in r['stdout']
    counts['original_checks'] += len(orig)
    covered = omitted = 0
    for q in s['slices']:
        key = q['role'] + '_' + q['action']
        v, live, implication = [raw[prefix + key] for prefix in ['probe_validate_', 'probe_live_', 'probe_']]
        assert v['code'] == 0 and 'validation passed' in v['stdout']
        assert live['code'] == 0 and 'DOES NOT HOLD' in live['stdout']
        counts['probe_validations'] += 1
        counts['probe_liveness'] += 1
        assert implication['code'] == 0
        if s['scenario'] == 'clinical_remove_auditor':
            assert 'DOES NOT HOLD' in implication['stdout']
            counts['negative_control_probes'] += 1
        elif 'VERIFIED' in implication['stdout']:
            covered += 1
        else:
            assert 'DOES NOT HOLD' in implication['stdout']
            omitted += 1
    counts['positive_covered'] += covered
    counts['positive_omitted'] += omitted
    label = s['scenario'].removeprefix('clinical_').replace('_', r'\_')
    expected = f"{label} & {len(orig)}/{len(orig)} & "
    expected += '-- & -- & Reject' if s['scenario'] == 'clinical_remove_auditor' else f'{covered} & {omitted} & Pass'
    assert expected in text, expected
    augmented = [r for r in s['records'] if r['name'].startswith('augmented_') and r['name'] != 'augmented_validate']
    failed = [r for r in augmented if ('DOES NOT HOLD' if 'always-denies' in r['command'] else 'VERIFIED') not in r['stdout']]
    assert len(failed) == (4 if s['scenario'] == 'clinical_remove_auditor' else 0)
    for action in ['View','Edit']:
        assert 'VERIFIED' in raw['rewrite_' + action]['stdout']
        counts['equivalent_rewrites'] += 1
assert counts['original_checks'] == 149
assert counts['positive_covered'] == 6 and counts['positive_omitted'] == 34
assert '(Covered,6) (Omitted,34)' in text
assert 'TABLE_PLACEHOLDER' not in text and 'FIGURE_PLACEHOLDER' not in text
print(json.dumps({'status': 'passed', 'counts': counts, 'scope': 'Independent parsing of existing native receipts and generated manuscript values; not independent requirement adjudication', 'source_sha256': hashlib.sha256(a.source.read_bytes()).hexdigest()}, indent=2))
