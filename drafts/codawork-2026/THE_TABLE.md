# The Table — What Not Utilizing Compositional Monitoring Leaves Behind

*For CoDaWork 2026, Coimbra. Not a sales pitch. An inventory.*

---

## The Observation

Every monitoring system on Earth that watches a whole made of parts is sitting on compositional data. Almost none of them monitor the composition directly. They monitor how much (MC-1), what kind (MC-2), and which direction (MC-3). The internal balance — the ratio-state — goes unwatched.

This is not a criticism of existing practice. It is a description of a structural gap. The mathematics for compositional analysis has existed since Aitchison (1982). The monitoring application has not followed.

EITT sharpens the point. If the geometric mean preserves Shannon entropy under temporal decimation — as the tested energy datasets suggest — then every system that aggregates compositional data over time using arithmetic means is not just missing the composition. It is actively discarding information that would have survived under the correct operation.

The d(CoDa)/dt chain sharpens it further. Three temporal layers exist for any compositional time series: perturbation velocity (the scalar speed of compositional change), the balance trajectory in ILR coordinates (the structural path), and the balance derivative dB/dt (the directed rate of structural change along each partition). In raw proportions, the zero-sum constraint (Σ dx_i/dt = 0) forces a relay — every gain financed by losses elsewhere. In ILR coordinates, the balance derivatives move independently, decomposing the relay into interpretable structural rates. None of this is being monitored. Not the speed. Not the path. Not the rate of structural handoff.

The information is in the data. It is not being read.

---

## The Inventory

What follows is not exhaustive. It is a survey of monitored domains where compositional structure exists, where standard practice does not monitor it, and where EITT's temporal stability property — if confirmed beyond energy — would mean the signal survives aggregation.

### Energy

National electricity grids are zero-sum compositional systems. Fuel shares must close to 100%. Every country, every regional market, every utility reports generation by fuel type. The standard monitoring watches total generation, peak demand, and price. The internal reorganization of fuel mix — concentration, hollowing, relay sequences between carriers — is compositionally visible years before headline indicators break.

Germany's structural concentration (p = 0.0016) was invisible in total generation figures. Japan's post-Fukushima relay (Nuclear → Gas → Coal → Renewables) followed infrastructure time constants that only composition could reveal. In both cases, magnitude said stable. Composition said otherwise.

Approximately 200 countries maintain energy generation statistics. Thousands of regional grids report fuel mix data. None of them, to our knowledge, run compositional drift detection as standard practice.

### Finance

Every index, every portfolio, every pension fund is a compositional system. Sector weights must sum to the total. Performance monitoring watches return, volatility, drawdown, and tracking error. The composition of the portfolio — which sectors are quietly cannibalizing which — is treated as a rebalancing input, not a monitoring observable.

When the S&P 500 reached 30% technology concentration, the total return said all-time high. The composition said single-sector dependency at a level not seen since the dot-com era. Portfolio theory has the tools. Portfolio monitoring does not use them compositionally.

The global asset management industry oversees roughly $120 trillion. The ratio-state of that capital — how it is distributed across sectors, geographies, and instruments — is the structural risk signal. It is reported in quarterly snapshots and monitored by magnitude.

### Ecology

Species abundance data is compositional by definition. The proportion of each species in a community must sum to one. Biodiversity monitoring watches species richness (count), total abundance, and presence/absence. Shannon-Wiener diversity — which IS Shannon entropy — is computed but not tracked compositionally across temporal resolutions.

EITT, if it holds for ecological compositions, would mean that temporal aggregation of biodiversity surveys using the geometric mean preserves the diversity index. Every long-term ecological monitoring program that aggregates annual surveys into decadal assessments using arithmetic means may be smoothing away the very signal it exists to detect.

There are 2,500 Ramsar wetland sites under international convention. Tens of thousands of ecological monitoring stations operate globally. The compositional dimension of their data — the balance of species, habitat types, functional groups — is collected but not monitored as a primary observable.

### Public Health

Disease burden statistics are compositional. The distribution of cases across disease categories, the allocation of hospital beds across departments, cause-of-death breakdowns — these are all ratios that must sum to a whole. Standard monitoring watches total cases, total mortality, total expenditure.

When one disease category quietly grows its share at the expense of others — when infectious disease spending crowds out chronic disease infrastructure, or when a new pathogen reshapes the case-type distribution — that is compositional drift. It is visible in the ratios before it is visible in the headlines.

The WHO monitors disease burden across 194 member states. National health systems track resource allocation by category. The compositional balance of these systems is reported but not monitored for structural drift.

### Agriculture

