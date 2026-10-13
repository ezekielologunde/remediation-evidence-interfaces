"""Native audit of the frozen clinical inventory. No model calls."""
import ast
import hashlib
import json
import subprocess
import urllib.request
from native_consent_controls import ROOT, PIN, decode

def main():
    protocol = ROOT / 'protocol/clinical-inventory-protocol.json'
    config = json.loads(protocol.read_text())
    cedar = str(next((ROOT / '.local-tools/cedar').rglob('cedar.exe')))
    cvc5 = str(next((ROOT / '.local-tools/cvc5').rglob('cvc5.exe')))
    out = ROOT / 'analysis/clinical-family'
    out.mkdir(exist_ok=True)
    report = {'commit': PIN, 'protocol_sha256': hashlib.sha256(protocol.read_bytes()).hexdigest(), 'scenarios': []}
    for scenario in config['scenarios']:
        cache = ROOT / '.native-cache' / scenario
        dest = out / scenario
        dest.mkdir(exist_ok=True)
        manifest, records = [], []
        def fetch(name):
            path = cache / name
            path.parent.mkdir(parents=True, exist_ok=True)
            url = f'https://raw.githubusercontent.com/neselab/cedar-synthesis-engine/{PIN}/cedarbench/scenarios/{scenario}/{name}'
            if not path.exists():
                path.write_bytes(urllib.request.urlopen(url, timeout=30).read())
            manifest.append({'name': name, 'url': url, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            return path
        schema = fetch('schema.cedarschema')
        fetch('policy_spec.md')
        tree = ast.parse(fetch('verification_plan.py').read_text())
        fun = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_checks')
        checks = decode(next(n.value for n in fun.body if isinstance(n, ast.Return)))
        for c in checks:
            if c['type'] != 'always-denies-liveness':
                fetch(c.get('floor_path', c.get('reference_path')))
        candidate = dest / 'candidate.cedar'
        floors = [(cache / c['floor_path']).read_text() for c in checks if c['type'] == 'floor']
        candidate.write_text('\n'.join(floors), encoding='utf-8')
        def run(name, cmd, expected=None):
            try:
                r = subprocess.run(cmd, capture_output=True, encoding='utf-8', timeout=45)
                raw = r.stdout + r.stderr
                verdict = 'verified' if 'VERIFIED' in r.stdout else 'counterexample' if 'DOES NOT HOLD' in r.stdout else 'unknown'
                rec = {'name': name, 'command': cmd, 'code': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr, 'verdict': verdict}
                rec['passed'] = r.returncode == 0 and (expected in raw if expected else verdict != 'unknown')
            except subprocess.TimeoutExpired:
                rec = {'name': name, 'command': cmd, 'verdict': 'timeout', 'passed': False}
            records.append(rec)
            return rec
        def sym(action):
            return [cedar, 'symcc', '--cvc5-path', cvc5, '--principal-type', 'User', '--action', action, '--resource-type', 'Document', '--schema', str(schema), '--counterexample']
        def evaluate(policy, prefix):
            valid = run(prefix + '_validate', [cedar, 'validate', '--schema', str(schema), '--policies', str(policy)], 'validation passed')['passed']
            results = []
            for c in checks:
                cmd = sym(c['action'])
                if c['type'] == 'always-denies-liveness':
                    cmd += ['always-denies', '--policies', str(policy)]
                    expected = 'DOES NOT HOLD'
                else:
                    ref = cache / c.get('floor_path', c.get('reference_path'))
                    a, b = (ref, policy) if c['type'] == 'floor' else (policy, ref)
                    cmd += ['implies', '--policies1', str(a), '--policies2', str(b)]
                    expected = 'VERIFIED'
                results.append(run(prefix + '_' + c['name'], cmd, expected)['passed'])
            return valid and all(results), sum(results)
        accepted, passed = evaluate(candidate, 'original')
        probes, slices = [], []
        for role in config['roles']:
            for action in config['actions']:
                cr = role == 'ClinicalResearcher'
                other = 'PrincipalInvestigator' if cr else 'ClinicalResearcher'
                conditions = ['resource.projectStatus == "Active"', f'principal in Role::"{role}"', 'principal in Role::"GlobalAuditor"',
                              f'!(principal in Role::"{other}")', '!(principal in Role::"DataManager")', '!(principal in Role::"SponsorRepresentative")',
                              'principal.department != resource.projectManagingDepartment']
                conditions += [f'principal.clearanceLevel {">=" if scenario == "clinical_relax_clearance" else ">"} 3', 'resource.classification != "HighlyRestricted"'] if cr else ['context.networkRiskScore < 20', 'context.isCompliantDevice']
                if action == 'Edit' and scenario in ['clinical_add_consent', 'clinical_full_expansion']:
                    conditions += ['context.hasPatientConsent']
                if cr and scenario in ['clinical_add_study_phase', 'clinical_full_expansion']:
                    conditions += ['resource.studyPhase != "Phase-3"']
                if cr and scenario == 'clinical_temporal_embargo':
                    conditions += ['context.requestTime >= resource.embargoUntil']
                probe = dest / f'{role}_{action}.cedar'
                probe.write_text(f'permit(principal is User, action == Action::"{action}", resource is Document) when {{\n' + ' &&\n'.join(conditions) + '\n};\n', encoding='utf-8')
                probes.append(probe.read_text())
                valid = run('probe_validate_' + probe.stem, [cedar, 'validate', '--schema', str(schema), '--policies', str(probe)], 'validation passed')['passed']
                live = run('probe_live_' + probe.stem, sym(f'Action::"{action}"') + ['always-denies', '--policies', str(probe)], 'DOES NOT HOLD')['passed']
                r = run('probe_' + probe.stem, sym(f'Action::"{action}"') + ['implies', '--policies1', str(probe), '--policies2', str(candidate)])
                status = 'intentional_denial_control' if scenario == 'clinical_remove_auditor' else 'tool_error' if not(valid and live and r['passed']) else 'candidate_rejected' if not accepted else 'covered' if r['verdict'] == 'verified' else 'accepted_candidate_omission'
                slices.append({'role': role, 'action': action, 'status': status, 'verdict': r['verdict'], 'probe_valid_live': valid and live})
        repaired = dest / 'augmented.cedar'
        repaired.write_text('\n'.join(floors + probes), encoding='utf-8')
        repaired_ok, repaired_count = evaluate(repaired, 'augmented')
        rewrite = dest / 'reordered.cedar'
        rewrite.write_text('\n'.join(reversed(floors)), encoding='utf-8')
        equivalence = []
        for action in config['actions']:
            equivalence.append(run('rewrite_' + action, sym(f'Action::"{action}"') + ['equivalent', '--policies1', str(candidate), '--policies2', str(rewrite)], 'VERIFIED')['passed'])
        entry = {'scenario': scenario, 'original_checks': len(checks), 'passed': passed, 'accepted': accepted, 'slices': slices,
                 'augmented_accepted': repaired_ok, 'augmented_passed': repaired_count, 'rewrite_equivalent': all(equivalence), 'manifest': manifest, 'records': records}
        report['scenarios'].append(entry)
        (out / 'receipt.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(scenario, f'{passed}/{len(checks)}', [s['status'] for s in slices], 'augmented:', repaired_ok, flush=True)

if __name__ == '__main__':
    main()
