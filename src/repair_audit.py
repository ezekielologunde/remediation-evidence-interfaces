"""Original finite-domain feasibility audit. Not AWS or Cedar semantics."""
from itertools import product
from pathlib import Path
import hashlib
import json

FIELDS = ('principal', 'action', 'resource', 'trusted')
DOMAINS = (('analyst', 'operator', 'guest'), ('read', 'write'), ('logs', 'config'), (False, True))
REQUESTS = tuple(product(*DOMAINS))

def rule(effect, **conditions):
    if effect not in ('allow', 'deny') or set(conditions) - set(FIELDS):
        raise ValueError('Unsupported rule')
    for key, value in conditions.items():
        if not any(type(value) is type(v) and value == v for v in DOMAINS[FIELDS.index(key)]):
            raise ValueError('Unsupported condition')
    return (effect, conditions)

def evaluate(policy, request):
    if len(request) != 4 or any(not any(type(x) is type(v) and x == v for v in domain) for x, domain in zip(request, DOMAINS)):
        raise ValueError('Request outside declared universe')
    effects = set()
    for effect, conditions in policy:
        rule(effect, **conditions)
        if all(request[FIELDS.index(k)] == v for k, v in conditions.items()):
            effects.add(effect)
    return 'allow' in effects and 'deny' not in effects

def oracle(request):
    # Independently expressed requirement, not evaluated through the rule engine.
    principal, action, resource, trusted = request
    return trusted and ((principal == 'analyst' and action == 'read' and resource == 'logs') or principal == 'operator')

BASE = [rule('allow', principal='analyst', action='read', resource='logs', trusted=True)]
GOOD = BASE + [rule('allow', principal='operator', trusted=True)]
BROAD = BASE + [rule('allow', principal='operator')]
BLOCKING = GOOD + [rule('deny', action='write')]
VISIBLE = (('operator', 'read', 'config', True), ('guest', 'read', 'logs', True))
POLICIES = {'initial': BASE, 'targeted': GOOD, 'overbroad': BROAD,
            'write_blocked': BLOCKING, 'equivalent': list(reversed(GOOD)) + [GOOD[0]]}

def audit(before, after):
    rows = []
    for request in REQUESTS:
        previous, current, expected = evaluate(before, request), evaluate(after, request), oracle(request)
        rows.append({'request': dict(zip(FIELDS, request)), 'before': previous, 'after': current, 'expected': expected})
    regressed = [r for r in rows if r['before'] == r['expected'] and r['after'] != r['expected']]
    return {'universe_size': len(rows),
            'visible_passed': sum(evaluate(after, r) == oracle(r) for r in VISIBLE),
            'visible_total': len(VISIBLE),
            'mismatches': sum(r['after'] != r['expected'] for r in rows),
            'fixed': sum(r['before'] != r['expected'] and r['after'] == r['expected'] for r in rows),
            'new_security_regressions': sum(r['after'] and not r['expected'] for r in regressed),
            'new_availability_regressions': sum(not r['after'] and r['expected'] for r in regressed),
            'regression_witnesses': regressed}

def main():
    transitions = [('initial', 'targeted'), ('initial', 'overbroad'), ('targeted', 'write_blocked'), ('targeted', 'equivalent'), ('overbroad', 'targeted')]
    report = {'status': 'synthetic feasibility only; hand-authored repairs; no LLM evaluated',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'oracle_allowed': sum(map(oracle, REQUESTS)),
              'transitions': {f'{a}->{b}': audit(POLICIES[a], POLICIES[b]) for a,b in transitions}}
    output = Path(__file__).resolve().parents[1] / 'analysis' / 'repair-feasibility.json'
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: {m:v for m,v in r.items() if m != 'regression_witnesses'} for k,r in report['transitions'].items()}, indent=2))

if __name__ == '__main__':
    main()
