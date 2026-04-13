# EITT: Entropy-Invariant Time Transformer

**Canonical name:** Entropy-Invariant Time Transformer
**NOT:** Ternary Transform, Temporal Transform, Time Transfer

Shannon entropy of compositional data is near-invariant under geometric-mean decimation across temporal resolutions. Arithmetic mean destroys 20-40% of entropy.

## Four Proofs

| Proof | Domain | Key Number |
|-------|--------|------------|
| 1 | European electricity prices | 0.18% variation, 341:1 compression |
| 2 | EMBER monthly generation (6 countries) | 1.02% mean deviation |
| 3 | NGFS scenarios (geometric vs arithmetic) | Geometric preserves; arithmetic destroys 20-40% |
| 4 | CheMixHub chemistry (500k data points) | 54-82% interior pass, 4 diagnostic lenses |

## Adversarial Testing

17 tests: 10 pass (real-world temporal data), 7 fail (6 synthetic + 1 borderline). Boundary condition: temporal autocorrelation required.

**Posture:** We found this empirically. We can't prove it. Can you?
