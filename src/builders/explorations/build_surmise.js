const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak } = require('./node_modules/docx/dist/index.cjs');
const fs = require('fs');

// ── Helpers ──
const FONT = "Arial";
const W_FULL = 9360; // US Letter - 1" margins

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, font: FONT, size: 32, bold: true })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, font: FONT, size: 28, bold: true })] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 220, after: 120 },
    children: [new TextRun({ text, font: FONT, size: 24, bold: true })] });
}
function p(text, opts = {}) {
  const runs = [];
  // Support bold segments with ** markers
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const part of parts) {
    if (part.startsWith('**') && part.endsWith('**')) {
      runs.push(new TextRun({ text: part.slice(2, -2), font: FONT, size: 22, bold: true, ...opts }));
    } else {
      runs.push(new TextRun({ text: part, font: FONT, size: 22, ...opts }));
    }
  }
  return new Paragraph({ spacing: { after: 160 }, children: runs });
}
function pItalic(text) {
  return new Paragraph({ spacing: { after: 160 },
    children: [new TextRun({ text, font: FONT, size: 22, italics: true })] });
}
function code(text) {
  return new Paragraph({ spacing: { after: 80 },
    indent: { left: 720 },
    children: [new TextRun({ text, font: "Courier New", size: 20 })] });
}

const numbering = {
  config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets2", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets3", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets4", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets5", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets6", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets7", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets8", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bullets9", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bulletsA", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "bulletsB", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]
};

function bullet(text, ref = "bullets") {
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const part of parts) {
    if (part.startsWith('**') && part.endsWith('**')) {
      runs.push(new TextRun({ text: part.slice(2, -2), font: FONT, size: 22, bold: true }));
    } else {
      runs.push(new TextRun({ text: part, font: FONT, size: 22 }));
    }
  }
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: runs });
}

function num(text, ref = "numbers") {
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const part of parts) {
    if (part.startsWith('**') && part.endsWith('**')) {
      runs.push(new TextRun({ text: part.slice(2, -2), font: FONT, size: 22, bold: true }));
    } else {
      runs.push(new TextRun({ text: part, font: FONT, size: 22 }));
    }
  }
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: runs });
}

// ── Content ──
const children = [];

// Title
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [new TextRun({ text: "DADC-DADI-ADAC Operational Surmise", font: FONT, size: 40, bold: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [new TextRun({ text: "BTL Jupyter Lab Experiments", font: FONT, size: 28 })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [new TextRun({ text: "Detailed Walkthrough, Concept Parse, and Gap Analysis", font: FONT, size: 24, italics: true })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: "March 2026 | Session 6+ | Peter Higgins & Claude", font: FONT, size: 22 })] }));

// ═══════════════════════════════════════════════════════════════
// SECTION 1: WHAT THE NOTEBOOK IS
// ═══════════════════════════════════════════════════════════════
children.push(h1("1. What the Notebook Is"));

children.push(p("The BTL DADC-DADI-ADAC Tuning Loop (v1.1, \"Lazy Human\" quickstart, FIXED2) is a companion tool and run logger for the JAES manuscript on Dimension-Apportioned Diffraction Correction (DADC) and Dimension-Apportioned Diffraction Inference (DADI). It is built in Jupyter with ipywidgets, designed to be operated by a single human with a measurement mic, a DSP processor, and a loudspeaker cabinet in a room."));

children.push(p("The notebook explicitly states that its shelf response model is for **fitting and visualization only**, not for diffraction simulation. This is a critical conceptual boundary: the logistic and RBJ shelf curves are proxies for what a real DSP low-shelf filter does, used to infer apparent room dimensions from measured transfer functions. The physics of diffraction is in the room and the cabinet; the notebook maps observations onto a parametric model so the human can close the loop."));

// ═══════════════════════════════════════════════════════════════
// SECTION 2: THE NINE-STEP PROTOCOL
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("2. The Nine-Step Protocol (Cell 1)"));

children.push(p("The notebook prescribes a human-proof workflow in five phases comprising nine discrete steps. Each step has a clear input, action, and output. The protocol is designed so that a tired or distracted operator cannot accidentally corrupt the measurement chain."));

children.push(h2("Phase 1: Start / Reset (Step 1)"));
children.push(p("Run the Setup cells from the top. Set Mode to Simple. Click Start/Reset Run. This creates a fresh manifest.json and iteration_log.csv in a timestamped run directory. The ExperimentState dataclass is initialized with empty containers for transfer functions, iteration history, mic configurations, and position data. Every subsequent action writes into this state object, producing a complete audit trail."));

children.push(p("**Concept: Immutable manifest.** The run directory, once created, serves as the North Star anchor. Every iteration appends to the log; nothing is overwritten. This is the acoustic equivalent of HUF's governance ledger."));

