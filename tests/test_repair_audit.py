import unittest
from src.repair_audit import *

class AuditTests(unittest.TestCase):
    def test_universe(self):
        self.assertEqual(len(set(REQUESTS)), 24)
        self.assertEqual(sum(map(oracle, REQUESTS)), 5)
    def test_gold_full_domain(self):
        self.assertTrue(all(evaluate(GOOD, r) == oracle(r) for r in REQUESTS))
    def test_default_deny(self):
        self.assertFalse(any(evaluate([], r) for r in REQUESTS))
    def test_deny_overrides(self):
        self.assertFalse(evaluate([rule('deny'), rule('allow')], REQUESTS[0]))
    def test_invalid(self):
        for kwargs in ({'typo': True}, {'trusted': 1}, {'principal': 'unknown'}):
            with self.assertRaises(ValueError): rule('allow', **kwargs)
        with self.assertRaises(ValueError): evaluate(GOOD, ('guest', 'read', 'logs', 1))
    def test_overbroad(self):
        r = audit(BASE, BROAD)
        self.assertEqual((r['visible_passed'], r['fixed'], r['mismatches'], r['new_security_regressions']), (2,4,4,4))
    def test_availability(self):
        r = audit(GOOD, BLOCKING)
        self.assertEqual((r['visible_passed'], r['new_availability_regressions']), (2,2))
    def test_equivalence(self):
        self.assertEqual(audit(GOOD, POLICIES['equivalent'])['mismatches'], 0)
    def test_recovery(self):
        r = audit(BROAD, GOOD)
        self.assertEqual((r['fixed'], r['mismatches']), (4,0))
    def test_conservation_all_pairs(self):
        for before in POLICIES.values():
            old = sum(evaluate(before,r) != oracle(r) for r in REQUESTS)
            for after in POLICIES.values():
                r = audit(before, after)
                self.assertEqual(r['mismatches'], old-r['fixed']+r['new_security_regressions']+r['new_availability_regressions'])

if __name__ == '__main__': unittest.main()
