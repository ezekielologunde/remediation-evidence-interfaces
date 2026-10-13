"""Audit available upstream outputs using unchanged, previously frozen probes."""
import ast
import hashlib
import json
import subprocess
import urllib.request
from native_consent_controls import ROOT, PIN, decode

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    protocol = ROOT/'protocol/released-clinical-protocol.json'
    config = json.loads(protocol.read_text())
    scenarios = json.loads((ROOT/'protocol/clinical-inventory-protocol.json').read_text())['scenarios']
    cedar = str(next((ROOT/'.local-tools/cedar').rglob('cedar.exe')))
    cvc5 = str(next((ROOT/'.local-tools/cvc5').rglob('cvc5.exe')))
    out = ROOT/'analysis/released-clinical'
    out.mkdir(exist_ok=True)
    report = {'protocol_sha256': digest(protocol), 'commit': PIN, 'run': config['run'], 'scenarios': []}
    def fetch(remote, dest):
        url = f'https://raw.githubusercontent.com/neselab/cedar-synthesis-engine/{PIN}/{config["run"]}/{remote}'
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            dest.write_bytes(urllib.request.urlopen(url, timeout=45).read())
        return {'url': url, 'sha256': digest(dest)}
    report['summary'] = fetch('SUMMARY.md', out/'UPSTREAM-SUMMARY.md')
    for scenario in scenarios:
        baseline = ROOT/'.native-cache'/scenario
        dest = out/scenario
        cache = ROOT/'.native-cache/released-clinical'/scenario
        checks_ast = ast.parse((baseline/'verification_plan.py').read_text())
        fun = next(n for n in checks_ast.body if isinstance(n, ast.FunctionDef) and n.name == 'get_checks')
        checks = decode(next(n.value for n in fun.body if isinstance(n, ast.Return)))
        names = ['schema.cedarschema', 'policy_spec.md', 'verification_plan.py']
        names += sorted({c.get('floor_path', c.get('reference_path')) for c in checks if c['type'] != 'always-denies-liveness'})
        alignment = []
        for name in names:
            manifest = fetch(f'workspaces/{scenario}/{name}', cache/name)
            alignment.append({'name': name, **manifest, 'baseline_sha256': digest(baseline/name), 'identical': digest(cache/name) == digest(baseline/name)})
        policy = dest/'candidate.cedar'
        candidate_manifest = fetch(f'workspaces/{scenario}/candidate.cedar', policy)
        entry = {'scenario': scenario, 'alignment': alignment, 'candidate': candidate_manifest, 'records': [], 'slices': []}
        report['scenarios'].append(entry)
        def run(name, cmd, expected=None):
            try:
                r = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=45)
                verdict = 'verified' if 'VERIFIED' in r.stdout else 'counterexample' if 'DOES NOT HOLD' in r.stdout else 'unknown'
                rec = {'name': name, 'command': cmd, 'code': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr, 'verdict': verdict,
                       'passed': r.returncode == 0 and (expected in r.stdout+r.stderr if expected else verdict != 'unknown')}
            except subprocess.TimeoutExpired:
                rec = {'name': name, 'command': cmd, 'verdict': 'timeout', 'passed': False}
            entry['records'].append(rec)
            return rec
        schema = baseline/'schema.cedarschema'
        def sym(action):
            return [cedar, 'symcc', '--cvc5-path', cvc5, '--principal-type', 'User', '--action', action, '--resource-type', 'Document', '--schema', str(schema), '--counterexample']
        aligned = all(a['identical'] for a in alignment)
        entry['aligned'] = aligned
        if aligned:
            valid = run('validate', [cedar, 'validate', '--schema', str(schema), '--policies', str(policy)], 'validation passed')['passed']
            passed = 0
            for c in checks:
                cmd = sym(c['action'])
                if c['type'] == 'always-denies-liveness':
                    cmd += ['always-denies', '--policies', str(policy)]
                    expected = 'DOES NOT HOLD'
                else:
                    ref = baseline/c.get('floor_path', c.get('reference_path'))
                    a, b = (ref, policy) if c['type'] == 'floor' else (policy, ref)
                    cmd += ['implies', '--policies1', str(a), '--policies2', str(b)]
                    expected = 'VERIFIED'
                passed += run('original_'+c['name'], cmd, expected)['passed']
            entry.update(accepted=valid and passed == len(checks), passed=passed, original_checks=len(checks))
            for role in ['ClinicalResearcher', 'PrincipalInvestigator']:
                for action in ['View', 'Edit']:
                    probe = ROOT/'analysis/clinical-family'/scenario/f'{role}_{action}.cedar'
                    r = run('probe_'+probe.stem, sym(f'Action::"{action}"') + ['implies', '--policies1', str(probe), '--policies2', str(policy)])
                    status = 'tool_error' if not r['passed'] else 'candidate_rejected' if not entry['accepted'] else 'intentional_denial_control' if scenario == 'clinical_remove_auditor' else 'covered' if r['verdict'] == 'verified' else 'accepted_candidate_omission'
                    entry['slices'].append({'role': role, 'action': action, 'probe_sha256': digest(probe), 'status': status, 'verdict': r['verdict']})
        (out/'receipt.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(scenario, 'aligned', aligned, entry.get('passed'), [s['status'] for s in entry['slices']], flush=True)

if __name__ == '__main__':
    main()