children.push(h2("Phase 2: Calibration Capture (Steps 2-3, Optional but Recommended)"));
children.push(p("Set Capture mode to Calibration capture (co-located). Place the mic cluster co-located (within a few centimeters). Capture L/R for the M23 reference mic plus at least one auxiliary mic. Load at least two mics by repeating Load L/R per mic."));

children.push(p("Click Auto-detect correction sign. The notebook computes a co-located disagreement metric and selects the sign (positive or negative) that minimizes the disagreement between mics. This is applied to all future measurement captures."));

children.push(p("**Concept: Auto-sign detection.** The function autosign_metric_for_position() computes the RMS disagreement between mics at a co-located position, trying both +1 and -1 correction polarity. It picks the sign that makes the corrected curves agree best. This eliminates a common human error (applying mic correction with wrong polarity) that would silently corrupt every subsequent measurement."));

children.push(p("**Concept: M23 correction curve.** The notebook bundles 62 calibration points for the Earthworks M23 mic, spanning 20 Hz to 20 kHz. These are interpolated in log-frequency space. The correction is additive in dB, applied to the raw magnitude trace. If you skip calibration, you can set the correction sign manually or leave corrections off entirely."));

children.push(h2("Phase 3: Baseline Capture, Arm 0 (Steps 4-5)"));
children.push(p("Switch Capture to Measurement (P1-P3). With no DADC shelves enabled in the DSP (this is Arm 0, the baseline), capture transfer functions at three measurement positions P1, P2, and P3. For each position: select the position in the UI, load the Left TF, load the Right TF, and confirm it is loaded as a measurement."));

children.push(p("The transfer functions are parsed by parse_tf_text(), which accepts 2-column (frequency, magnitude), 3-column (frequency, magnitude, coherence), or 4-column (frequency, magnitude, phase, coherence) formats. Frequencies must be strictly increasing after sorting. Coherence data, when present, becomes the weighting function for all subsequent fits."));

children.push(p("**Concept: Multi-position spatial sampling.** Three positions are the minimum for spatial averaging. The notebook enforces this by default (require_all_pos = True, requiring 3 complete positions before iteration can proceed). Each position captures the room's influence on the loudspeaker-to-mic path from a different angle, reducing the chance that a single room mode dominates the correction."));

children.push(p("**Concept: L/R symmetry as a diagnostic.** The two-channel architecture (Left and Right) is not just stereo convenience. The mismatch between L and R at the same position reveals asymmetric room coupling, cabinet asymmetry, or measurement error. This becomes a hard gate in the ADAC acceptance logic."));

children.push(h2("Phase 4: One-Shot DADC, Arm 2 (Step 6)"));
children.push(p("Click Compute DADC shelves. The notebook calls dadc_shelves(H, W, D, beta) with the physical cabinet dimensions. This is the founding computation, the one-shot allocation that is the acoustic origin of HUF's proportional governance."));

children.push(p("The core math:"));
children.push(code("dims = np.array([H, W, D], float)"));
children.push(code("w = dims ** beta"));
children.push(code("s = w / w.sum()          # THIS IS \u03A3\u03C1\u1D62 = 1"));
children.push(code("gains = G_TOTAL_DB * s    # proportional allocation of 6.02 dB"));
children.push(code("fcs = K_F / dims          # corner frequencies from geometry"));

children.push(p("**G_TOTAL_DB = 20 * log10(2) = 6.0206 dB.** This is the diffraction gain of a rectangular baffle: the total low-frequency boost that any box-shaped loudspeaker cabinet produces as wavelengths become large relative to its dimensions. It is a physical constant of the geometry, not a tuning parameter."));

children.push(p("**K_F = 115.0 Hz\u00B7m.** This is the product of frequency and dimension at which the diffraction transition occurs. For a dimension d, the corner frequency is Fc = 115 / d. For the BTL cabinet [H=0.800, W=0.368, D=0.330], this yields Fc_H = 143.8 Hz, Fc_W = 312.5 Hz, Fc_D = 348.5 Hz."));

children.push(p("**beta = 1.0 (default).** The exponent on dimensions. At beta = 1, shares are purely proportional to physical size: the tallest dimension gets the largest share. At beta > 1, large dimensions are weighted more heavily; at beta < 1, shares are compressed toward equality. Beta is the only free parameter in the one-shot DADC."));

children.push(p("**Concept: Closure by construction.** Because s = w / w.sum(), the shares always sum to exactly 1.0. The gains always sum to exactly G_TOTAL_DB. This is the unity-sum constraint, identical to HUF's \u03A3\u03C1\u1D62 = 1. It is not imposed after the fact; it is built into the division. You cannot break it."));

children.push(p("After computing, the notebook displays a DSP table (axis, gain_dB, Fc_Hz, BW_oct) and a DSP copy block formatted for direct entry into a Lake or Lab.gruppen processor. It also plots the predicted composite correction curve with a dashed line at 6.02 dB."));

children.push(p("Apply these shelves to the DSP. Re-capture P1-P3 with the same mic(s) and settings. This is the before/after comparison: Arm 0 (no shelves) vs Arm 2 (DADC shelves applied)."));

