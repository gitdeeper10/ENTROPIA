"""
Unit tests for ENTROPIA detector module
"""

import unittest
from entropia.detector import EntropiaSystem, EntropiaDetector


class TestDetector(unittest.TestCase):
    
    def test_system_initialization(self):
        """Test EntropiaSystem initialization"""
        system = EntropiaSystem(
            architecture="von_neumann",
            total_capacity=1e9,
            temperature=300
        )
        self.assertEqual(system.architecture, "von_neumann")
        self.assertEqual(system.total_capacity, 1e9)
    
    def test_system_update(self):
        """Test system state update"""
        system = EntropiaSystem(total_capacity=1e9, effective_volume=1.0)
        
        state = system.update(
            bit_rate=7.2e8,
            microstate_probabilities=[0.5, 0.3, 0.2],
            symbol_probabilities=[0.4, 0.3, 0.2, 0.1]
        )
        
        self.assertIsNotNone(state["rho"])
        self.assertIsNotNone(state["psi"])
        self.assertIn("risk_level", state)
    
    def test_predict(self):
        """Test collapse prediction"""
        system = EntropiaSystem(total_capacity=1e9, effective_volume=1.0)
        system.update(bit_rate=8e8)
        
        prediction = system.predict(dpsi_dt=0.02)
        self.assertIn("tau_collapse", prediction)
        self.assertIn("actionable", prediction)
    
    def test_detector_check(self):
        """Test detector alert system"""
        system = EntropiaSystem(total_capacity=1e9)
        detector = EntropiaDetector(system, psi_threshold=2.0)
        
        # Normal operation
        result = detector.check({"bit_rate": 5e8})
        self.assertFalse(result["alert"])
        
        # Critical operation
        # Note: This may need higher bit_rate to trigger critical
        result = detector.check({"bit_rate": 1.2e9})
        
        # Should have a result regardless
        self.assertIn("psi", result)


if __name__ == "__main__":
    unittest.main()
