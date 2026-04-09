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
        if total != Decimal('1'):
            raise ValueError(f"{name} weights must sum exactly to 1 (got {total})")

    def evaluate(self, input_data: Dict[str, Decimal]) -> Decimal:
        contributions = [element.func(input_data) for element in self.elements]
        return sum(w * c for w, c in zip(self.weights, contributions))

class UnitySumSystem:
    def __init__(self, name: str, regimes: List[Regime], regime_weights: List[Decimal]):
        self.name = name
        self.regimes = regimes
        self.regime_weights = regime_weights
        total = sum(regime_weights)
        if total != Decimal('1'):
            raise ValueError(f"Top-level weights must sum exactly to 1 (got {total})")

    def evaluate(self, input_data: Dict[str, Decimal]) -> Dict[str, Any]:
        regime_scores = {r.name: r.evaluate(input_data) for r in self.regimes}
        total_score = sum(w * regime_scores[r.name] for w, r in zip(self.regime_weights, self.regimes))
        contributions = {r.name: self.regime_weights[i] * regime_scores[r.name] for i, r in enumerate(self.regimes)}
        tier = "High" if total_score >= Decimal('0.7') else "Medium" if total_score >= Decimal('0.4') else "Low"
        recommendation = {
            "High": "Strong Kardashev advancement potential — prioritize execution.",
            "Medium": "Moderate potential — consider with risk mitigation.",
            "Low": "Limited impact — deprioritize or redesign."
        }[tier]
        return {
            "total_impact_score": str(total_score),  # String for clean display
            "impact_tier": tier,
            "recommendation": recommendation,
            "regime_breakdown": {k: str(v) for k, v in regime_scores.items()},
            "regime_weights": {r.name: str(self.regime_weights[i]) for i, r in enumerate(self.regimes)},
            "weighted_contributions": {k: str(v) for k, v in contributions.items()}
        }

# Expanded Kardashev Elements (same as v0.2)
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

# Regimes (exact unity)
energy_regime = Regime("Energy Mastery", [FiniteElement("Fusion/Grid Potential", energy_element, "")], [Decimal('1')])
tech_regime = Regime("Technological Advancement", [FiniteElement("AI/Compute Synergy", tech_element, "")], [Decimal('1')])
society_regime = Regime("Societal Stability", [FiniteElement("Cohesion + Education", society_element, "")], [Decimal('1')])
env_regime = Regime("Environmental Sustainability", [FiniteElement("Climate + Resource", environment_element, "")], [Decimal('1')])
geo_regime = Regime("Geopolitical Coordination", [FiniteElement("Cooperation vs Risk", geopolitics_element, "")], [Decimal('1')])

# Top-level
kardashev_system = UnitySumSystem("Kardashev Civilization Impact Analyzer v0.2.1",
                                 [energy_regime, tech_regime, society_regime, env_regime, geo_regime],
                                 [Decimal('0.3'), Decimal('0.3'), Decimal('0.15'), Decimal('0.15'), Decimal('0.1')])

# Interactive CLI
if __name__ == "__main__":
    print("Kardashev Impact Analyzer v0.2.1 - Enter values (0.0-1.0 scale) or press Enter for defaults.")
    print("Blank input uses default value shown in [].\n")
    while True:
        try:
            input_data = {}
            prompts = [
                ("energy_tech", "Energy tech maturity (e.g., fusion readiness) [0.7]: "),
                ("investment", "Normalized investment level [1.0]: "),
                ("ai_advancement", "AI advancement level [0.8]: "),
                ("compute_scale", "Compute infrastructure scale [0.7]: "),
                ("social_cohesion", "Social cohesion index [0.9]: "),
                ("education_level", "Education/access level [0.8]: "),
                ("sustainability_index", "Sustainability practices [0.7]: "),
                ("climate_risk", "Climate disruption risk (0-1, higher=more risk) [0.2]: "),
                ("global_cooperation", "International cooperation level [0.6]: "),
                ("conflict_risk", "Geopolitical conflict risk [0.1]: ")
            ]
            for key, prompt in prompts:
                val = input(prompt).strip()
                input_data[key] = Decimal(val) if val else Decimal(prompt.split('[')[1].split(']')[0])
            
            result = kardashev_system.evaluate(input_data)
            print("\nResults:\n" + json.dumps(result, indent=2))
            
            if input("\nRun another analysis? (y/n): ").lower() != 'y':
                break
        except Exception as e:
            print(f"Error: {e}. Please enter valid numbers. Try again.\n")