children.push(p("**Concept: Driver-aware variant.** The notebook also implements dadc_driver_aware(), which adjusts corner frequencies using harmonic effective dimensions when the driver is not centered on the baffle. The harmonic effective dimension is H_eff = 4 * d_top * d_bottom / (d_top + d_bottom), and similarly for width. This can operate in Fc-only mode (gains from physical dims, Fc from effective dims) or Fc+gain mode (both from effective dims). The Fc-only mode is safer because it preserves the gain allocation from actual cabinet geometry while acknowledging that the driver position shifts the frequency at which each transition occurs."));

children.push(h2("Phase 5: DADI + ADAC Iteration, Loop A (Steps 7-9)"));
children.push(p("Click Run Shared Iteration. This is the heart of the notebook: the DADI inference loop with ADAC governance."));

// ═══════════════════════════════════════════════════════════════
// SECTION 3: THE DADI ENGINE IN DETAIL
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("3. The DADI Engine in Detail (Cell 8, run_shared_iteration)"));

children.push(p("This function is 250 lines of carefully structured inference. Here is what happens, step by step."));

children.push(h2("3.1 Validation and Setup"));
children.push(bullet("**Mic compliance check**: validate_mic_compliance() enforces that at least one Reference mic is configured and that correction curves are loaded for mics that claim to have them.", "bullets2"));
children.push(bullet("**Position initialization**: If positions have not been initialized from the UI, init_positions_from_widgets() runs. Mic config is synced from the widget state.", "bullets2"));
children.push(bullet("**Position completeness**: For each required position (P1-P3), the code checks that both L and R transfer functions are loaded for all required mics. If strict_all mode (Precision all-mics), every mic must have data at every position. If env probes mode (the default), only the reference mic is required.", "bullets2"));
children.push(bullet("**Minimum 3 positions enforced**: If require_all_pos is True and fewer than 3 positions are complete, the iteration aborts with a clear diagnostic.", "bullets2"));

children.push(h2("3.2 Fitting Grid and Bounds"));
children.push(p("A logarithmic frequency grid is constructed: 260 points from fit_low to fit_high (default range typically 80-8000 Hz). The bounds for the optimizer are derived from the physical dimensions with a fractional margin (default bound = 0.25, meaning each apparent dimension can vary by \u00B125% from the physical measurement). This keeps the optimizer from drifting into physically impossible territory."));

children.push(h2("3.3 Residual Construction (Multi-Position, Multi-Mic)"));
children.push(p("For each (position, mic) pair, the code:"));

children.push(num("Interpolates the L and R magnitude traces onto the fit grid.", "numbers2"));
children.push(num("Computes residuals RL = 0 - magL and RR = 0 - magR. The target is flat (0 dB). The residual is the deviation from flat that the shelves need to explain.", "numbers2"));
children.push(num("Constructs coherence-weighted masks: wL and wR. Where coherence is below coh_gate, the weight drops to zero. This means that frequency bins where the measurement is unreliable (low coherence, typically due to room modes or noise floor) are excluded from the fit.", "numbers2"));
children.push(num("Computes per-mic RMS for diagnostic purposes. If multiple mics are present at a position, the spread (max - min RMS) is recorded as a spatial consistency diagnostic.", "numbers2"));
children.push(num("Computes L/R mismatch from the reference mic only, using a midband window (default 200-2000 Hz). This is computed per-position and averaged.", "numbers2"));

children.push(h2("3.4 The Objective Function"));
children.push(p("The optimizer minimizes a combined objective:"));

children.push(code("def obj(p):"));
children.push(code("    df = dadc_shelves(p[0], p[1], p[2], beta=beta)"));
children.push(code("    M = composite_model(f_grid, df, bw_oct=bw_oct)"));
children.push(code("    tot = sum over all (pos, mic): wL*(RL-M)^2 + wR*(RR-M)^2"));
children.push(code("    reg = 0.02 * sum of ((p_i - midpoint) / half_span)^2"));
children.push(code("    return tot + reg * wsum"));

children.push(p("**Concept: The model M is shared across all positions and both channels.** This is the key insight. The DADI does not fit a separate correction per position or per channel. It fits one set of apparent dimensions (H*, W*, D*) that best explains the residuals across all positions and both channels simultaneously. This is why it is called \"shared iteration.\""));

children.push(p("**Concept: Mild regularization toward physical midpoints.** The 0.02 coefficient on the regularizer is deliberately weak. It nudges the optimizer toward the center of the search bounds without preventing it from finding the true minimum. The purpose is stability, not bias: without it, the optimizer can oscillate between iterations when the data are noisy."));

children.push(p("**Concept: The optimizer is L-BFGS-B** (when scipy is available), a bounded quasi-Newton method. This is the right choice: the problem is smooth, low-dimensional (3 parameters), and bounded. If scipy is not available, a fallback grid search over a 5\u00D75\u00D75 grid is used, which is crude but functional."));

