"""Reproduce the auditor omission using native Cedar SymCC and authorization.

Downloads pinned inputs as data, never executes upstream Python. Requires Cedar
experimental CLI and CVC5 paths. Raw outputs and input hashes are retained.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

COMMIT = '0201565abf5993e258764d3f0ef83a59d3b4962e'
BASE = f'https://raw.githubusercontent.com/neselab/cedar-synthesis-engine/{COMMIT}/cedarbench/scenarios/clinical_add_consent/'
REFS = ['ceiling_view', 'ceiling_edit', 'ceiling_view_dept',
        'ceiling_edit_dept', 'ceiling_edit_consent', 'floor_cr_view',
        'floor_pi_view', 'floor_pi_edit', 'floor_cr_edit']

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cedar', required=True)
    p.add_argument('--cvc5', required=True)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    cache = root / '.native-cache' / 'clinical_add_consent'
    cache.mkdir(parents=True, exist_ok=True)
    output = root / 'analysis' / 'native-consent'
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name in ['schema.cedarschema', 'policy_spec.md', 'verification_plan.py'] + ['references/' + r + '.cedar' for r in REFS]:
        dest = cache / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            dest.write_bytes(urllib.request.urlopen(BASE + name, timeout=30).read())
        manifest.append({'path': name, 'url': BASE + name,
                         'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
    condition = '''resource.projectStatus == "Active" &&
    ((principal in Role::"ClinicalResearcher" && principal.clearanceLevel > 3 && resource.classification != "HighlyRestricted") ||
     (principal in Role::"PrincipalInvestigator" && context.networkRiskScore < 20 && context.isCompliantDevice)) &&
    DEPARTMENT && (action == Action::"View" || context.hasPatientConsent)'''
    template = 'permit(principal is User, action in [Action::"View", Action::"Edit"], resource is Document) when {\nCONDITION\n};\n'
    policies = {
        'candidate': 'principal.department == resource.projectManagingDepartment',
        'intended': '(principal.department == resource.projectManagingDepartment || principal in Role::"GlobalAuditor")',
        'auditor_floor': 'principal in Role::"GlobalAuditor"',
    }
    for name, dept in policies.items():
        (output / (name + '.cedar')).write_text(template.replace('CONDITION', condition.replace('DEPARTMENT', dept)), encoding='utf-8')
    records = []
    def run(name, cmd):
        r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=60)
        records.append({'name': name, 'command': cmd, 'returncode': r.returncode,
                        'stdout': r.stdout, 'stderr': r.stderr})
        print(name, r.returncode, r.stdout[:180].replace('\n', ' ').encode('ascii', 'replace').decode(), flush=True)
        return r
    run('cedar_version', [args.cedar, '--version'])
    run('cvc5_version', [args.cvc5, '--version'])
    schema = str(cache / 'schema.cedarschema')
    for name in policies:
        run('validate_' + name, [args.cedar, 'validate', '--schema', schema, '--policies', str(output / (name + '.cedar'))])
    candidate = str(output / 'candidate.cedar')
    for name in REFS + ['liveness_view', 'liveness_edit', 'added_auditor_view', 'added_auditor_edit']:
        action = 'View' if 'view' in name else 'Edit'
        cmd = [args.cedar, 'symcc', '--cvc5-path', args.cvc5,
               '--principal-type', 'User', '--action', f'Action::"{action}"',
               '--resource-type', 'Document', '--schema', schema, '--counterexample']
        if name.startswith('liveness'):
            cmd += ['always-denies', '--policies', candidate]
        else:
            ref = str(output / 'auditor_floor.cedar') if name.startswith('added') else str(cache / 'references' / (name + '.cedar'))
            first, second = (ref, candidate) if name.startswith(('floor', 'added')) else (candidate, ref)
            cmd += ['implies', '--policies1', first, '--policies2', second]
        run(name, cmd)
        if name.startswith('added'):
            repaired = cmd.copy()
            repaired[repaired.index('--policies2') + 1] = str(output / 'intended.cedar')
            run('repaired_' + name, repaired)
    def uid(t, i):
        return {'type': t, 'id': i}
    entities = [
        {'uid': uid('Role', role), 'attrs': {}, 'parents': []}
        for role in ['PrincipalInvestigator', 'GlobalAuditor']]
    entities += [
        {'uid': uid('User', 'auditor'), 'attrs': {'department': 'A', 'clearanceLevel': 0},
         'parents': [uid('Role', 'PrincipalInvestigator'), uid('Role', 'GlobalAuditor')]},
        {'uid': uid('Document', 'record'), 'attrs': {'classification': 'HighlyRestricted', 'projectStatus': 'Active', 'projectManagingDepartment': 'B'}, 'parents': []}]
    (output / 'entities.json').write_text(json.dumps(entities, indent=2), encoding='utf-8')
    request = {'principal': 'User::"auditor"', 'action': 'Action::"View"',
               'resource': 'Document::"record"', 'context': {'networkRiskScore': 0, 'isCompliantDevice': True, 'hasPatientConsent': False}}
    (output / 'request.json').write_text(json.dumps(request, indent=2), encoding='utf-8')
    for name in ['candidate', 'intended']:
        run('witness_' + name, [args.cedar, 'authorize', '--schema', schema,
            '--policies', str(output / (name + '.cedar')), '--entities', str(output / 'entities.json'), '--request-json', str(output / 'request.json')])
    report = {'upstream_commit': COMMIT, 'input_manifest': manifest, 'records': records,
              'scope': 'Independent native CLI checks mapped from pinned plan; not an execution of AutoCedar synthesis or its Python harness.'}
    (output / 'receipt.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    indexed = {r['name']: r for r in records}
    assert all(indexed['validate_' + name]['returncode'] == 0 for name in policies)
    assert all('VERIFIED' in indexed[name]['stdout'] and indexed[name]['returncode'] == 0 for name in REFS)
    assert all('DOES NOT HOLD' in indexed[name]['stdout'] and indexed[name]['returncode'] == 0 for name in ['liveness_view', 'liveness_edit', 'added_auditor_view', 'added_auditor_edit'])
    assert 'DENY' in indexed['witness_candidate']['stdout'].upper()
    assert 'ALLOW' in indexed['witness_intended']['stdout'].upper()
    assert indexed['witness_candidate']['returncode'] == 2
    assert indexed['witness_intended']['returncode'] == 0
    assert all('VERIFIED' in indexed['repaired_added_auditor_' + action]['stdout'] for action in ['view', 'edit'])

if __name__ == '__main__':
    main()
