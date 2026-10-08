# Replication Plan: Residence-Time Scaling in Grokking

---

## OUR IDEA (Janhavi, Oct 6, 2026)

**Claim:** Grokking time is inversely proportional to the product of learning rate and weight decay.

```
grok_step ≈ 2.28 × τ,  where τ = 1 / (lr × wd)
```

- Grok time when measured in "residence times" (how long weights persist) is nearly constant across different learning rates and weight decays.
- Data: 14 runs, 7 hyperparameter combos, 2 seeds. CV = 0.084 for grok/τ vs CV = 0.449 for raw steps. 5.3× tighter.
- Mechanism: weight decay is a first-order drain; once training loss hits zero (inflow shuts off), only the drain timescale τ remains.
- Prediction: grok_step = C / (lr × wd), where C is task/architecture-specific constant (~2.28 for mod-97 addition).

---

## PUBLISHED PAPER: "A Spectral Theory of Grokking"

**arXiv ID:** [2609.26679](https://arxiv.org/abs/2609.26679)  
**Authors:** Pracher, Lewkowycz, et al.  
**Date:** September 2026  
**Key Claim:**

> "The grokking timescale is controlled by the product of learning rate and weight decay. τ ∝ 1/(lr·wd)."

- Validates τ = 1/(lr·wd) scaling across an **84×90 grid** of experiments (7560 independent runs).
- Shows residual-driven kernel growth competing with weight decay.
- Derives feature-learning speedup near critical decay threshold.
- Extends to: varying seeds, multiple tasks (mod addition, modular subtraction, permutation).
- Provides theoretical foundation: weight decay induces feature learning; timescale is τ.

---

## OVERLAP ANALYSIS

| Aspect | Our Idea | Their Paper | Overlap % |
|---|---|---|---|
| Main formula | τ = 1/(lr·wd) | τ = 1/(lr·wd) | **100%** |
| Experimental validation | 14 runs, 2 seeds | 7560 runs, 84×90 grid | Same concept, much larger scale |
| Mechanism | Weight decay drain + inflow shutdown | Residual-driven kernel + weight decay | **~90%** — same root cause, different language |
| Prediction | grok ≈ 2.28τ | grok ≈ Cτ (C task-dependent) | **100%** |
| Constants | C ≈ 2.28 (mod-97) | C varies across tasks | **80%** — shape is same, C values differ |
| Caveats | Only tested on mod-97, full-batch | Multiple tasks; minibatch + full-batch | We are more limited |

**Overall Overlap: 95%**

The core claim is identical. Their work is more rigorous, more comprehensive, and published. The residence-time interpretation (stock/flow framing) is novel to us, but the formula itself is theirs.

---

## DECISION: REPLICATE

**Condition Met:** Main idea already exists in published form with stronger empirical validation.

**Action:** Replicate [2609.26679] with focus on:
1. Validating τ = 1/(lr·wd) on our own hardware (M3 MacBook)
2. Extending to tasks beyond mod arithmetic (permutation, modular subtraction)
3. Testing the residence-time stock/flow interpretation (our novel angle)

---

## REPLICATION PLAN (What to Do)

### Phase 1: Environment & Reproducibility (4 hours)
- Clone or reconstruct the experimental setup from the paper
- Target: modular addition mod 97, simple MLP (2·p → 256 → 256 → p)
- Verify baseline grokking on our machine
- Measure grok step for 2–3 (lr, wd) pairs to confirm formula

### Phase 2: Grid Sweep (12–16 hours on M3)
- Run an lr × wd grid: **7 × 5 = 35 configurations** (smaller than their 84×90 but testable on MacBook)
  - lr ∈ {1e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2}
  - wd ∈ {0.1, 0.5, 1.0, 2.0, 5.0}
- Run each for 1 seed; target: ~15k–30k steps per run
- Log: grok_step, τ = 1/(lr·wd), grok/τ

### Phase 3: Analysis (2 hours)
- Plot: grok_step vs τ (should be linear)
- Measure: correlation, R², residual variance
- Calculate: CV(grok_step) vs CV(grok/τ)
- Report: the constant C ≈ ?

### Phase 4: Novel Angle — Stock/Flow Interpretation (2 hours)
- Reframe their results in Meadows/Sterman language
- Document: how τ as a "residence time of the weight stock" differs from "decay timescale"
- Note: where stock/flow framing adds insight their paper doesn't have

### Phase 5: One Extended Task (2–4 hours, if time)
- Run modular subtraction mod 97 with 3–5 (lr, wd) pairs
- Check: does C stay ~2.28 or shift?

---

## Resource Requirements

| Resource | Requirement | Status |
|---|---|---|
| Time per run | 30–60 min (30k steps) | ✓ M3 MacBook can handle |
| Total compute | ~35 runs × 30 min = 17.5 hours | ✓ Reasonable overnight/over 2 days |
| Memory | ~2GB per run | ✓ M3 has 8GB+ |
| Storage | ~500MB for CSVs/logs | ✓ Abundant |
| Code | PyTorch, NumPy, Matplotlib | ✓ Already in .venv |

---

## Success Criteria

- [ ] Reproduce τ formula with R² > 0.95 on the grid
- [ ] CV(grok/τ) < 0.15 (tight clustering in residence times)
- [ ] Identify constant C within ±0.5 of 2.28
- [ ] Write-up: "Residence Time as Stock-Flow Interpretation" (500 words)

---

## Next Steps

1. **Spawn worker agent** to execute Phase 1–3
2. **Expected completion:** ~2 days (distributed runs)
3. **Output:** CSV with all 35 runs, plot, analysis summary

---

**Note:** This is not an original contribution. We are replicating published work ([2609.26679]) at smaller scale on available hardware. The novel aspect (if any) is the stock/flow interpretation and potential connection to oscillation dynamics (Idea 4). Those remain untouched by the literature found so far.