children.push(h2("3.5 The Damped Update"));
children.push(p("After the optimizer returns p_fit, the candidate dimensions are computed as a damped blend:"));

children.push(code("p_candidate = (1 - alpha) * p_k + alpha * p_fit"));

children.push(p("where alpha is the damping factor (default typically 0.5). This is the same exponential moving average used in control systems. At alpha = 1, the full optimizer suggestion is taken. At alpha = 0, nothing changes. The damping prevents overcorrection: the room response changes when you adjust the DSP, so the next measurement will be different. Taking the full step would chase a moving target."));

children.push(p("**Concept: This is the governance damper.** In HUF terms, alpha controls the rate of portfolio rebalancing. Too fast (alpha near 1) and you get oscillation. Too slow (alpha near 0) and convergence takes forever. The default is a compromise that converges in 3-5 iterations for most rooms."));

children.push(h2("3.6 Residual Decomposition"));
children.push(p("After fitting, the code decomposes residuals into common-mode and differential components:"));

children.push(code("Ecm = 0.5 * (eL + eR)    # what both channels share"));
children.push(code("Ed  = 0.5 * (eL - eR)    # what differs between channels"));

children.push(p("These are aggregated across positions and mics using coherence weights. The common-mode residual Ecm represents room effects that affect both channels equally: standing waves, boundary reflections, general room gain. The differential residual Ed represents asymmetries: cabinet asymmetry, room asymmetry, measurement positioning error."));

children.push(p("**Concept: Ecm is what Loop A can fix. Ed is what Loop B (per-channel refinement) targets.** The shared DADI iteration can only reduce Ecm because it applies the same shelves to both channels. Once Ecm is converged, the differential residual becomes the frontier."));

children.push(h2("3.7 The ADAC Accept/Reject Gate"));
children.push(p("The notebook computes an improvement metric and an acceptance recommendation:"));

children.push(code("improvement = rms_prev - rms_now"));
children.push(code("accept_suggest = (improvement >= tau_accept)"));
children.push(code("                 AND (lr_worsen <= lr_worsen_max)"));

children.push(p("**tau_accept** (default typically 0.05 dB) is the minimum improvement required to accept a candidate. If the RMS reduction is less than this, the candidate is not worth the DSP change and the associated re-measurement effort."));

children.push(p("**lr_worsen** checks that the L/R mismatch has not gotten worse. Even if the overall RMS improved, if the mismatch between channels increased, the candidate is flagged for rejection. This prevents a situation where the optimizer reduces the average error by making one channel better at the expense of the other."));

children.push(p("The human operator sees the recommendation and can Accept, Reject, or Revert to last-known-good (LKG). This is manual ADAC governance."));

children.push(p("**Concept: Accept updates p_k and LKG.** On acceptance, p_k becomes p_candidate, and LKG is updated to the new p_k. The iteration counter advances. The DSP copy block is printed so the operator can program the new shelves."));

children.push(p("**Concept: Reject preserves p_k.** On rejection, p_k does not change. The iteration counter still advances (the attempt is logged). The operator re-measures with the existing shelves."));

children.push(p("**Concept: Revert restores LKG.** If things go wrong (e.g., measurement error, environmental change), the operator can revert to the last accepted state. There is also a snapshot/branch restore system for reverting to any previously accepted iteration."));

// ═══════════════════════════════════════════════════════════════
// SECTION 4: PER-CHANNEL REFINEMENT (LOOP B)
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("4. Per-Channel Refinement: Loop B"));

children.push(p("Loop B is only enabled after the shared iteration (Loop A) has converged and the operator clicks Lock Shared. Locking captures the current aggregated decomposition (Ecm_ref, Ed_ref) as a reference and freezes p_shared."));

children.push(p("The per-channel optimizer (run_per_channel_refine) fits separate apparent dimensions pL and pR for the left and right channels. The objective function has three terms:"));

children.push(num("**Differential reduction**: Minimize wcm * Ed\u00B2 (the primary goal).", "numbers3"));
children.push(num("**Common-mode drift penalty**: lambda_cm = 8.0 times wcm * (Ecm - Ecm_ref)\u00B2. This heavily penalizes any change to the common-mode residual. Loop B must not undo what Loop A achieved.", "numbers3"));
children.push(num("**Deviation penalty**: lambda_dev = 0.6 times the squared fractional deviation of pL and pR from p_shared. This keeps the per-channel dimensions close to the shared solution.", "numbers3"));

children.push(p("The acceptance gate for Loop B is three-part:"));

children.push(bullet("Differential improvement must exceed pc_tau_diff.", "bullets3"));
children.push(bullet("Common-mode drift must not exceed pc_cm_drift_max.", "bullets3"));
children.push(bullet("Predicted L/R delta (mean |ML - MR|) must not exceed pc_pred_lr_max.", "bullets3"));

