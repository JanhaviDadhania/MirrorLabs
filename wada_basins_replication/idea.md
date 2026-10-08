# Replication Plan: Wada Basin Boundaries in Neural Network Training

---

## OUR IDEA (Janhavi, Oct 8, 2026)

**Claim:** In the training of a small neural network, the basin boundaries have the Wada property. Every boundary point touches all the basins (all the minima / outcomes). No boundary point touches only some of them. A start is either deep inside one basin, or on a boundary where all outcomes meet.

```
for every boundary point x, and every radius r > 0:
    the ball B(x, r) contains starts that end in ALL outcomes
```

- Colors are basins (sets of starting weights). Minima are where they end up.
- Wada needs at least 3 outcomes. With 2 it is meaningless.
- This is stronger than "the boundary is fractal" and stronger than "riddled".
- Link to idea 1: if many circuits compete, every dominance shift happens on one shared boundary, not on a bracket of pairwise boundaries (see `../ideas/wada_basins_in_neural_networks.txt`).

**Tightening done on Oct 8** (after discussion):
- "All points" is false by definition. Wada is about boundary points only.
- "Can reach any minimum" is false for a single run. Gradient descent is deterministic. Wada says nearby starts reach all of them.
- "Either one or all, nothing in between" is a statement about boundary points. It is not a statement about the fraction of space that is uncertain.

**Not yet tested by us.** Nothing below is a result.

---

## PUBLISHED PAPER: "Fractal basin geometry and the limits to predictability and reproducibility in deep learning"

