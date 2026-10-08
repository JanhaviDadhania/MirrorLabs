# Problem 076: Ultraflat real Littlewood polynomials

Source: OpenAI Research Catalog (Oct 6, 2026), entry 076. Based only on the catalog's
one-paragraph summary; the paper's construction is not reproduced here.

**Setting.** Choose N signs (+1/-1) as polynomial coefficients. Look at |P(z)| on the unit circle.
The average of |P|^2 is forced to be N, so the typical height is sqrt(N).

**Question.** Can the height be (1+o(1))*sqrt(N) at *every* point (ultraflat), with real +-1 coefficients?

**Known now (per catalog).** Yes, for all sufficiently large N. Merit factor -> infinity, disproving Turyn's conjecture.

Files:
- `littlewood.py` generates the figures (numpy, matplotlib).
- `fig1_setting.png`: signs -> polynomial -> height profile.
- `fig2_forced_average.png`: different sign choices all average to N, but shapes differ.
- `fig3_flatness_vs_N.png`: random and Rudin-Shapiro vs the ultraflat goal.
- `fig4_summary.png`: question / before / result.

The figures illustrate the question. They do not show ultraflat polynomials.
