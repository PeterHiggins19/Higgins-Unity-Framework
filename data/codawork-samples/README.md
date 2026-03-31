# CoDaWork Sample Datasets

CoDa-ready compositional data extracted from the HUF corpus.

## Contents

| File | Description |
|------|-------------|
| `ember_multisite_compositions.csv` | 3 countries, 9 fuel types, 2000-2025. Real EMBER proportions. |
| `ember_multisite_metadata.yaml` | Carrier definitions, zero handling, intended analyses. |

## Quick start

Each row is one country-year observation. The 9 fuel columns sum to 1.

```r
# R example
library(compositions)
d <- read.csv("ember_multisite_compositions.csv")
comp <- acomp(d[, 3:11])
plot(comp)
```

```python
# Python example
import pandas as pd
df = pd.read_csv("ember_multisite_compositions.csv")
# Rows sum to 1 — ready for simplex analysis
```

## Zero handling

Solar and wind start near zero in early years. Strict log-ratio transforms
require zero replacement. Raw proportions provided for transparency.

## Source

EMBER electricity data (CC BY 4.0). See `ember_multisite_metadata.yaml`
for full provenance.