children.push(p("**Concept: Fc-only mode (safe).** By default, per-channel refinement operates in Fc-only mode: it adjusts corner frequencies using the per-channel apparent dimensions but keeps the gain allocation from p_shared. This means the total gain budget (6.02 dB) is not redistributed per-channel; only the frequency placement changes. This is the conservative approach. Full per-channel DADC mode redistributes gains as well, but risks divergence."));

children.push(p("**Concept: The lambda_cm = 8.0 hard gate.** This is not arbitrary. It is roughly one order of magnitude higher than the differential weight (1.0). This means the optimizer will sacrifice differential improvement before it allows common-mode drift. The shared solution is the anchor; per-channel refinement is cosmetic adjustment."));

children.push(p("**Concept: Intersected bounds.** The search bounds for pL and pR are the intersection of two constraints: the per-channel fractional bound around p_shared (pc_bound, tighter) and the physical bound around the cabinet dimensions (bound, wider). This double constraint prevents the per-channel fit from straying outside physically plausible territory even if the channel-specific data suggests it."));

// ═══════════════════════════════════════════════════════════════
// SECTION 5: CONSTANTS AND THEIR ORIGINS
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("5. Constants and Their Origins"));

children.push(h2("5.1 G_TOTAL_DB = 6.0206 dB"));
children.push(p("Defined as 20 * log10(2). This is the theoretical diffraction gain of a rectangular baffle in the transition from 4\u03C0 radiation (omnidirectional, wavelength >> cabinet) to 2\u03C0 radiation (half-space, wavelength << cabinet). Every rectangular loudspeaker cabinet exhibits this gain. It is not a design choice; it is physics."));

children.push(h2("5.2 K_F = 115.0 Hz\u00B7m"));
children.push(p("The frequency-dimension product at the diffraction corner. For a baffle dimension d meters, the corner frequency is Fc = 115 / d Hz. This constant emerges from the relationship between wavelength and baffle size at which the diffraction transition is half-complete. The value 115 is empirical, refined from measurement campaigns. It is consistent with Olson's classical diffraction work and with modern FEM/BEM simulations."));

children.push(h2("5.3 BW_OCT_DEFAULT = 5.50 octaves"));
children.push(p("The default bandwidth of the logistic shelf model. This controls how gradually the shelf transitions from full boost to zero boost. At 5.50 octaves, the transition is broad and smooth, matching the gradual nature of real diffraction. The logistic steepness parameter k = 4.394 / bw_oct = 0.799 at the default bandwidth."));

children.push(p("**Concept: Q_fixed.** The Q of the equivalent parametric filter, derivable from BW_oct, is approximately Q = 1 / (2 * sinh(ln(2)/2 * BW_oct)) \u2248 0.304. This extremely low Q confirms that the shelves are broadband corrections, not narrow-band EQ. They reshape the entire low-frequency response contour, not individual modes."));

children.push(h2("5.4 The M23 Correction Curve (62 Points)"));
children.push(p("A bundled calibration dataset for the Earthworks M23 measurement microphone. The curve spans 20 Hz to 20 kHz with irregular spacing (denser in the high-frequency rolloff region). It is interpolated in log-frequency space using numpy.interp. The correction is purely additive (dB), applied after raw magnitude extraction."));

children.push(h2("5.5 Fit Grid: 260 Points, Logarithmic"));
children.push(p("The fitting is performed on a logarithmic frequency grid of 260 points. This is sufficient for the 3-parameter model (the shelf transitions are inherently smooth) while being fast enough for interactive iteration. The grid spacing is uniform in log-frequency, which gives equal weight per octave."));

// ═══════════════════════════════════════════════════════════════
// SECTION 6: THE TWO SHELF MODELS
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("6. The Two Shelf Models"));

children.push(h2("6.1 Logistic (Fast, Used for Fitting)"));
children.push(p("shelf_logistic(f, Fc, G_db, bw_oct) implements a smooth sigmoid transition in log-frequency space. The shelf value at frequency f is:"));
children.push(code("x = log2(f / Fc)"));
children.push(code("s = 1 / (1 + exp(k * x))"));
children.push(code("shelf = G_db * s"));
children.push(p("where k = 4.394 / bw_oct. Below Fc, the shelf is near full gain. Above Fc, it tapers to zero. The composite model sums three such shelves (H, W, D) to produce the total predicted correction."));

children.push(p("**Concept: The logistic is not a filter model.** It does not correspond to any realizable analog or digital filter. It is a smooth, differentiable approximation to the diffraction transition shape. Its virtue is speed and mathematical tractability for the optimizer."));

children.push(h2("6.2 RBJ Low-Shelf (Visualization Only)"));
children.push(p("shelf_rbj_db() implements the Robert Bristow-Johnson (RBJ) low-shelf biquad magnitude response. This is the actual filter topology that the DSP processor uses. It is computed from the standard biquad coefficients with a configurable slope parameter S (default 1.0) at a sample rate of 48 kHz."));

children.push(p("The RBJ model is never used for fitting because its frequency-dependent behavior near Nyquist and its slope characteristics make the optimization surface more complex. It is offered as a visualization option so the operator can see what the DSP filter actually does, as opposed to what the logistic proxy predicts. The two should agree closely in the passband."));

