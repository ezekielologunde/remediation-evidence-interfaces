"""Fixed two-slice transfer check, not a complete doccloud family audit."""
import ast
import hashlib
import json
import subprocess
import urllib.request
from native_consent_controls import ROOT, PIN, decode

def main():
    scenario = 'doccloud_base'
    out = ROOT/'analysis/doccloud-transfer'
    cache = ROOT/'.native-cache'/scenario
    out.mkdir(exist_ok=True)
    report = {'scenario': scenario, 'commit': PIN, 'manifest': [], 'records': [], 'candidates': {}, 'probes': []}
    report['protocol_sha256'] = hashlib.sha256((ROOT/'protocol/doccloud-transfer-protocol.json').read_bytes()).hexdigest()
    prefix = f'https://raw.githubusercontent.com/neselab/cedar-synthesis-engine/{PIN}/'
    def fetch(remote, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(prefix+remote, timeout=45).read())
        report['manifest'].append({'url': prefix+remote, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        return path
    def source(name):
        return fetch(f'cedarbench/scenarios/{scenario}/{name}', cache/name)
    schema = source('schema.cedarschema')
    source('policy_spec.md')
    tree = ast.parse(source('verification_plan.py').read_text())
    fun = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_checks')
    checks = decode(next(n.value for n in fun.body if isinstance(n, ast.Return)))
    for c in checks:
        if c['type'] != 'always-denies-liveness':
            source(c.get('floor_path', c.get('reference_path')))
    baseline = fetch('experiments/cedarbench_aitl_fast/cedarbench-aitl-fast-gpt55-low-20260630/workspaces/doccloud_base/candidate.cedar', out/'released.cedar')
    narrowed = out/'narrowed.cedar'
    narrowed.write_text(baseline.read_text()+'\nforbid(principal is User, action in [Action::"ViewDocument", Action::"ModifyDocument"], resource is Document) when { principal != resource.owner };\n', encoding='utf-8')
    cedar = str(next((ROOT/'.local-tools/cedar').rglob('cedar.exe')))
    cvc5 = str(next((ROOT/'.local-tools/cvc5').rglob('cvc5.exe')))
    def run(name, cmd, expected):
        try:
            r = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=45)
            result = {'name': name, 'command': cmd, 'code': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr, 'passed': r.returncode == 0 and expected in r.stdout+r.stderr}
        except subprocess.TimeoutExpired:
            result = {'name': name, 'command': cmd, 'passed': False, 'error': 'timeout'}
        report['records'].append(result)
        return result['passed']
    def sym(c):
        return [cedar, 'symcc', '--cvc5-path', cvc5, '--principal-type', c['principal_type'], '--action', c['action'], '--resource-type', c['resource_type'], '--schema', str(schema), '--counterexample']
    for label, policy in [('released', baseline), ('narrowed', narrowed)]:
        valid = run(label+'_validate', [cedar, 'validate', '--schema', str(schema), '--policies', str(policy)], 'validation passed')
        passed = 0
        for c in checks:
            cmd = sym(c)
            if c['type'] == 'always-denies-liveness':
                cmd += ['always-denies', '--policies', str(policy)]
                expected = 'DOES NOT HOLD'
            else:
                ref = cache/c.get('floor_path', c.get('reference_path'))
                a,b = (ref,policy) if c['type'] == 'floor' else (policy,ref)
                cmd += ['implies', '--policies1', str(a), '--policies2', str(b)]
                expected = 'VERIFIED'
            passed += run(label+'_'+c['name'], cmd, expected)
        report['candidates'][label] = {'valid': valid, 'passed': passed, 'total': len(checks), 'accepted': valid and passed == len(checks)}
    for action, acl in [('ViewDocument','viewACL'), ('ModifyDocument','modifyACL')]:
        probe = out/(action+'.cedar')
        probe.write_text(f'permit(principal is User, action == Action::"{action}", resource is Document) when {{ context.is_authenticated && principal != resource.owner && !resource.isPrivate && principal in resource.{acl} && !principal.blocked.contains(resource.owner) && !resource.owner.blocked.contains(principal) }};\n', encoding='utf-8')
        cmd = sym({'principal_type':'User', 'action':f'Action::"{action}"', 'resource_type':'Document'})
        valid = run(action+'_validate', [cedar, 'validate', '--schema', str(schema), '--policies', str(probe)], 'validation passed')
        live = run(action+'_live', cmd+['always-denies', '--policies', str(probe)], 'DOES NOT HOLD')
        covered = run(action+'_released', cmd+['implies','--policies1',str(probe),'--policies2',str(baseline)], 'VERIFIED')
        omitted = run(action+'_narrowed', cmd+['implies','--policies1',str(probe),'--policies2',str(narrowed)], 'DOES NOT HOLD')
        report['probes'].append({'action':action,'valid':valid,'live':live,'released_covered':covered,'narrowed_counterexample':omitted})
    (out/'receipt.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'candidates':report['candidates'],'probes':report['probes']}, indent=2))

if __name__ == '__main__':
    main()
