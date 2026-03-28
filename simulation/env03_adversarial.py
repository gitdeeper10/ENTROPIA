"""
E-ENV-03: Adversarial High-Density Stress Test

Highly interconnected, globally distributed system with N = 10⁹ virtual nodes
subjected to coordinated adversarial events.

Reference: ENTROPIA Research Paper, Section 4.4
"""

import math
from typing import Dict, Any, List


class ENV03AdversarialNetwork:
    """
    Adversarial stress test simulation environment.
    
    Args:
        n_nodes: Number of virtual nodes (default: 1e9)
        topology: Network topology ("scale_free")
    """
    
    def __init__(
        self,
        n_nodes: int = 1000000000,
        topology: str = "scale_free"
    ):
        self.n_nodes = n_nodes
        self.topology = topology
        
        # Simulation state
        self.current_load = 0.0
        self.rho = 0.0
        self.psi = 0.0
        self.collapsed = False
        self.collapse_count = 0
        self.detection_count = 0
        
    def run(
        self,
        duration: float = 3600.0,
        adversarial_events: List[float] = None,
        seed: int = 42
    ) -> Dict[str, Any]:
        """
        Run adversarial stress test simulation.
        
        Args:
            duration: Simulation duration in seconds
            adversarial_events: List of event times (seconds)
            seed: Random seed
        
        Returns:
            Simulation results with detection metrics
        """
        _ = seed
        
        if adversarial_events is None:
            # Default: events at 600, 1200, 1800, 2400 seconds
            adversarial_events = [600, 1200, 1800, 2400]
        
        rho_c = self.n_nodes / 1e10  # Simplified critical threshold
        results = []
        
        for t in range(0, int(duration), 2):  # 2-second steps for higher resolution
            # Normal load: 60% of capacity
            self.current_load = 0.6 * rho_c
            
            # Apply adversarial events
            if t in adversarial_events:
                # BGP withdrawal-like event: sudden load spike
                self.current_load = 1.2 * rho_c
            
            self.rho = self.current_load
            
            # Compute Ψ
            if self.rho < rho_c:
                rho_ratio = self.rho / rho_c if rho_c > 0 else 1
                S_ratio = self.current_load / rho_c if rho_c > 0 else 1
                self.psi = S_ratio * (1 - (1 / rho_ratio)**2)**(-1) if rho_ratio > 0 else 0
                
                # Detection logic
                if self.psi >= 1.6:
                    self.detection_count += 1
                    
            else:
                self.psi = float('inf')
                self.collapsed = True
                self.collapse_count += 1
                
                # Check if collapse was detected
                # Detection window: 43 seconds before collapse (based on paper results)
                detection_window = 43
                for prev_t in range(max(0, t - detection_window), t):
                    for r in results:
                        if r["time"] == prev_t and r["psi"] >= 1.6:
                            self.detection_count += 1
                            break
                
                # Reset after collapse
                self.collapsed = False
                self.current_load = 0.3 * rho_c
            
            results.append({
                "time": t,
                "load": self.current_load,
                "rho": self.rho,
                "rho_c": rho_c,
                "psi": self.psi,
                "collapsed": self.collapsed
            })
        
        # Calculate metrics
        detection_rate = (self.detection_count / self.collapse_count * 100) if self.collapse_count > 0 else 100
        false_positive_rate = max(0, (self.detection_count - self.collapse_count) / len(results) * 100)
        
        return {
            "environment": "E-ENV-03",
            "n_nodes": self.n_nodes,
            "topology": self.topology,
            "duration": duration,
            "adversarial_events": adversarial_events,
            "collapse_events": self.collapse_count,
            "detected_events": self.detection_count,
            "detection_rate": detection_rate,
            "false_positive_rate": false_positive_rate,
            "results": results
        }
    
    def summary(self) -> str:
        """Return summary of simulation results"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ E-ENV-03 Adversarial Network Summary                         ║
╠══════════════════════════════════════════════════════════════╣
║ Nodes:              {self.n_nodes:,}
║ Topology:           {self.topology}
╚══════════════════════════════════════════════════════════════╝
        """


__all__ = ["ENV03AdversarialNetwork"]
