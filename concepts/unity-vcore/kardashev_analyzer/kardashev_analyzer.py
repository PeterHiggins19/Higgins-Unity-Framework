import json
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
import numpy as np  # For potential numerical elements

@dataclass
class FiniteElement:
    name: str
    func: Callable[[Dict[str, Any]], float]  # Input dict → score/contribution (0-1 normalized or bounded)
    description: str

class Regime:
    def __init__(self, name: str, elements: List[FiniteElement], weights: List[float]):
        self.name = name
        self.elements = elements
        self.weights = np.array(weights)
        assert abs(sum(weights) - 1.0) < 1e-8, f"{name} weights must sum exactly to 1"

    def evaluate(self, input_data: Dict[str, Any]) -> float:
        contributions = [element.func(input_data) for element in self.elements]
        return float(np.dot(self.weights, contributions))

class UnitySumSystem:
    def __init__(self, name: str, regimes: List[Regime], regime_weights: List[float]):
        self.name = name
        self.regimes = regimes
        self.regime_weights = np.array(regime_weights)
        assert abs(sum(regime_weights) - 1.0) < 1e-8, "Top-level weights must sum exactly to 1"

    def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        regime_scores = {r.name: r.evaluate(input_data) for r in self.regimes}
        total_score = float(np.dot(self.regime_weights, [regime_scores[r.name] for r in self.regimes]))
        return {
            "total_impact_score": total_score,  # 0-1 Kardashev-aligned potential
            "regime_breakdown": regime_scores,
            "weighted_contributions": {r.name: self.regime_weights[i] * regime_scores[r.name] for i, r in enumerate(self.regimes)}
        }

# Example Kardashev Regimes (expandable)
def energy_element(input_data: Dict) -> float:
    tech_level = input_data.get("energy_tech", 0.0)  # e.g., fusion readiness 0-1
    investment = input_data.get("investment", 0.0)
    return min(tech_level + 0.3 * investment, 1.0)

def tech_element(input_data: Dict) -> float:
    return input_data.get("ai_advancement", 0.5)

def society_element(input_data: Dict) -> float:
    stability = input_data.get("social_cohesion", 0.8)
    return stability * 0.9

# Build prototype regimes
energy_regime = Regime("Energy Mastery", 
                       [FiniteElement("Fusion Potential", energy_element, "Fusion tech impact")],
                       [1.0])  # Single element for v0.1

tech_regime = Regime("Technological Advancement", 
                     [FiniteElement("AI/Computing", tech_element, "AI scaling")],
                     [1.0])

society_regime = Regime("Societal Stability", 
                        [FiniteElement("Cohesion Metrics", society_element, "Stability factor")],
                        [1.0])

# Top-level Kardashev Analyzer (equal weights initial)
kardashev_system = UnitySumSystem("Kardashev Impact Analyzer",
                                 [energy_regime, tech_regime, society_regime],
                                 [0.4, 0.4, 0.2])  # Sum=1 exactly

# Simple CLI Demo (replace with GUI later)
if __name__ == "__main__":
    sample_input = {
        "energy_tech": 0.7,
        "investment": 1.0,  # $B normalized
        "ai_advancement": 0.8,
        "social_cohesion": 0.9
    }
    result = kardashev_system.evaluate(sample_input)
    print(json.dumps(result, indent=2))