# CoDaWork 2026 — Battle Card

## 10 Hardest Questions. Cleanest Answers.

*One page. Glance at it over coffee. Walk back in.*

---

### 1. "What is actually new here? The simplex is well-studied."

**Answer:** The simplex is yours. Nobody has built a monitoring protocol on it — one that tracks declared-versus-observed allocation at the carrier level with perturbation-based drift detection. The math is not new. The application is. I've structured four specific ways to defeat that claim and I'm asking this room to try.

---

### 2. "Why aren't you using log-ratio transforms?"

**Answer:** I haven't yet. The current implementation operates on raw proportions because monitoring applications need interpretable absolute magnitudes. Expressing the same trajectories in ILR coordinates and comparing drift detection sensitivity is exactly the collaboration I came here looking for. I'd welcome guidance on whether ALR or ILR is more appropriate for time-series monitoring.

---

### 3. "How do you handle zeros?"

**Answer:** The structural zeros in energy data — a country that has zero nuclear capacity — represent genuine absence, not measurement below detection. I flag them explicitly in the metadata rather than imputing. For rounded zeros near detection limits, I haven't applied multiplicative replacement or the methods in zCompositions. That's a gap I've disclosed and I'd value this community's advice on best practice.

---

### 4. "What is your null model? Where does the p-value come from?"

**Answer:** The p=0.0016 comes from a Pettitt test on a sliding-window statistic. No formal compositional null model — no Dirichlet, no permutation envelope, no bootstrap on the simplex — is specified. I flagged this as an open gap in the abstract. Specifying a principled null model for compositional time series is one of the things I most want help with.

---

### 5. "Is this subcompositionally coherent?"

**Answer:** I haven't tested that formally. If I monitor nine carriers but someone analyzes only the three fossil fuels, do my drift results hold? That's a question I can answer empirically with the data I have, and I'd appreciate hearing from this community what the expected behaviour should be under Aitchison geometry when a sub-composition is extracted.

---

### 6. "Isn't this just existing CoDa methods applied to energy data? What does your framework add?"

**Answer:** If it is, that's a valid defeat of my claim and I'll accept it. Show me the existing compositional monitoring protocol that does carrier-level drift detection with perturbation measurement, and I'll withdraw the novelty claim. What I believe I add is the monitoring architecture itself — the distinction between observation and governance, the threshold where passive tracking becomes active response, and cross-domain portability from energy to any compositional system.

---

### 7. "Why Aitchison distance and not some other metric on the simplex?"

**Answer:** I started with total variation distance, which comes from information theory. Aitchison distance is the metric native to the simplex geometry, and computing it on the same data is the natural next step. In the EMBER data I've processed both side by side — they agree on regime boundaries and differ on fine structure. I'm retaining both until I understand why they diverge, and I'd welcome insight from people who've worked with Aitchison distance longer than I have.

---

### 8. "How is this different from monitoring Dirichlet-distributed data?"

**Answer:** The Dirichlet is a parametric model on the simplex. My approach is model-free — it doesn't assume any distribution. Whether model-free detection or parametric Dirichlet monitoring performs better is an empirical question. My data is public and I'd be glad to see someone run a Dirichlet-based comparison.

---

### 9. "You're an independent researcher with no academic affiliation. Why should we take this seriously?"

**Answer:** I've operated physical compositional systems for 40 years — wave solder, audio signal chains, energy monitoring. The work is public, the data is public, the code is public, and the claim has four explicit defeat paths. Judge the work, not the letterhead. I'm here because Professor Egozcue invited me to submit after reviewing the packet.

---

### 10. "Did AI write this?"

**Answer:** I developed this framework with AI assistance — Claude, ChatGPT, Grok, Gemini, Copilot, and DeepSeek as research tools. The physical insight, the 40 years of operational experience, and the monitoring architecture are mine. The AIs helped me find the right vocabulary, check my mathematics, and prepare for exactly this question. I disclosed this because honest science requires it.

---

## Emergency Fallback

If any question goes somewhere you can't follow:

> "The geometry is yours. The monitoring protocol is mine. I'm here to see if they fit together."

---

## The Posture

You are not selling. You are not defending. You are presenting a falsifiable claim and asking the best people in the world to test it. Every "I don't know" followed by "here's how I'd find out" earns more respect than a confident wrong answer.

Short answers. Point at the data. Say thank you.
