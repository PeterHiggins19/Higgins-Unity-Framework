# CoDaWork 2026 — Conference Concept Points

## Living document. Add points as they emerge. Keep it tight.

---

| # | Concept | HUF Perspective | CoDa Perspective | Bridge |
|---|---------|----------------|-------------------|--------|
| 1 | **The simplex is a monitoring instrument** | The unity constraint is the sensor — state IS output, estimation error is zero | The simplex is the sample space — compositions live here by definition | HUF operationalizes what CoDa formalizes |
| 2 | **Change = perturbation, not subtraction** | Gain adjustment — scale the ratio, renormalize | Perturbation ⊕ — the group operation on S^D | Same operation, discovered independently: electronics and geometry |
| 3 | **Log-ratios = decibels** | dB = 20·log₁₀(ratio). Standard in signal processing since the 1920s | CLR/ILR = ln(ratio). Standard in CoDa since Aitchison 1982 | Different log base, same insight: multiplicative relationships become additive |
| 4 | **Closure = common-mode noise** | When one element moves, phantom response appears in others. Differential measurement removes it | Spurious correlation from constant-sum constraint. Log-ratio transforms remove it | Both are artifacts of measuring parts of a whole. Both solved by ratios |
| 5 | **Did the environment or the element move?** | The core diagnostic question in every constrained physical system | The core purpose of log-ratio analysis — separate real change from closure artifact | This single question is why CoDa exists and why HUF needs CoDa |
| 6 | **Authorized vs unauthorized change** | Silent drift = perturbation with no governance record. The detection target | Not a CoDa concept — CoDa measures change but doesn't ask "who decided?" | HUF's unique contribution: governance distinction on the simplex |
| 7 | **Concentration / effective diversity** | K_eff = exp(Shannon entropy). How many carriers are "effectively present" | Aitchison norm of the composition. Active research (Egozcue poster at CoDaWork) | Open bridge — two measures of the same phenomenon. Collaboration opportunity |
| 8 | **The ternary diagram is universal** | Soil texture triangle (sand/silt/clay). Energy triangle (fossil/nuclear/renewable). Same S² | The 2-simplex — the most intuitive CoDa visualization. Every CoDa researcher's first tool | Peter plotted compositions in soil pits in the 1980s. The geometry was always there |
| 9 | **Balances = crossover networks** | Hierarchical frequency splits: low/high, then sub-splits within each band | Sequential binary partition into ILR coordinates: fossil/renewable, then coal/gas | Both are tree-structured decompositions of a whole into interpretable contrasts |
| 10 | **Trajectory on the simplex = control loop** | Real-time monitoring: each period adds a point, trajectory reveals drift | Compositional time series: sequence of points on S^D, underdeveloped in CoDa | CoDa has the space. HUF has the trajectory. Together: monitored compositional dynamics |
| 11 | **Fixed budget (closed loop) meets open geometry (open loop)** | Physics to math — start with constrained physical system, discover the geometry | Math to physics — start with abstract geometry, look for applications | Portugal is where closed loop meets open loop. Meeting in the middle |
| 12 | **Falsifiable claim structure** | Four defeat paths: prior art, metric, case, category. Invitation to break it | CoDa community has the expertise to attempt all four defeats | The posture of "please try to break this" is the strongest position in a room of mathematicians |
| 13 | **Fukushima on the simplex** | Massive undeclared perturbation — nuclear → 0, fossil absorbs. No governance decision preceded the compositional shock | Large Aitchison distance spike, regime boundary in distance matrix, trajectory discontinuity on S² | The single most powerful visual example. Every panel of the CoDa Explorer shows it differently |
| 14 | **BTL as experimental test bed** | Physical system with fixed energy budget, precision perturbation control, known ground truth | Controlled experiment on compositions with predicted vs observed perturbation response | Prospective validation — not retrospective observation. Answers "does it work?" not just "does it fit?" |
| 15 | **Zero handling as structural truth** | Germany nuclear = 0 after 2023. Not a measurement limit — genuine absence of the carrier | Structural zeros break log-ratios. No consensus solution for essential zeros | HUF flags zeros as governance events (a carrier was removed by decision). CoDa treats them as statistical problems. Both are right |
| 16 | **4,700 regimes** | HUF-Codex identifies 4,700+ governance regimes where compositional monitoring applies | CoDa applications span geosciences, biology, genetics, economics, ecology — but no unified monitoring protocol across all | The simplex is domain-independent. The monitoring protocol should be too |

