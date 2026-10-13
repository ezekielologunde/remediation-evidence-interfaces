"""Independent Boolean abstraction of pinned clinical_add_consent checks.

Not a Cedar interpreter or native symcc reproduction. Boolean variables denote
the predicates appearing in the published spec and nine reference policies.
"""
import itertools
import json

FIELDS = ('active', 'cr', 'pi', 'auditor', 'clearance_ok',
          'classification_ok', 'risk_ok', 'device_ok', 'same_dept', 'consent')

def audit():
    failures = []
    witnesses = []
    live = {'View': False, 'Edit': False}
    count = 0
    repaired_floor_rejections = 0
    for values in itertools.product((False, True), repeat=len(FIELDS)):
        q = dict(zip(FIELDS, values))
        qualified = q['active'] and (
            (q['cr'] and q['clearance_ok'] and q['classification_ok']) or
            (q['pi'] and q['risk_ok'] and q['device_ok']))
        for action in ('View', 'Edit'):
            count += 1
            consent_ok = action == 'View' or q['consent']
            intended = qualified and (q['same_dept'] or q['auditor']) and consent_ok
            candidate = qualified and q['same_dept'] and consent_ok
            auditor_floor = qualified and q['auditor'] and consent_ok
            repaired_floor_rejections += int(auditor_floor and not candidate)
            ceiling = qualified and consent_ok
            dept_ceiling = q['same_dept'] or q['auditor']
            floor_cr = (q['active'] and q['cr'] and q['clearance_ok'] and
                        q['classification_ok'] and q['same_dept'] and consent_ok)
            floor_pi = (q['active'] and q['pi'] and q['risk_ok'] and
                        q['device_ok'] and q['same_dept'] and consent_ok)
            checks = {
                'safety': not candidate or ceiling,
                'department': not candidate or dept_ceiling,
                'consent': action == 'View' or not candidate or q['consent'],
                'floor_cr': not floor_cr or candidate,
                'floor_pi': not floor_pi or candidate,
            }
            if not all(checks.values()):
                failures.append({'request': q, 'action': action, 'checks': checks})
            live[action] |= candidate
            if intended and not candidate:
                witnesses.append({'action': action, **q})
    assert not failures
    assert all(live.values())
    assert witnesses
    assert repaired_floor_rejections == len(witnesses)
    return {'scope': 'Boolean abstraction only; native Cedar verification pending',
            'upstream_commit': '0201565abf5993e258764d3f0ef83a59d3b4962e',
            'scenario': 'clinical_add_consent', 'valuations': count,
            'boundary_violations': len(failures), 'liveness': live,
            'spec_allow_candidate_deny_valuations': len(witnesses),
            'added_auditor_floor_rejections': repaired_floor_rejections,
            'example': witnesses[0],
            'interpretation': 'Coverage counterexample, not empirical prevalence or novelty proof'}

if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
