"""
ENTROPIA Detector Module
Ψ-Dashboard real-time monitoring and prediction engine

Author: Samir Baladi
Reference: ENTROPIA Research Paper, Section 5
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from entropia.parameters import (
    DataDensity,
    CriticalThroughput,
    DissipationCoefficient,
    EntropyProductionRate,
    CollapseLeadTime,
)


@dataclass
class EntropiaSystem:
    """
    Main ENTROPIA system class for monitoring digital infrastructure.
    """
    
    architecture: str = "von_neumann"
    total_capacity: float = 1e9
    temperature: float = 300.0
    effective_volume: float = 1.0
    max_entropy: float = 1e-18
    
    scaling_exponent: float = 1.85
    alpha: float = 0.85
    beta: float = 0.15
    
    bit_rate: float = 0.0
    microstate_probabilities: list = field(default_factory=list)
    symbol_probabilities: list = field(default_factory=list)
    
    data_density: Optional[DataDensity] = None
    critical_threshold: Optional[CriticalThroughput] = None
    psi: Optional[DissipationCoefficient] = None
    sigma: Optional[EntropyProductionRate] = None
    tau: Optional[CollapseLeadTime] = None
    
    def __post_init__(self):
        if not self.microstate_probabilities:
            self.microstate_probabilities = [1.0]
        if not self.symbol_probabilities:
            self.symbol_probabilities = [1.0]
    
    def update(
        self,
        bit_rate: Optional[float] = None,
        microstate_probabilities: Optional[list] = None,
        symbol_probabilities: Optional[list] = None,
        dpsi_dt: Optional[float] = None
    ) -> Dict[str, Any]:
        if bit_rate is not None:
            self.bit_rate = bit_rate
        
        if microstate_probabilities is not None:
            self.microstate_probabilities = microstate_probabilities
        
        if symbol_probabilities is not None:
            self.symbol_probabilities = symbol_probabilities
        
        self.data_density = DataDensity(
            bit_rate=self.bit_rate,
            effective_volume=self.effective_volume
        )
        
        rho_c_value = self.total_capacity / self.effective_volume
        
        self.critical_threshold = CriticalThroughput(
            omega_max=1e6,
            omega_min=1e3,
            temperature=self.temperature,
            energy_per_bit=1e-21
        )
        self.critical_threshold._value = rho_c_value
        
        S_total = self._compute_entropy()
        
        self.psi = DissipationCoefficient(
            rho=float(self.data_density),
            rho_c=float(self.critical_threshold),
            S_total=S_total,
            S_max=self.max_entropy
        )
        
        self.sigma = EntropyProductionRate(
            rho=float(self.data_density),
            rho_c=float(self.critical_threshold),
            temperature=self.temperature,
            scaling_exponent=self.scaling_exponent
        )
        
        if dpsi_dt is not None:
            self.tau = CollapseLeadTime(
                psi_current=self.psi.value,
                dpsi_dt=dpsi_dt
            )
        
        return self.get_state()
    
    def _compute_entropy(self) -> float:
        from entropia.core import unified_state_function
        
        return unified_state_function(
            microstate_probabilities=self.microstate_probabilities,
            symbol_probabilities=self.symbol_probabilities,
            alpha=self.alpha,
            beta=self.beta,
            temperature=self.temperature
        )
    
    def get_state(self) -> Dict[str, Any]:
        state = {
            "bit_rate": self.bit_rate,
            "rho": float(self.data_density) if self.data_density else None,
            "rho_c": float(self.critical_threshold) if self.critical_threshold else None,
            "rho_ratio": self.psi.rho_ratio if self.psi else None,
            "psi": self.psi.value if self.psi else None,
            "risk_level": self.psi.risk_level() if self.psi else "UNKNOWN",
            "is_critical": self.psi.is_critical() if self.psi else False,
            "sigma": float(self.sigma) if self.sigma else None,
            "tau_collapse": float(self.tau) if self.tau else None,
        }
        
        if self.tau and self.tau.is_actionable():
            state["alert"] = f"⚠️ Collapse in {self.tau.value:.0f} seconds"
        
        return state
    
    def predict(self, dpsi_dt: float) -> Dict[str, Any]:
        if self.psi is None:
            return {"error": "System not initialized. Call update() first."}
        
        self.tau = CollapseLeadTime(
            psi_current=self.psi.value,
            dpsi_dt=dpsi_dt
        )
        
        return {
            "tau_collapse": self.tau.value,
            "actionable": self.tau.is_actionable(),
            "warning": self.tau.value < 30 and self.tau.value > 0
        }


class EntropiaDetector:
    def __init__(self, system: EntropiaSystem, psi_threshold: float = 2.0):
        self.system = system
        self.psi_threshold = psi_threshold
        self.alert_history = []
    
    def check(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        self.system.update(**telemetry)
        state = self.system.get_state()
        
        result = {
            "timestamp": None,
            "psi": state["psi"],
            "risk_level": state["risk_level"],
            "alert": False
        }
        
        if state["is_critical"]:
            result["alert"] = True
            result["alert_message"] = f"CRITICAL: Ψ={state['psi']:.3f} > {self.psi_threshold}"
            self.alert_history.append(result)
        
        return result
    
    def get_alert_history(self) -> list:
        return self.alert_history


__all__ = [
    "EntropiaSystem",
    "EntropiaDetector",
]
