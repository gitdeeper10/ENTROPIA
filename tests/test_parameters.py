import unittest
from entropia.parameters import CollapseLeadTime

class TestParameters(unittest.TestCase):
    def test_collapse_lead_time(self):
        tau = CollapseLeadTime(psi_current=2.5, dpsi_dt=0.02)
        print(f"\nDEBUG: tau._value = {tau._value}")
        print(f"DEBUG: tau.is_actionable(10) = {tau.is_actionable(10)}")
        self.assertFalse(tau.is_actionable(min_seconds=10))

if __name__ == "__main__":
    unittest.main()
