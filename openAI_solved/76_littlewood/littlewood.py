"""Problem 76 (OpenAI catalog): ultraflat real Littlewood polynomials.

A Littlewood polynomial has +-1 coefficients. We look at |P(z)| on the unit circle.
Forced fact: mean of |P|^2 over the circle is exactly N, so the typical height is sqrt(N).
Ultraflat = |P(z)| = (1+o(1)) sqrt(N) at EVERY point.

This script only illustrates the question (it does NOT construct the ultraflat polynomials
from the result; that construction is in the paper and not reproduced here).
It draws: the setting, the forced average, random vs. structured sequences, and the
merit factor, N^2 / (sum_{k>=1} C_k^2 * 2), where C_k are aperiodic autocorrelations.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(0)


def profile(a, M=4096):
    """|P(e^{i t})| for t in [0, 2pi), via zero-padded FFT."""
    return np.abs(np.fft.fft(a, M))


def merit_factor(a):
    N = len(a)
    c = np.correlate(a, a, mode="full")[N:]  # C_1..C_{N-1}
    return N**2 / (2 * np.sum(c**2))


def rudin_shapiro(n_pow):
    a = np.array([1.0])
    b = np.array([1.0])
    for _ in range(n_pow):
        a, b = np.concatenate([a, b]), np.concatenate([a, -b])
    return a


def barker13():
    return np.array([1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1], float)


# ---- Fig 1: the setting ----
a = np.array([1, -1, -1, 1, -1], float)
N = len(a)
M = 2048
t = np.linspace(0, 2 * np.pi, M, endpoint=False)
h = profile(a, M)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
ax[0].stem(range(N), a, basefmt=" ")
ax[0].set_title("1. Pick N signs (+1 / -1)")
ax[0].set_xlabel("position k"); ax[0].set_ylabel("coefficient a_k"); ax[0].set_ylim(-1.5, 1.5)
ax[0].text(0.02, -1.35, "P(z) = a0 + a1 z + ... + a_{N-1} z^{N-1}", fontsize=9)
th = np.linspace(0, 2 * np.pi, 400)
ax[1].plot(np.cos(th), np.sin(th), "k-", lw=1)
ax[1].plot(np.cos(t) * h / np.sqrt(N), np.sin(t) * h / np.sqrt(N), "C3", lw=1.5)
ax[1].set_aspect("equal"); ax[1].set_title("2. Radius = |P(z)|/sqrt(N)\n(black circle = perfectly flat)")
ax[2].plot(t, h, "C3"); ax[2].axhline(np.sqrt(N), color="k", ls="--", label="sqrt(N)")
ax[2].set_title("3. Same thing unrolled: height around the circle")
ax[2].set_xlabel("angle t (z = e^{it})"); ax[2].set_ylabel("|P(z)|"); ax[2].legend()
plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig1_setting.png"), dpi=140); plt.close()

# ---- Fig 2: forced average = N, but shape is free ----
N = 64
cands = {
    "random signs": rng.choice([-1.0, 1.0], N),
    "all +1": np.ones(N),
    "Rudin-Shapiro": rudin_shapiro(6),
}
fig, ax = plt.subplots(1, 3, figsize=(14, 3.8), sharey=True)
t = np.linspace(0, 2 * np.pi, 4096, endpoint=False)
for axi, (name, s) in zip(ax, cands.items()):
    h = profile(s)
    axi.plot(t, h, lw=1)
    axi.axhline(np.sqrt(N), color="k", ls="--")
    axi.set_title(f"{name}\nmean |P|^2 = {np.mean(h**2):.1f} (always N={N})\n"
                  f"max/sqrt(N) = {h.max()/np.sqrt(N):.2f}, min/sqrt(N) = {h.min()/np.sqrt(N):.2f}")
    axi.set_xlabel("angle t")
ax[0].set_ylabel("|P(e^{it})|")
plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig2_forced_average.png"), dpi=140); plt.close()

# ---- Fig 3: how flat can ordinary choices get as N grows ----
Ns = [2**k for k in range(3, 13)]
rs_ratio, rand_ratio, rs_mf, rand_mf = [], [], [], []
for k in range(3, 13):
    s = rudin_shapiro(k); n = len(s)
    h = profile(s, 8 * n)
    rs_ratio.append(h.max() / np.sqrt(n)); rs_mf.append(merit_factor(s))
    r = rng.choice([-1.0, 1.0], n)
    h = profile(r, 8 * n)
    rand_ratio.append(h.max() / np.sqrt(n)); rand_mf.append(merit_factor(r))
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].semilogx(Ns, rand_ratio, "o-", label="random signs")
ax[0].semilogx(Ns, rs_ratio, "s-", label="Rudin-Shapiro")
ax[0].axhline(1, color="k", ls="--", label="ultraflat goal (->1)")
ax[0].set_xlabel("N"); ax[0].set_ylabel("max |P| / sqrt(N)")
ax[0].set_title("Peak height: both stay well above 1\n(Rudin-Shapiro flat at ~sqrt(2); random keeps rising)")
ax[0].legend()
ax[1].semilogx(Ns, rand_mf, "o-", label="random signs")
ax[1].semilogx(Ns, rs_mf, "s-", label="Rudin-Shapiro")
ax[1].set_xlabel("N"); ax[1].set_ylabel("merit factor")
ax[1].set_title("Merit factor (bigger = flatter on average)\nTuryn: stays bounded. Result 076: -> infinity")
ax[1].legend()
plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig3_flatness_vs_N.png"), dpi=140); plt.close()

# ---- Fig 4: what was unknown vs known (schematic) ----
fig, ax = plt.subplots(figsize=(10, 3.6)); ax.axis("off")
rows = [
    ("Question", "Can +-1 coefficients make |P| ~ sqrt(N) EVERYWHERE on the circle?"),
    ("Before", "Complex unit-size coefficients: yes.  Real +-1 (incl. endpoints z=+-1): open."),
    ("Turyn's belief", "Merit factor stays bounded, i.e. you can never be arbitrarily flat."),
    ("Result 076", "Ultraflat real Littlewood polynomials exist for all large N;\nmerit factor -> infinity, so Turyn's conjecture is false."),
]
for i, (k, v) in enumerate(rows):
    y = 0.9 - i * 0.24
    ax.text(0.0, y, k, fontweight="bold", fontsize=11, va="top")
    ax.text(0.2, y, v, fontsize=10.5, va="top")
plt.savefig(os.path.join(HERE, "fig4_summary.png"), dpi=140, bbox_inches="tight"); plt.close()

print("merit factor Barker-13:", round(merit_factor(barker13()), 2))
print("done")
