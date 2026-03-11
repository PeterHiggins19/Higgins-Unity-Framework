import decimal
from decimal import Decimal, getcontext
getcontext().prec = 28

class MinimalRegime:
    def __init__(self, name, weights):
        self.name = name
        self.weights = weights[:]
        total = sum(self.weights)
        if abs(total - Decimal('1')) > Decimal('1e-10'):
            raise ValueError("Unity violation")

    def evaluate(self, inputs):
        return sum(w * i for w, i in zip(self.weights, inputs))

    def hill_climb_step(self, inputs, step_size=Decimal('0.05')):
        current_score = self.evaluate(inputs)
        best_score = current_score
        best_weights = self.weights[:]
        for i in range(len(self.weights)):
            for delta in [step_size, -step_size]:
                new_weights = self.weights[:]
                new_weights[i] += delta
                total = sum(new_weights)
                new_weights = [w / total for w in new_weights]
                temp_score = sum(nw * inp for nw, inp in zip(new_weights, inputs))
                if temp_score > best_score:
                    best_score = temp_score
                    best_weights = new_weights
        if best_score > current_score + Decimal('0.001'):
            self.weights = best_weights
            return True, best_score
        return False, current_score

inputs = [Decimal('0.8'), Decimal('0.3'), Decimal('0.9'), Decimal('0.2')]
initial_weights = [Decimal('0.25')] * 4
system = MinimalRegime("Core", initial_weights)

history = []
score = system.evaluate(inputs)
history.append((0, [float(w) for w in system.weights], float(score)))

cycle = 0
improved = True
while improved and cycle < 20:
    cycle += 1
    improved, score = system.hill_climb_step(inputs)
    history.append((cycle, [float(w) for w in system.weights], float(score)))

print("Evolution:")
for c, w, s in history:
    print(f"Cycle {c}: Weights {w} | Score {s:.4f}")