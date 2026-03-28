"""
E-ENV-01: Static Closed-Form Network

Simplified closed information system with N = 10³ processing nodes,
each with fixed capacity, connected by symmetric random graph.

Reference: ENTROPIA Research Paper, Section 4.2
"""

import math
from typing import Dict, Any, Optional


class ENV01StaticNetwork:
    """
    Static closed-form network simulation environment.
    
    Args:
        n_nodes: Number of processing nodes (default: 1000)
        mean_degree: Average node degree (default: 20)
        node_capacity: Microstates per node (default: 1000)
    """
    
    def __init__(
        self,
        n_nodes: int = 1000,
        mean_degree: int = 20,
        node_capacity: int = 1000
    ):
        self.n_nodes = n_nodes
        self.mean_degree = mean_degree
        self.node_capacity = node_capacity
        self.total_microstates = n_nodes * node_capacity
        
        # Simulation state
        self.current_load = 0.0
        self.rho = 0.0
        self.psi = 0.0
        self.collapsed = False
        
    def run(self, duration: float = 3600.0, seed: int = 42) -> Dict[str, Any]:
        """
        Run simulation for specified duration.
        
        Args:
            duration: Simulation duration in seconds
            seed: Random seed for reproducibility
        
        Returns:
            Simulation results dictionary
        """
        # Set seed (simple implementation without random)
        _ = seed
        
        # Linear increase of data density from 0 to 2ρ_c
        rho_c = self.total_microstates / 1000.0  # Simplified critical threshold
        results = []
        
        for t in range(0, int(duration), 10):  # 10-second steps
            self.current_load = t / duration  # 0 to 1
            self.rho = self.current_load * 2 * rho_c
            
            # Compute Ψ based on ENTROPIA Eq. 9
            if self.rho < rho_c:
                rho_ratio = self.rho / rho_c
                self.psi = (self.current_load) * (1 - (1 / rho_ratio)**2)**(-1) if rho_ratio > 0 else 0
            else:
                self.psi = float('inf')
                self.collapsed = True
            
            results.append({
                "time": t,
                "rho": self.rho,
                "rho_c": rho_c,
                "psi": self.psi,
                "collapsed": self.collapsed
            })
            
            if self.collapsed:
                break
        
        return {
            "environment": "E-ENV-01",
            "n_nodes": self.n_nodes,
            "duration": duration,
            "collapsed_at": t if self.collapsed else None,
            "results": results
        }
    
    def summary(self) -> str:
        """Return summary of simulation results"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ E-ENV-01 Static Network Summary                              ║
╠══════════════════════════════════════════════════════════════╣
║ Nodes:              {self.n_nodes}
║ Total microstates:  {self.total_microstates}
║ Collapsed:          {self.collapsed}
╚══════════════════════════════════════════════════════════════╝
        """


__all__ = ["ENV01StaticNetwork"]
