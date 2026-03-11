import json
from decimal import Decimal, getcontext
from typing import Dict, List, Callable, Any
from dataclasses import dataclass

# High precision for exact unity
getcontext().prec = 28
getcontext().rounding = "ROUND_HALF_EVEN"

@dataclass
class FiniteElement:
    name: str
    func: Callable[[Dict[str, Decimal]], Decimal]  # Input dict → exact contribution
    description: str

class Regime:
    def __init__(self, name: str, elements: List[FiniteElement], weights: List[Decimal]):
        self.name = name
        self.elements = elements
        self.weights = weights
        total = sum(weights)
        assert total == Decimal('1'), f"{name} weights must sum exactly to 1 (got {total})"

    def evaluate(self, input_data: Dict[str, Decimal]) -> Decimal:
        contributions = [element.func(input_data) for element in self.elements]
        return sum(w * c for w, c in zip(self.weights, contributions))

class UnitySumSystem:
    def __init__(self, name: str, regimes: List[Regime], regime_weights: List[Decimal]):
        self.name = name
        self.regimes = regimes
        self.regime_weights = regime_weights
        total = sum(regime_weights)
        assert total == Decimal('1'), f"Top-level weights must sum exactly to 1 (got {total})"

    def evaluate(self, input_data: Dict[str, Decimal]) -> Dict[str, Any]:
        regime_scores = {r.name: r.evaluate(input_data) for r in self.regimes}
        total_score = sum(w * regime_scores[r.name] for w, r in zip(self.regime_weights, self.regimes))
        contributions = {r.name: self.regime_weights[i] * regime_scores[r.name] for i, r in enumerate(self.regimes)}
        return {
            "total_impact_score": total_score,
            "impact_tier": "High" if total_score >= Decimal('0.7') else "Medium" if total_score >= Decimal('0.4') else "Low",
            "regime_breakdown": {k: float(v) for k, v in regime_scores.items()},  # Float for display
            "weighted_contributions": {k: float(v) for k, v in contributions.items()},
            "contribution_percent": {k: f"{(v / total_score * 100 if total_score > 0 else 0):.1f}%" for k, v in contributions.items()}
        }

# Expanded Kardashev Elements
def energy_element(input_data: Dict[str, Decimal]) -> Decimal:
    tech = input_data.get("energy_tech", Decimal('0'))
    invest = input_data.get("investment", Decimal('0'))
    return min(tech + Decimal('0.3') * invest, Decimal('1'))

def tech_element(input_data: Dict[str, Decimal]) -> Decimal:
    ai = input_data.get("ai_advancement", Decimal('0.5'))
    compute = input_data.get("compute_scale", Decimal('0.5'))
    return min(ai * Decimal('0.6') + compute * Decimal('0.4'), Decimal('1'))

def society_element(input_data: Dict[str, Decimal]) -> Decimal:
    cohesion = input_data.get("social_cohesion", Decimal('0.8'))
    education = input_data.get("education_level", Decimal('0.7'))
    return cohesion * education ** Decimal('0.5')

def environment_element(input_data: Dict[str, Decimal]) -> Decimal:
    sustainability = input_data.get("sustainability_index", Decimal('0.6'))
    climate_risk = Decimal('1') - input_data.get("climate_risk", Decimal('0.3'))
    return sustainability * climate_risk

def geopolitics_element(input_data: Dict[str, Decimal]) -> Decimal:
    cooperation = input_data.get("global_cooperation", Decimal('0.5'))
    conflict_risk = Decimal('1') - input_data.get("conflict_risk", Decimal('0.2'))
    return cooperation * conflict_risk ** Decimal('2')

# Regimes (exact unity weights)
energy_regime = Regime("Energy Mastery", [FiniteElement("Fusion/Grid Potential", energy_element, "Renewables + fusion scaling")], [Decimal('1')])

tech_regime = Regime("Technological Advancement", 
                     [FiniteElement("AI/Compute Synergy", tech_element, "Exponential tech growth")],
                     [Decimal('1')])

society_regime = Regime("Societal Stability", 
                        [FiniteElement("Cohesion + Education", society_element, "Human capital factor")],
                        [Decimal('1')])

env_regime = Regime("Environmental Sustainability", 
                    [FiniteElement("Climate + Resource", environment_element, "Planetary limits")],
                    [Decimal('1')])

geo_regime = Regime("Geopolitical Coordination", 
                    [FiniteElement("Cooperation vs Risk", geopolitics_element, "Global alignment")],
                    [Decimal('1')])

# Top-level system (adjust weights for strategic bias if needed)
kardashev_system = UnitySumSystem("Kardashev Civilization Impact Analyzer v0.2",
                                 [energy_regime, tech_regime, society_regime, env_regime, geo_regime],
                                 [Decimal('0.3'), Decimal('0.3'), Decimal('0.15'), Decimal('0.15'), Decimal('0.1')])  # Exact sum=1

# Interactive CLI
if __name__ == "__main__":
    print("Kardashev Impact Analyzer v0.2 - Enter values (0.0-1.0 scale) or press Enter for defaults