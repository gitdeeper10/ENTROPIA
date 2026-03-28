"""
ENTROPIA Core Module
Unified Dissipation State Function and Master Equations

Author: Samir Baladi
Reference: ENTROPIA Research Paper, Section 2
"""

import math
from typing import Union, Optional, List

# Boltzmann constant (J/K) - قيمة ثابتة
k_B = 1.380649e-23


def boltzmann_entropy(omega: Union[int, float], k: float = k_B) -> float:
    """
    Boltzmann statistical entropy: S = k_B ln Ω
    
    Args:
        omega: Number of accessible microstates
        k: Boltzmann constant (default: k_B)
    
    Returns:
        Entropy in J/K
    """
    if omega <= 0:
        raise ValueError("Ω must be positive")
    return k * math.log(omega)


def shannon_entropy(
    probabilities: List[float], 
    base: float = 2.0
) -> float:
    """
    Shannon information entropy: H = -Σ p_i log(p_i)
    
    Args:
        probabilities: List of symbol probabilities
        base: Logarithm base (2 for bits, e for nats)
    
    Returns:
        Entropy in bits or nats
    """
    # Validate probabilities sum to 1
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Probabilities must sum to 1, got {total}")
    
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            if base == 2:
                entropy -= p * math.log2(p)
            elif base == math.e:
                entropy -= p * math.log(p)
            else:
                entropy -= p * math.log(p) / math.log(base)
    
    return entropy


def unified_state_function(
    microstate_probabilities: List[float],
    symbol_probabilities: List[float],
    alpha: float = 0.85,
    beta: float = 0.15,
    temperature: float = 300.0
) -> float:
    """
    Unified Dissipation State Function S_total
    
    S_total = α·k_B[-Σ p_i ln p_i] + β·k_B[-Σ P(x_i) ln P(x_i)]
    
    Reference: ENTROPIA Research Paper, Eq. 4
    """
    if abs(alpha + beta - 1.0) > 1e-6:
        raise ValueError(f"α + β must equal 1, got {alpha + beta}")
    
    # Gibbs entropy: S_G = -k_B Σ p_i ln p_i
    S_G = 0.0
    for p in microstate_probabilities:
        if p > 0:
            S_G -= k_B * p * math.log(p)
    
    # Shannon entropy in nats: H_nats = -Σ P(x_i) ln P(x_i)
    H_nats = 0.0
    for p in symbol_probabilities:
        if p > 0:
            H_nats -= p * math.log(p)
    
    # Convert to thermodynamic units: k_B * H_nats
    H_thermo = k_B * H_nats
    
    # Unified state function
    S_total = alpha * S_G + beta * H_thermo
    
    return S_total


def entropy_balance(
    production_rate: Optional[float] = None,
    flux_divergence: Optional[float] = None,
    dS_dt: Optional[float] = None
) -> dict:
    """
    Entropy balance equation: dS/dt = σ_production + ∇·J_S
    
    Reference: ENTROPIA Research Paper, Eq. 5
    """
    if dS_dt is not None:
        return {
            "dS_dt": dS_dt,
            "sigma_production": production_rate,
            "flux_divergence": flux_divergence
        }
    
    if production_rate is not None and flux_divergence is not None:
        dS_dt = production_rate + flux_divergence
    elif production_rate is not None:
        dS_dt = production_rate
    elif flux_divergence is not None:
        dS_dt = flux_divergence
    else:
        raise ValueError("Must provide production_rate, flux_divergence, or dS_dt")
    
    return {
        "dS_dt": dS_dt,
        "sigma_production": production_rate,
        "flux_divergence": flux_divergence
    }


def steady_state_condition(
    production_rate: float,
    flux_divergence: float,
    tolerance: float = 1e-6
) -> bool:
    """
    Check if system is in thermodynamic steady state.
    
    Steady-state condition: σ_production = -∇·J_S
    
    Reference: ENTROPIA Research Paper, Eq. 6
    """
    return abs(production_rate + flux_divergence) < tolerance


__all__ = [
    "k_B",
    "boltzmann_entropy",
    "shannon_entropy",
    "unified_state_function",
    "entropy_balance",
    "steady_state_condition",
]