// ═══════════════════════════════════════════════════════════════
// SECTION 7: STATE MANAGEMENT AND AUDIT TRAIL
// ═══════════════════════════════════════════════════════════════
children.push(h1("7. State Management and Audit Trail"));

children.push(p("The ExperimentState dataclass wraps a dictionary with attribute-style access. It holds:"));

children.push(bullet("**p_k**: Current apparent dimensions [H*, W*, D*] (the portfolio).", "bullets4"));
children.push(bullet("**p_candidate**: The latest proposed update (not yet accepted/rejected).", "bullets4"));
children.push(bullet("**last_good**: The last accepted p_k (the revert target).", "bullets4"));
children.push(bullet("**rms_prev, lr_prev**: Previous-iteration metrics for computing improvement.", "bullets4"));
children.push(bullet("**tf_by_pos**: Nested dict of transfer functions indexed by position and mic.", "bullets4"));
children.push(bullet("**history**: List of iteration records, each containing p_k, p_fit, RMS, L/R mismatch, accepted flag, timestamp.", "bullets4"));
children.push(bullet("**run_dir**: Path to the timestamped run directory.", "bullets4"));
children.push(bullet("**shared_locked, shared_ref**: Lock state for Loop A and the reference decomposition.", "bullets4"));
children.push(bullet("**fit_last, pc_fit_last**: Latest fit results for shared and per-channel iterations.", "bullets4"));

children.push(p("Every accept and reject writes an iteration record to history and persists it as iteration_log.csv. The manifest.json is updated on export with the current p_k, iteration count, and timestamp. The run directory also stores branch/snapshot data for non-linear exploration."));

children.push(p("**Concept: The notebook is a governance ledger.** Every measurement, every fit, every accept/reject decision is recorded with a timestamp. The human cannot lose their place. If the room changes (door opens, temperature shifts), the operator can revert to any prior state and resume. This is the run manifest that Cell 9 describes as an anti-drift mechanism."));

// ═══════════════════════════════════════════════════════════════
// SECTION 8: MULTI-MIC ARCHITECTURE
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("8. Multi-Mic Architecture"));

children.push(p("The notebook supports 1 reference mic plus up to 3 auxiliary mics. Two operating modes are offered:"));

children.push(h3("Env Probes Mode (Default)"));
children.push(p("Loop A uses only the reference mic for fitting. Auxiliary mics provide diagnostics: the spread between mics at each position indicates environmental variation (reflections, standing waves, turbulence). This is the safe mode because the fit is driven by a single, known mic with a characterized correction curve."));

children.push(h3("Precision All-Mics Mode"));
children.push(p("Loop A uses all mics. This requires certified correction curves for every mic. The objective function aggregates residuals across all mics, giving a more spatially robust fit at the cost of requiring more careful setup."));

children.push(p("**Concept: Mic compliance is a hard gate.** validate_mic_compliance() checks that every mic claimed as active has a name, a role (Reference or Auxiliary), and an appropriate correction curve. If compliance fails, iteration cannot proceed. This prevents garbage-in-garbage-out scenarios where an uncorrected aux mic corrupts the fit."));

children.push(p("**Concept: L/R mismatch is always from the reference mic.** Even in all-mics mode, the L/R symmetry diagnostic uses only the reference mic. This ensures the symmetry metric is consistent across iterations regardless of which auxiliary mics are present."));

// ═══════════════════════════════════════════════════════════════
// SECTION 9: STOP CONDITIONS AND CONVERGENCE
// ═══════════════════════════════════════════════════════════════
children.push(h1("9. Stop Conditions and Convergence"));

children.push(p("The notebook prescribes stopping when:"));

children.push(bullet("Improvement falls below tau_accept (the shared iteration is no longer making meaningful progress).", "bullets5"));
children.push(bullet("The L/R mismatch worsening gate triggers (the optimizer is fighting room asymmetry rather than improving the shared correction).", "bullets5"));
children.push(bullet("The position-to-position RMS spread exceeds 0.35 dB, indicating that the room itself is the limiting factor and additional DSP adjustment will not help without better spatial sampling.", "bullets5"));

children.push(p("Convergence typically occurs in 3-5 iterations for a well-behaved room. Each iteration requires: adjust DSP, re-measure all positions, run iteration, evaluate accept/reject. With a practiced operator, this takes 5-10 minutes per iteration, so a full tuning session is 30-60 minutes."));

children.push(p("**Concept: The stop condition is the acoustic analog of HUF's MDG threshold.** When the Marginal Drift Gap (improvement per iteration) falls below a significance threshold, further optimization is noise-chasing. The notebook prevents this by gating on tau_accept."));

// ═══════════════════════════════════════════════════════════════
// SECTION 10: CONCEPT CATALOG
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("10. Concept Catalog"));

children.push(p("The following concepts are embedded in the notebook, listed in order of their appearance and significance."));