Crop mix is compositional. The proportion of arable land devoted to each crop must sum to the total. Food security monitoring watches total production, yield per hectare, and price. The internal restructuring of what is grown where — monoculture concentration, diversity loss, substitution patterns — is the structural vulnerability.

When a country's crop mix concentrates into one or two export commodities, that is compositional hollowing. It precedes the food security crisis by years. The FAO collects crop production data for over 200 countries. The compositional analysis of that data is available. The compositional monitoring is not standard practice.

### International Trade

Export and import portfolios are compositional. A country's trade mix by sector must sum to total trade. Standard monitoring watches trade balance, total volume, and bilateral flows. The internal composition — which sectors are growing their share, which are being displaced — is the structural signal.

The Dutch Disease pattern (resource concentration displacing manufacturing) is a compositional phenomenon. It is diagnosed retrospectively. Compositional monitoring could detect it prospectively. Every country's trade statistics contain this signal. It is not monitored compositionally.

### Demographics

Age distribution, workforce composition, urban-rural balance, ethnic and income distributions — all compositional. Census data is the largest compositional dataset most countries collect. It is analyzed for trends in individual categories. The ratio-state across categories — the structural balance of the population — is not monitored as a primary observable.

When a country's age distribution shifts from pyramid to column to inverted pyramid, the composition changes years before the dependency ratio crosses a policy threshold. The data exists. The compositional monitoring does not.

### Manufacturing and Quality

Product mix, defect type distribution, supply chain component ratios — all compositional. Quality management systems monitor total defect rate, individual category thresholds, and trend. The composition of defects — which failure modes are growing their share at the expense of others — tells you which process is degrading. It is the early warning that total defect rate monitors miss.

### Environmental Monitoring

Water chemistry, air quality indices, soil composition — all compositional at the measurement level. Environmental monitoring stations report individual pollutant levels against thresholds. The ratio-state across pollutants — the compositional fingerprint of the contamination source — is available in the data but not tracked as a monitoring signal.

### Network Infrastructure

Traffic composition by protocol, application, source, and destination is compositional. Network operations centres monitor total bandwidth, latency, and packet loss. The composition of traffic — which applications are consuming what share — predicts congestion patterns and capacity needs. It is reported in utilization dashboards. It is not monitored compositionally for structural drift.

---

## The Scale

This is not a list of domains where compositional monitoring might be useful. It is a list of domains where compositional data is already being collected, where the mathematical tools for compositional analysis already exist, and where the monitoring dimension is absent.

The gap is not data. The gap is not mathematics. The gap is application.

MC-1 (Magnitude), MC-2 (Identity), and MC-3 (Trend) cover three dimensions of every monitored system. MC-4 (Composition) covers the fourth. Three walls of a four-walled room have windows. The fourth does not.

EITT makes the gap more specific. If Shannon entropy is near-invariant under geometric-mean temporal decimation — as the tested energy datasets suggest, pending confirmation on other domains — then every system that aggregates compositional data over time has a choice. Aggregate with arithmetic means and lose the compositional signal. Aggregate with geometric means and keep it.

The d(CoDa)/dt chain makes the gap operational. The balance derivative dB/dt — the rate of structural change along each ILR partition — tells you not just that the composition is drifting, but which partitions are moving, how fast, and whether that rate is accelerating. The zero-sum constraint in raw proportions forces every gain to be financed by losses elsewhere. In ILR coordinates, those relay handoffs become independent, measurable rates. Every domain listed above has this relay structure in its data. None of them monitor it as a directed rate of structural change.

The information is there. It has always been there. The instrument to read it exists. It has existed since Aitchison. What does not exist, in standard practice, is the decision to look.

---

## What This Is Not

This is not a claim that compositional monitoring would have prevented any specific crisis, predicted any specific outcome, or improved any specific decision. We do not know that. Domain-by-domain validation is required, and negative results are as important as positive ones.

This is not a claim that EITT holds across all these domains. It has been tested on energy data only. Every domain listed above is an open question.

This is not a claim that existing monitoring is wrong. MC-1, MC-2, and MC-3 work. They have always worked. The claim is that they are incomplete — and that the missing dimension is now accessible.

---

## What This Is

An invitation. The compositional data is being collected. The mathematics is mature. The temporal stability property appears real in the tested domains and has a defined boundary. The monitoring application is ready to be tested.

The question is not whether the data contains compositional structure. It does. The question is whether anyone is going to read it.

We found the signal in energy. We mapped the boundary. We showed where it breaks. We cannot prove the invariance analytically.

The CoDa community built the mathematics. We are asking them to help us understand what it means — and to test whether the signal is there in their domains too.

---

*Peter Higgins — Rogue Wave Audio — Markham, Ontario*
*CoDaWork 2026, Coimbra*
*"The information is there. It has always been there."*
