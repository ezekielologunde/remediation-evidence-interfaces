"""Exploratory lineage controls. Parses plans as data; never executes them."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PIN = '0201565abf5993e258764d3f0ef83a59d3b4962e'

def decode(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [decode(n) for n in node.elts]
    if isinstance(node, ast.Dict):
        return {decode(k): decode(v) for k, v in zip(node.keys, node.values)}
    if (isinstance(node, ast.Call) and ast.unparse(node.func) == 'os.path.join'
            and len(node.args) == 2 and isinstance(node.args[0], ast.Name)
            and node.args[0].id == 'REFS' and not node.keywords):
        return 'references/' + decode(node.args[1])
    raise ValueError('Unsupported plan expression: ' + ast.dump(node))

def main():
    cedar = str(next((ROOT / '.local-tools/cedar').rglob('cedar.exe')))
    cvc5 = str(next((ROOT / '.local-tools/cvc5').rglob('cvc5.exe')))
    out = ROOT / 'analysis/native-controls'
    out.mkdir(exist_ok=True)
    receipts = []
    for scenario in ['clinical_base', 'clinical_remove_auditor']:
        cache = ROOT / '.native-cache' / scenario
        manifest = []
        def fetch(name):
            path = cache / name
            path.parent.mkdir(parents=True, exist_ok=True)
            url = f'https://raw.githubusercontent.com/neselab/cedar-synthesis-engine/{PIN}/cedarbench/scenarios/{scenario}/{name}'
            if not path.exists():
                path.write_bytes(urllib.request.urlopen(url, timeout=30).read())
            manifest.append({'url': url, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            return path
        schema = fetch('schema.cedarschema')
        fetch('policy_spec.md')
        tree = ast.parse(fetch('verification_plan.py').read_text())
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_checks')
        checks = decode(next(n.value for n in function.body if isinstance(n, ast.Return)))
        candidate = out / (scenario + '.cedar')
        original = (ROOT / 'analysis/native-consent/candidate.cedar').read_text()
        consent = ' && (action == Action::"View" || context.hasPatientConsent)'
        assert original.count(consent) == 1
        candidate.write_text(original.replace(consent, ''), encoding='utf-8')
        validation = subprocess.run([cedar, 'validate', '--schema', str(schema), '--policies', str(candidate)], capture_output=True, encoding='utf-8')
        assert validation.returncode == 0, validation.stdout + validation.stderr
        results = []
        for check in checks:
            cmd = [cedar, 'symcc', '--cvc5-path', cvc5, '--principal-type', check['principal_type'],
                   '--action', check['action'], '--resource-type', check['resource_type'], '--schema', str(schema), '--counterexample']
            if check['type'] == 'always-denies-liveness':
                cmd += ['always-denies', '--policies', str(candidate)]
                expected = 'DOES NOT HOLD'
            else:
                ref = fetch(check.get('floor_path', check.get('reference_path')))
                first, second = (ref, candidate) if check['type'] == 'floor' else (candidate, ref)
                cmd += ['implies', '--policies1', str(first), '--policies2', str(second)]
                expected = 'VERIFIED'
            r = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=60)
            assert r.returncode == 0 and ('VERIFIED' in r.stdout or 'DOES NOT HOLD' in r.stdout), r.stdout + r.stderr
            results.append({'name': check['name'], 'passed': expected in r.stdout, 'command': cmd,
                            'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
        receipts.append({'scenario': scenario, 'manifest': manifest, 'validation': validation.stdout, 'checks': results})
        print(scenario, sum(r['passed'] for r in results), '/', len(results), 'failed:', [r['name'] for r in results if not r['passed']])
    (out / 'receipt.json').write_text(json.dumps({'commit': PIN, 'scope': 'Exploratory related-scenario controls, not independent prevalence samples', 'results': receipts}, indent=2), encoding='utf-8')
    assert [r['name'] for r in receipts[0]['checks'] if not r['passed']] == ['floor_auditor_cross_dept_view']
    assert all(r['passed'] for r in receipts[1]['checks'])

if __name__ == '__main__':
    main()
