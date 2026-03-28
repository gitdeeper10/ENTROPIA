"""
ENTROPIA Parameters Module
Five governing parameters: ρ, ρ_c, Ψ, σ, τ_collapse

Author: Samir Baladi
Reference: ENTROPIA Research Paper, Section 3
"""

import math
from typing import Optional

# Boltzmann constant (J/K)
k_B = 1.380649e-23
# Electron volt in Joules
eV = 1.602176634e-19


class DataDensity:
    """
    Data Density ρ = Φ / V_effective
    
    Units: bits·s⁻¹·m⁻³
    
    Reference: ENTROPIA Research Paper, Eq. 7
    """
    
    def __init__(self, bit_rate: float, effective_volume: float):
        self.bit_rate = bit_rate
        self.effective_volume = effective_volume
        self._value = bit_rate / effective_volume
    
    @property
    def value(self) -> float:
        return self._value
    
    def __float__(self):
        return float(self._value)
    
    def __repr__(self):
        return f"DataDensity(ρ={self._value:.2e} bits·s⁻¹·m⁻³)"


class CriticalThroughput:
    """
    Critical Throughput Threshold ρ_c
    
    Units: bits·s⁻¹·m⁻³
    
    Reference: ENTROPIA Research Paper, Eq. 8
    """
    
    def __init__(
        self, 
        omega_max: float, 
        omega_min: float, 
        temperature: float, 
        energy_per_bit: float
    ):
        self.omega_max = omega_max
        self.omega_min = omega_min
        self.temperature = temperature
        self.energy_per_bit = energy_per_bit
        
        numerator = omega_max * k_B * temperature
        denominator = energy_per_bit * math.log(omega_max / omega_min)
        self._value = numerator / denominator
    
    @property
    def value(self) -> float:
        return self._value
    
    def __float__(self):
        return float(self._value)
    
    def __repr__(self):
        return f"CriticalThroughput(ρ_c={self._value:.2e} bits·s⁻¹·m⁻³)"


class DissipationCoefficient:
    """
    Dissipation Coefficient Ψ(ρ)
    
    Units: dimensionless
    Critical threshold: Ψ_c = 2.0
    
    Reference: ENTROPIA Research Paper, Eq. 9
    """
    
    CRITICAL_THRESHOLD = 2.0
    
    def __init__(self, rho: float, rho_c: float, S_total: float, S_max: float):
        self.rho = rho
        self.rho_c = rho_c
        self.S_total = S_total
        self.S_max = S_max
        self.rho_ratio = rho / rho_c if rho_c > 0 else 0
        self.S_ratio = S_total / S_max if S_max > 0 else 0
        
        if rho >= rho_c:
            self.divergent = True
            self._value = float('inf')
        else:
            self.divergent = False
            self._value = (S_total / S_max) * (1 - (rho_c / rho) ** 2) ** (-1)
    
    @property
    def value(self) -> float:
        return self._value
    
    def is_critical(self) -> bool:
        return self.divergent or self._value >= self.CRITICAL_THRESHOLD
    
    def risk_level(self) -> str:
        if self.divergent or self._value >= self.CRITICAL_THRESHOLD:
            return "🔴 COLLAPSE IMMINENT"
        elif self._value >= 1.4:
            return "🔶 CRITICAL"
        elif self._value >= 0.7:
            return "⚠️ ELEVATED"
        else:
            return "✅ NORMAL"
    
    def __float__(self):
        return float(self._value)
    
    def __repr__(self):
        if self.divergent:
            return f"DissipationCoefficient(Ψ=∞, divergent at ρ={self.rho:.2e})"
        return f"DissipationCoefficient(Ψ={self._value:.3f})"


class EntropyProductionRate:
    """
    Entropy Production Rate σ(ρ, T)
    
    Units: J·K⁻¹·m⁻³·s⁻¹
    
    Reference: ENTROPIA Research Paper, Eq. 10
    """
    
    def __init__(
        self, 
        rho: float, 
        rho_c: float, 
        temperature: float,
        scaling_exponent: float = 1.85,
        activation_energy: float = 0.6,
        prefactor: float = 1.0
    ):
        self.rho = rho
        self.rho_c = rho_c
        self.temperature = temperature
        self.scaling_exponent = scaling_exponent
        self.activation_energy = activation_energy
        
        # Convert activation energy from eV to J
        E_a_joules = activation_energy * eV
        
        # Power-law term
        if rho_c > 0 and rho > 0:
            power_law = (rho / rho_c) ** scaling_exponent
        else:
            power_law = 0.0
        
        # Arrhenius term
        if temperature > 0:
            arrhenius = math.exp(-E_a_joules / (k_B * temperature))
        else:
            arrhenius = 0.0
        
        self._value = prefactor * k_B * power_law * arrhenius
    
    @property
    def value(self) -> float:
        return self._value
    
    def __float__(self):
        return float(self._value)
    
    def __repr__(self):
        return f"EntropyProductionRate(σ={self._value:.2e} J·K⁻¹·m⁻³·s⁻¹)"


class CollapseLeadTime:
    """
    Collapse Lead Time τ_collapse
    
    Time remaining before Dissipation Coefficient reaches critical threshold.
    
    Units: seconds
    
    Reference: ENTROPIA Research Paper, Eq. 11
    """
    
    def __init__(self, psi_current: float, dpsi_dt: float, psi_critical: float = 2.0):
        self.psi_current = psi_current
        self.dpsi_dt = dpsi_dt
        self.psi_critical = psi_critical
        
        if dpsi_dt <= 0:
            self._value = float('inf')
        elif psi_current >= psi_critical:
            self._value = 0.0
        else:
            self._value = (psi_critical - psi_current) / abs(dpsi_dt)
    
    @property
    def value(self) -> float:
        return self._value
    
    def is_actionable(self, min_seconds: float = 30.0) -> bool:
        """Check if lead time is sufficient for intervention"""
        return self._value >= min_seconds
    
    def __float__(self):
        return float(self._value)
    
    def __repr__(self):
        if self._value == float('inf'):
            return "CollapseLeadTime(τ=∞, system stable)"
        return f"CollapseLeadTime(τ={self._value:.1f} seconds)"


__all__ = [
    "DataDensity",
    "CriticalThroughput",
    "DissipationCoefficient",
    "EntropyProductionRate",
    "CollapseLeadTime",
]
