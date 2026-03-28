"""
ENTROPIA Simulation Environments

Three validated simulation environments:
- E-ENV-01: Static closed-form network (10³ nodes)
- E-ENV-02: Dynamic streaming network (10⁵ nodes)
- E-ENV-03: Adversarial stress test (10⁹ nodes)

Reference: ENTROPIA Research Paper, Section 4
"""

from simulation.env01_static import ENV01StaticNetwork
from simulation.env02_streaming import ENV02StreamingNetwork
from simulation.env03_adversarial import ENV03AdversarialNetwork

__all__ = [
    "ENV01StaticNetwork",
    "ENV02StreamingNetwork",
    "ENV03AdversarialNetwork",
]