**arXiv ID:** [2510.05606](https://arxiv.org/abs/2510.05606)
**Authors:** Andrew Ly and Pulin Gong (University of Sydney)
**Venue:** to be published in Nature Machine Intelligence (per arXiv comments)
**Code:** https://github.com/anly2178/riddled_basins_neural_network (MIT license)
**Data:** https://doi.org/10.24433/CO.8310374.v1 (Code Ocean)
**Key claim (from the abstract, paraphrased):** training outcomes are governed by fractal, riddled basin geometry. Near any start that reaches one solution, there are starts that reach other solutions, at every scale.

What they did (read from the HTML version and the repo):

- **Minimal model:** two-layer tanh network, 4 parameters, full-batch GD at η = 2.5, 8 Gaussian regression points. Image is a 2047×2047 grid on a random 2D plane through parameter space. Colors: blue → P+, orange → P−, white → infinity or off-plane attractors. That is already **3 colors**.
- **Deep networks:** tapered bias-free VGG-12, 12,036 parameters, SGD, MNIST with 50% label noise, 255×255 grid. Outcomes are labeled by which neurons vanish (1772 neurons). About 500,000 networks trained overall, also ResNet and BERT.
- **Measurements:** uncertainty exponent φ and Lyapunov exponents. φ = 0.0126 ± 0.0002 (minimal model), 0.000 ± 0.002 (VGG-12, GPU and CPU). Functional exponent 0.00 ± 0.01.
- **One-bit test:** the code (`dnn_one_bit.py`) flips the lowest bit of **one** float32 parameter and retrains. The paper reports f(ε) = 0.477 for these flips (VGG-12). I have not read the part of the script that forms pairs.
- **Wada:** not tested in the main text. It only points to Supplementary Sec. 3 about "hyperparameter-space fractality resembling lakes of Wada". I could not read the supplement.
- **Not reported:** the prefactor c, for any network. Per-architecture numbers for ResNet and BERT are in Extended Data and the Supplement, which I did not read.

**Related work:**

- [Testing for Basins of Wada](https://www.nature.com/articles/srep16579) (Daza, Wagemakers, Sanjuán, Yorke, 2015): the merging method.
- Kennedy & Yorke (1991), "Basins of Wada": Wada basins occur in ordinary dissipative systems.
- [The Butterfly Effect](https://arxiv.org/pdf/2506.13234): training is highly sensitive to initial conditions. Findings not read.
- Search of Oct 7 found no paper testing Wada in neural network training. This is five searches, not a literature review.

---

## OVERLAP ANALYSIS

| Aspect | Our Idea | Their Paper | Overlap |
|---|---|---|---|
| Fractal basin boundaries in NN training | Assumed | Shown (φ ≈ 0) | **High** |
| Riddled basins | Implied | Claimed and analysed | **High** |
| Slice method (random 2D plane, color by outcome) | Planned | Used | **Same method** |
| Uncertainty exponent | Planned | Measured | **Same method** |
| Wada property (every boundary point touches ≥ 3 basins) | **Core claim** | Not in main text, only a pointer to the supplement | **Unknown, likely low** |
| Merging test | Planned | Not seen | **None seen** |
| Outcomes = circuits (Fourier signature of logits) | Planned for grokking | Outcomes = vanished-neuron subspaces | **Different** |
| Grokking tasks | Target | Not studied | **None** |
| Prefactor c | Will report | Not reported | **None** |

**Overall overlap: high on fractal and riddled, unknown on Wada.**

Riddled is not Wada. Riddled says every point of a basin has other outcomes arbitrarily close. Wada says every boundary point touches at least 3 basins. Related, but separate tests. Their near-zero exponent supports the fractal part of our claim only.

---

## DECISION: REPLICATE, THEN EXTEND

**Condition:** The slice method and the exponent measurement are published, with code. The Wada test may be unpublished, or only in the supplement.

**Action:**
1. Read Supplementary Sec. 3 first. If they already tested Wada, we replicate that and the idea becomes an extension to grokking.
2. Replicate their minimal-model image and exponent.
3. Run the merging test on it. This is the cheapest Wada test.
4. Move to a small grokking network, with circuits as outcomes.

---

## REPLICATION PLAN (What to Do)

### Phase 0: Read before running (1–2 hours)
- Download the supplement: https://arxiv.org/src/2510.05606v2/anc
- Read Sec. 3 (Wada) and the Methods on how pairs are formed.
- Read the rest of `dnn_one_bit.py`.
- Decide whether the plan below changes.

### Phase 1: Reproduce their minimal model (1 day)
- Clone the repo. Pinned: Python 3.10, JAX 0.6.0, Flax, Optax.
- Run `Code/mnn_main.py` (README: about 12 hours on a normal computer).
- Compare our image and exponent to the paper's: φ ≈ 0.0126.
- Check the Code Ocean data against our output.

### Phase 2: Merging test on the minimal model (1 day)
- Three colors already exist: P+, P−, and white.
- Compute the box-counting dimension of the full boundary.
- Merge each pair of colors in turn, then recompute.
  - **Wada:** dimension unchanged under every merge.
  - **Not Wada:** dimension drops for the merge of the two basins that share a stretch.
- Check the white region first. It lumps several attractors together, so it may need splitting.

### Phase 3: Grokking network (2–3 days)
- Task: modular addition mod 97, small MLP, full batch, deterministic.
- Slice: random 2D plane through initialization space.
- Outcome label: Fourier signature of the logits (which key frequencies the model converges on). This ignores permutation symmetry.
- Count distinct outcomes first. If fewer than 3, stop. Wada is vacuous here.
- Run the merging test and the uncertainty exponent.
- Port the slice-and-train loop to PyTorch (their code is JAX).

### Phase 4: Sweeps and controls (2–3 days)
- **Learning-rate sweep.** Prediction: exponent goes toward 1 (smooth) at small steps. If it stays near 0, our step-size argument is wrong.
- **float32 vs float64.** If the maps differ, we are measuring rounding noise.
- **Many planes, several zoom levels.** One picture proves nothing.
- **Basin entropy** as a second fractality measure.
- **Report the prefactor c.** The paper does not. It decides whether "unpredictable" is a small caveat or the main behavior.

### Phase 5: One-bit test on grokking (1 day, if time)
- Flip one bit in one weight, train, record the circuit signature.
- Repeat over many weights. Report the fraction that change the outcome.

---

## Resource Requirements

| Resource | Requirement | Status |
|---|---|---|
| Minimal model run | about 12 hours (per their README) | Reasonable on a laptop, JAX install untested |
| Grokking slice | e.g. 100×100 grid, 1 run each | Small MLP, full batch, a few minutes per run |
| VGG-12 and ResNet reruns | about 6 weeks on GPU (per their README) | **Not feasible.** Use their Code Ocean data instead |
| Code | JAX (theirs), PyTorch (ours) | Must port the slice loop |
| Storage | CSVs, images | Small |

---

## Success Criteria

- [ ] Reproduce their minimal-model exponent: φ within error of 0.0126.
- [ ] Reproduce their minimal-model image qualitatively.
- [ ] Merging test gives a clear answer on the minimal model (Wada or not).
- [ ] At least 3 distinct circuit outcomes found in the grokking network.
- [ ] Exponent and prefactor c reported for grokking.
- [ ] float32 and float64 maps agree.
- [ ] Learning-rate sweep done.

## Failure Conditions (written before running)

- Merging two basins shrinks the boundary dimension → not Wada.
- Fewer than 3 outcomes → Wada is vacuous for that task.
- Exponent near 1 → smooth boundary.
- Maps differ between float32 and float64 → numerical noise.
- Exponent near 1 at small step size is **not** a failure of the idea. It is the predicted result.

---

## Caveats

- Wada is a property of the boundary's shape. It does not show that training trajectories spend time near boundaries. That is a separate claim, needed for the explanatory story in idea 1.
- Training with SGD is not a deterministic map. Full batch first.
- A 2D slice of a huge space can mislead. Wada must hold at every scale.
- I have not run any of the paper's code. "Reproducible" so far means the materials are documented.
- All paper details above come from the arXiv HTML text and the repo, read through a summarizer. Check the numbers against the paper before quoting them.
- The 5 searches did not cover everything. Do not claim novelty until Phase 0 is done.

---

## Next Steps

1. Read the supplement and the rest of `dnn_one_bit.py` (Phase 0).
2. Clone the repo and run the minimal model.
3. Merging test.

---

**Note:** The Wada property is the only part that may be new. The slice method, the exponent and the code are Ly & Gong's. If their supplement already tests Wada, our contribution narrows to grokking, circuit outcomes and the step-size dependence.