---

| 17 | **Physics grounds math, math generalizes physics** | HUF was built from physical observation of constrained systems — the geometry was discovered empirically | CoDa was built from axioms — the geometry was proven mathematically | Both arrived at the same structure. Neither is superior. Physics without math can't generalize. Math without physics can't validate. The meeting is the point |

---

### Concepts 18–25: From Grok CoDa Deep Dive (S006)

| # | Concept | HUF Perspective | CoDa Perspective | Bridge |
|---|---------|----------------|-------------------|--------|
| 18 | **Aitchison distance = Euclidean distance in CLR space** | THD computed on ratio differences between all carrier pairs | d_A(x,y) = ‖clr(x) − clr(y)‖₂. The natural metric. Subcompositionally coherent, permutation invariant, scale invariant | TV sees absolute share movement. d_A sees ratio movement. Both detect Fukushima. d_A is geometrically correct. TV is operationally intuitive. Keep both side-by-side |
| 19 | **Open loop → closed loop (Breaker 16)** | HUF currently runs open-loop: observe, record, report. No actuator. The moment governance acts on HUF output, the loop closes | CoDa is inherently open-loop — it analyses, it doesn't govern | HUF's closed-loop capability is what makes it a monitoring framework, not just an analysis framework. Breaker 16 is the threshold. CoDa has no equivalent |
| 20 | **Four polarity-aligned roots** | a₀ (internal balance), a₁ (fleet alignment), a₂ (concentration resistance), a₃ (shape) → RMS aggregated into K_eff_fill | No direct equivalent — CoDa computes distances and coordinates but doesn't aggregate into a scalar health score | The roots are HUF's reduction of high-dimensional simplex state to an operational readout. Like reducing a full spectrum to a single THD+N number |
| 21 | **SBP design = domain knowledge encoded as geometry** | The partition tree is chosen once by the operator based on what contrasts matter: fossil vs renewable, coal vs gas, wind vs solar | SBP is the standard method for constructing ILR coordinates. Choice of partition determines what each balance measures | The operator decides what to monitor. The geometry ensures the measurement is rigorous. Domain knowledge enters through partition design, not through the math |
| 22 | **Compositional examples beyond energy** | Budget allocation, soil particles, election votes, dietary nutrients, corporate revenue, waste streams — all fixed-budget simplex systems | Geosciences, genetics, microbiome, ecology — CoDa's established domains | The 4,700 regimes include both lists. Every system where parts sum to a constrained total is a simplex. The monitoring protocol is the same for all of them |
| 23 | **TV and d_A agree on regime boundaries, differ on fine structure** | TV detects the big events: Fukushima spike, coal exit, nuclear phase-out. Simple, bounded [0,1], cheap to compute | d_A detects the same events plus fine-grained ratio changes invisible to TV. Unbounded, geometrically correct, closure-free | Not a competition — a dual-metric validation. When both agree, confidence is high. When they disagree, the disagreement itself is informative |
| 24 | **First contact = first empirical test of open-loop survival** | The packet survived inspection by a domain founder without requiring any closed-loop response. Pure observation held | Egozcue engaged with the mathematics, not metadata. The four comments were technical, not dismissive | Grok frames this as: "first empirical demonstration that open-loop HUF-GOV survives direct inspection by a domain founder." The posture worked |
| 25 | **PLL discipline as scientific hygiene** | Six rules: simplex carrier, simplex normalization, RMS aggregator p=2, every observation retained, no new constants, polarity alignment mandatory | CoDa has its own hygiene: always use log-ratios, always check subcompositional coherence, always handle zeros explicitly | Both are discipline frameworks that prevent the practitioner from introducing artifacts. HUF's PLL rules and CoDa's log-ratio rules serve the same purpose: keep it honest |

---

### Concept 26: The Opening Line

| # | Concept | HUF Perspective | CoDa Perspective | Bridge |
|---|---------|----------------|-------------------|--------|
| 26 | **A gateway to the physical world** | HUF operates compositional monitoring on real systems in real time — energy grids, solder waves, speaker arrays, governance regimes. The simplex isn't abstract. It's running | CoDa built the geometry, proved the theorems, defined the operations. Forty years of rigorous mathematics waiting for physical systems to adopt it | "We are here today to offer the CoDa community a gateway to the physical world." — Peter Higgins, CoDaWork 2026, Coimbra |

*Add new concepts as they emerge from collective reviews and conference preparation.*