children.push(h3("C1. Unity-Sum Closure"));
children.push(p("s = w / w.sum() guarantees \u03A3s\u1D62 = 1. The shares of the 6.02 dB gain budget are allocated exactly, with zero residual. This is the founding axiom of HUF governance, demonstrated here in its original acoustic context."));

children.push(h3("C2. Proportional Allocation by Physical Dimension"));
children.push(p("The share of each axis is proportional to dim\u1D47\u1D49\u1D57\u1D43. The physical world determines the allocation, not the operator's preference. Beta modulates the sensitivity but does not break closure."));

children.push(h3("C3. Coherence-Weighted Fitting"));
children.push(p("Frequency bins with low coherence are down-weighted or excluded. This is a form of data quality gating: the notebook trusts its measurements only where the measurement system says they are reliable."));

children.push(h3("C4. Damped Iterative Inference"));
children.push(p("The (1-\u03B1)*p_k + \u03B1*p_fit update rule prevents overcorrection. This is the same exponential smoothing used in Kalman filters, PID controllers, and HUF's governance damper."));

children.push(h3("C5. Accept/Reject Governance (ADAC)"));
children.push(p("The human decides, informed by the notebook's recommendation. The notebook cannot force an accept. This is the OCC 51/49 principle: the algorithm advises, the authority decides."));

children.push(h3("C6. Common-Mode / Differential Decomposition"));
children.push(p("Ecm = 0.5*(eL+eR) and Ed = 0.5*(eL-eR). This linear decomposition separates the problem into what the shared correction can address (Ecm) and what requires per-channel treatment (Ed). It is the acoustic analog of separating systematic risk from idiosyncratic risk in portfolio theory."));

children.push(h3("C7. Last-Known-Good Reversion"));
children.push(p("The LKG mechanism provides a safe fallback. If an iteration makes things worse (measurement error, environmental change), the operator can instantly recover. This is HUF's FM-3 (cascade) defense."));

children.push(h3("C8. Spatial Averaging Across Positions"));
children.push(p("The shared objective function aggregates residuals across P1-P3. This is equivalent to ensemble averaging in statistics: individual position biases are diluted by the aggregate. The position-to-position spread diagnostic flags when the ensemble is not representative."));

children.push(h3("C9. Immutable Audit Trail"));
children.push(p("manifest.json + iteration_log.csv + per-arm captures create a complete, reproducible record. Any JAES reviewer can reconstruct the exact sequence of decisions. This is HUF's decision log and run manifest."));

children.push(h3("C10. Anti-Drift Governance (Cell 9)"));
children.push(p("The notebook closes with an explicit statement of the HUF governance pattern: North Star (scope + constraints), Decision log, Run manifest, Critique diversity. This is not separate from the acoustic tool; it is the same instinct that motivates DADC/DADI/ADAC, stated in governance language."));

children.push(h3("C11. Regularization as Governance Constraint"));
children.push(p("The 0.02 regularization toward physical midpoints is a soft prior. It says: absent strong evidence, stay close to what the tape measure says. This is the acoustic equivalent of a Bayesian prior, or HUF's anchor against orphan drift."));

children.push(h3("C12. Hard Gates vs Soft Recommendations"));
children.push(p("Some constraints are hard (mic compliance, position count, coherence gate zero-out). Others are soft (accept/reject recommendation, position spread warning). The notebook distinguishes between what cannot be violated (hard gates) and what the operator can override with judgment (soft recommendations). This mirrors HUF's PROOF line (hard) vs MDG threshold (advisory)."));

// ═══════════════════════════════════════════════════════════════
// SECTION 11: WHAT CLAUDE MAY HAVE MISSED
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("11. What Claude May Have Missed"));

children.push(p("The following items warrant attention. Some are observations that need verification; others are potential gaps in my understanding."));

children.push(h3("M1. The dadc_df_fc_only Function"));
children.push(p("This function (line 587) builds a DADC table where gains come from p_gain (the shared solution) but Fc comes from p_fc (the per-channel fit). The comment says \"This reduces degrees of freedom and is safer against room chasing.\" I noted this but did not fully trace its integration path. It appears to be the backbone of the Fc-only per-channel mode. If there is additional intent behind separating the gain and frequency sources beyond what I described, I may have missed it."));

children.push(h3("M2. Branch and Snapshot System"));
children.push(p("The code contains capture_snapshot() (line 1341) and references to branch_id, suggesting a non-linear exploration model where the operator can fork the iteration history and explore alternative paths. I saw this in passing but did not fully trace the branch/restore UI logic. This is architecturally significant: it turns the iteration from a linear chain into a directed graph, which is HUF's reciprocity theorem in action (any s-to-g path is bounded)."));

children.push(h3("M3. The Scipy Fallback Grid Search"));
children.push(p("When scipy is not available, the optimizer falls back to a brute-force 5\u00D75\u00D75 grid search (125 evaluations) with 5% step size. This is crude but guarantees that the notebook works in constrained environments (e.g., a field laptop without scipy). I noted it but did not analyze whether the grid resolution is sufficient for convergence in all practical cases. It may introduce quantization artifacts in the apparent dimensions."));

