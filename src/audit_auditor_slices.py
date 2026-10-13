"""Exploratory four-slice audit, using inputs acquired by prior native audits."""
import ast
import json
import subprocess
from native_consent_controls import ROOT, PIN, decode

def main():
    cedar = str(next((ROOT / '.local-tools/cedar').rglob('cedar.exe')))
    cvc5 = str(next((ROOT / '.local-tools/cvc5').rglob('cvc5.exe')))
    out = ROOT / 'analysis/auditor-slices'
    out.mkdir(exist_ok=True)
    report = []
    for scenario in ['clinical_base', 'clinical_add_consent']:
        cache = ROOT / '.native-cache' / scenario
        tree = ast.parse((cache / 'verification_plan.py').read_text())
        fun = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_checks')
        checks = decode(next(n.value for n in fun.body if isinstance(n, ast.Return)))
        # Union of original floors: a candidate that implements exactly the
        # published must-allow coverage. All original checks are tested below.
        candidate = out / (scenario + '.cedar')
        candidate.write_text('\n'.join((cache / c['floor_path']).read_text() for c in checks if c['type'] == 'floor'), encoding='utf-8')
        records = []
        def run(name, cmd, expected):
            r = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=60)
            records.append({'name': name, 'command': cmd, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
            assert r.returncode == 0, r.stdout + r.stderr
            if expected:
                assert expected in r.stdout, r.stdout + r.stderr
            return r.stdout
        run('validate', [cedar, 'validate', '--schema', str(cache / 'schema.cedarschema'), '--policies', str(candidate)], 'validation passed')
        def command(action):
            return [cedar, 'symcc', '--cvc5-path', cvc5, '--principal-type', 'User', '--action', action,
                    '--resource-type', 'Document', '--schema', str(cache / 'schema.cedarschema'), '--counterexample']
        for c in checks:
            cmd = command(c['action'])
            if c['type'] == 'always-denies-liveness':
                cmd += ['always-denies', '--policies', str(candidate)]
                expected = 'DOES NOT HOLD'
            else:
                ref = cache / c.get('floor_path', c.get('reference_path'))
                a, b = (ref, candidate) if c['type'] == 'floor' else (candidate, ref)
                cmd += ['implies', '--policies1', str(a), '--policies2', str(b)]
                expected = 'VERIFIED'
            run('original_' + c['name'], cmd, expected)
        slices = []
        for role in ['ClinicalResearcher', 'PrincipalInvestigator']:
            for action in ['View', 'Edit']:
                cond = 'principal.clearanceLevel > 3 && resource.classification != "HighlyRestricted"' if role == 'ClinicalResearcher' else 'context.networkRiskScore < 20 && context.isCompliantDevice'
                consent = ' && context.hasPatientConsent' if scenario == 'clinical_add_consent' and action == 'Edit' else ''
                probe = out / f'{scenario}_{role}_{action}.cedar'
                probe.write_text(f'permit(principal is User, action == Action::"{action}", resource is Document) when {{ resource.projectStatus == "Active" && principal in Role::"{role}" && principal in Role::"GlobalAuditor" && principal.department != resource.projectManagingDepartment && {cond}{consent} }};\n', encoding='utf-8')
                run('validate_' + probe.stem, [cedar, 'validate', '--schema', str(cache / 'schema.cedarschema'), '--policies', str(probe)], 'validation passed')
                result = run(probe.stem, command(f'Action::"{action}"') + ['implies', '--policies1', str(probe), '--policies2', str(candidate)], None)
                assert 'VERIFIED' in result or 'DOES NOT HOLD' in result
                slices.append({'role': role, 'action': action, 'covered': 'VERIFIED' in result})
        report.append({'scenario': scenario, 'original_checks_passed': len(checks), 'slices': slices, 'records': records})
        print(scenario, len(checks), 'original checks passed;', sum(s['covered'] for s in slices), '/4 slices covered')
    (out / 'receipt.json').write_text(json.dumps({'upstream_commit': PIN, 'scope': 'Exploratory logical coverage audit, not model performance or prevalence', 'results': report}, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
