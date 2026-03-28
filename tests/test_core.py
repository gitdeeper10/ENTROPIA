"""
Unit tests for ENTROPIA core module
"""

import unittest
import math
from entropia.core import (
    boltzmann_entropy,
    shannon_entropy,
    unified_state_function,
    entropy_balance,
    steady_state_condition,
    k_B
)


class TestCore(unittest.TestCase):
    
    def test_boltzmann_entropy(self):
        """Test Boltzmann entropy calculation"""
        S = boltzmann_entropy(1e6)
        expected = k_B * math.log(1e6)
        self.assertAlmostEqual(S, expected, places=10)
        
        # Test error on invalid input
        with self.assertRaises(ValueError):
            boltzmann_entropy(0)
    
    def test_shannon_entropy(self):
        """Test Shannon entropy calculation"""
        probs = [0.5, 0.3, 0.2]
        H = shannon_entropy(probs, base=2)
        expected = -(0.5*math.log2(0.5) + 0.3*math.log2(0.3) + 0.2*math.log2(0.2))
        self.assertAlmostEqual(H, expected, places=6)
        
        # Test uniform distribution
        probs = [0.25, 0.25, 0.25, 0.25]
        H = shannon_entropy(probs, base=2)
        self.assertAlmostEqual(H, 2.0, places=6)
        
        # Test error on invalid probabilities
        with self.assertRaises(ValueError):
            shannon_entropy([0.6, 0.6])
    
    def test_unified_state_function(self):
        """Test unified state function"""
        micro_probs = [0.5, 0.3, 0.2]
        symbol_probs = [0.4, 0.3, 0.2, 0.1]
        
        S_total = unified_state_function(
            microstate_probabilities=micro_probs,
            symbol_probabilities=symbol_probs,
            alpha=0.85,
            beta=0.15
        )
        
        self.assertGreater(S_total, 0)
        
        # Test alpha+beta=1 validation
        with self.assertRaises(ValueError):
            unified_state_function(micro_probs, symbol_probs, alpha=0.9, beta=0.2)
    
    def test_entropy_balance(self):
        """Test entropy balance equation"""
        # Test with dS_dt directly
        result = entropy_balance(dS_dt=1e-19)
        self.assertEqual(result["dS_dt"], 1e-19)
        
        # Test with production and flux
        result = entropy_balance(production_rate=1e-19, flux_divergence=-0.5e-19)
        self.assertAlmostEqual(result["dS_dt"], 0.5e-19)
        
        # Test error on no inputs
        with self.assertRaises(ValueError):
            entropy_balance()
    
    def test_steady_state_condition(self):
        """Test steady state condition"""
        # True steady state (production = -flux)
        self.assertTrue(steady_state_condition(1e-19, -1e-19))
        
        # Not steady state - should return False
        # Note: with tolerance 1e-6, 0.5e-19 difference is less than tolerance
        # So we need a larger difference to test false case
        self.assertFalse(steady_state_condition(1e-19, -0.5e-19, tolerance=1e-20))


if __name__ == "__main__":
    unittest.main()