children.push(h3("M4. The 0.35 dB Position Spread Threshold"));
children.push(p("The code flags a warning when position-to-position RMS spread exceeds 0.35 dB (line 1194). I did not find documentation for why this specific threshold was chosen. It may be empirical (derived from measurement campaigns) or theoretical (related to the expected variance from 3 spatial samples of a room mode field). This is worth documenting for the JAES manuscript."));

children.push(h3("M5. The lr_worsen Gate Asymmetry"));
children.push(p("The accept gate checks (lr_now - lr_prev) <= lr_worsen, which only penalizes worsening, not improvement. This means the gate is asymmetric: improving L/R mismatch is always allowed, but worsening is penalized. I noted this but did not explore whether there are edge cases where L/R improvement masks overall degradation."));

children.push(h3("M6. Per-Position RMS Uses Reference Mic Only"));
children.push(p("Lines 1132-1142 compute per-position RMS from the reference mic residuals, even if multiple mics contributed to the fit. The comment says \"stability.\" This design choice means the convergence metric is always grounded in a single, consistent measurement source, but it also means that aux mic information is used for fitting but not for evaluating fit quality. This is a deliberate asymmetry that could be worth discussing."));

children.push(h3("M7. The ExperimentState Dataclass"));
children.push(p("ExperimentState provides dict-like access via __getitem__ and __setitem__. This is a convenience wrapper, but it also means that any typo in a key name creates a new state entry silently (unlike a proper dataclass with defined fields). In a production tool, this could be a source of subtle bugs. For a research notebook, the flexibility is likely intentional."));

children.push(h3("M8. Coherence as Both Gate and Weight"));
children.push(p("Coherence serves double duty: bins below coh_gate are zeroed (hard gate), and bins above coh_gate use the coherence value as the weight (soft weighting). This means a bin with coherence 0.95 contributes more than a bin with coherence 0.70, and a bin with coherence below the gate contributes nothing. I noted this but did not analyze whether the transition at the gate boundary introduces discontinuities in the optimization surface."));

// ═══════════════════════════════════════════════════════════════
// SECTION 12: CONNECTIONS TO THE TRIAD
// ═══════════════════════════════════════════════════════════════
children.push(h1("12. Connections to the Triad"));

children.push(p("The DADC-DADI-ADAC notebook is not merely an acoustic tool. It is the proof-of-concept implementation of the entire HUF governance chain:"));

children.push(bullet("**DADC \u2192 Portfolio allocation.** dims\u1D47\u1D49\u1D57\u1D43 / sum maps directly to HUF's \u03C1\u1D62 = measure\u1D62 / \u03A3measure.", "bullets6"));
children.push(bullet("**DADI \u2192 Inference under uncertainty.** The optimizer infers hidden state (apparent dimensions) from noisy observations (room transfer functions), exactly as HUF infers portfolio health from anomaly counts.", "bullets6"));
children.push(bullet("**ADAC \u2192 Governance gate.** Accept/reject with improvement threshold and mismatch guard is the OCC 51/49 decision protocol.", "bullets6"));
children.push(bullet("**Loop A / Loop B \u2192 Shared vs per-element refinement.** Loop A adjusts the whole portfolio; Loop B adjusts individual elements with a hard constraint against drift.", "bullets6"));
children.push(bullet("**Common-mode / differential \u2192 Systematic vs idiosyncratic risk.** The decomposition is formally identical.", "bullets6"));
children.push(bullet("**LKG revert \u2192 Failure mode recovery.** FM-3 cascade defense.", "bullets6"));
children.push(bullet("**Manifest + log \u2192 Decision ledger.** Governance transparency.", "bullets6"));
children.push(bullet("**Cell 9 anti-drift note \u2192 HUF governance pattern.** The notebook names the connection explicitly.", "bullets6"));

children.push(p("Every concept in HUF's governance framework has its acoustic antecedent in this notebook. The notebook came first; HUF abstracted the pattern."));

// ═══════════════════════════════════════════════════════════════
// Footer
// ═══════════════════════════════════════════════════════════════
children.push(new Paragraph({ spacing: { before: 600 },
  border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
  children: [new TextRun({ text: "End of Surmise. Generated March 2026, Session 6+.", font: FONT, size: 20, italics: true, color: "666666" })] }));

// ── Build Document ──
const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: FONT },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: FONT },
        paragraph: { spacing: { before: 220, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering,
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "DADC-DADI-ADAC Operational Surmise", font: FONT, size: 18, italics: true, color: "999999" })] })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Page ", font: FONT, size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("DADC_DADI_ADAC_Operational_Surmise.docx", buffer);
  console.log("Written: DADC_DADI_ADAC_Operational_Surmise.docx (" + buffer.length + " bytes)");
});
