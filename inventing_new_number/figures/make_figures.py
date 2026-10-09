"""Figures for numbers_as_waves.md. Run: python make_figures.py"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = __file__.rsplit("/", 1)[0] + "/"
BLUE, ORANGE, GREEN, GREY, RED = "#2b6cb0", "#dd6b20", "#2f855a", "#718096", "#c53030"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name):
    fig.savefig(OUT + name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. The ladder: each doubling loses a rule
def fig_ladder():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    steps = [("ℝ", "1", "real", ""),
             ("ℂ", "2", "complex", "loses: bigger / smaller"),
             ("ℍ", "4", "quaternions", "loses: ab = ba"),
             ("𝕆", "8", "octonions", "loses: (ab)c = a(bc)"),
             ("𝕊", "16", "sedenions", "loses: division")]
    for k, (sym, n, name, lost) in enumerate(steps):
        x = k * 2.1
        ok = k < 4
        box = FancyBboxPatch((x, 0.9), 1.5, 1.3, boxstyle="round,pad=0.05",
                             fc="#ebf4ff" if ok else "#fff5f5",
                             ec=BLUE if ok else RED, lw=2)
        ax.add_patch(box)
        ax.text(x + 0.75, 1.75, sym, ha="center", va="center", fontsize=26)
        ax.text(x + 0.75, 1.15, f"{n} part{'s' if n != '1' else ''}", ha="center", fontsize=10)
        ax.text(x + 0.75, 2.45, name, ha="center", fontsize=11, weight="bold")
        if lost:
            ax.text(x + 0.75, 0.55, lost, ha="center", fontsize=9, color=RED if not ok else GREY)
        if k:
            ax.annotate("", xy=(x - 0.05, 1.55), xytext=(x - 0.55, 1.55),
                        arrowprops=dict(arrowstyle="->", lw=1.8, color=GREY))
            ax.text(x - 0.3, 1.75, "×2", ha="center", fontsize=9, color=GREY)
    ax.text(4.2 * 1.0 + 0.5, 0.05, "Hurwitz (1898): division survives only at 1, 2, 4, 8",
            ha="center", fontsize=10, style="italic")
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0, 2.8)
    save(fig, "fig1_ladder.png")


# 2. The u^2 = t dial: where division breaks
def fig_dial():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7))
    a = np.linspace(-2, 2, 400)
    for ax, t, title in zip(axes, [-1, 0, 1],
                            ["t = −1  (complex)", "t = 0  (dual)", "t = +1  (split-complex)"]):
        A, B = np.meshgrid(a, a)
        ax.contourf(A, B, A**2 - t * B**2, levels=30, cmap="Blues", alpha=0.6)
        if t == 0:
            ax.axvline(0, color=RED, lw=3)
        elif t == 1:
            ax.plot(a, a, color=RED, lw=3)
            ax.plot(a, -a, color=RED, lw=3)
        ax.plot(0, 0, "o", color=RED, ms=7)
        ax.set_title(title)
        ax.set_xlabel("a")
        ax.set_ylabel("b")
        ax.set_aspect("equal")
    fig.suptitle("Numbers a + b·u with u² = t.  Red: nonzero numbers you can't divide by "
                 "(a² − t·b² = 0)", y=1.02)
    save(fig, "fig2_dial.png")


# 3. Numbers as shapes; adding = smearing
def fig_shapes():
    x = np.linspace(-1, 9, 2000)
    dx = x[1] - x[0]
    bump = lambda m, s: np.exp(-(x - m) ** 2 / (2 * s**2)) / (s * np.sqrt(2 * np.pi))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))

    ax = axes[0]
    for m, c, lab in [(2, BLUE, "2"), (3, ORANGE, "3"), (5, GREEN, "2 + 3 = 5")]:
        ax.vlines(m, 0, 1, color=c, lw=4, label=lab)
    ax.set_title("Exact numbers are spikes")
    ax.set_yticks([])
    ax.set_xlim(0, 7)
    ax.legend(frameon=False)

    ax = axes[1]
    f, g = bump(2, 0.4), bump(3, 0.6)
    h = bump(5, np.sqrt(0.4**2 + 0.6**2))  # smearing two bumps: centres add, spreads add in quadrature
    ax.plot(x, f, color=BLUE, lw=2, label="about 2")
    ax.plot(x, g, color=ORANGE, lw=2, label="about 3")
    ax.plot(x, h, color=GREEN, lw=2.5, label="smeared: about 5, wider")
    ax.set_title("Fuzzy numbers are bumps; adding = smearing")
    ax.set_yticks([])
    ax.set_xlim(0, 8)
    ax.legend(frameon=False)
    save(fig, "fig3_shapes.png")


# 4. Real waves multiply wrong
def fig_real_wave_fails():
    x = np.linspace(0, 2 * np.pi, 1000)
    fig, axes = plt.subplots(2, 1, figsize=(10, 4.6), sharex=True)
    axes[0].plot(x, np.cos(3 * x), color=BLUE, lw=2, label="cos(3x)")
    axes[0].plot(x, np.cos(-3 * x), color=ORANGE, lw=2, ls="--", label="cos(−3x): identical")
    axes[0].set_title("Failure 1: a real wave can't tell 3 from −3")
    axes[0].legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    axes[1].plot(x, np.cos(2 * x) * np.cos(3 * x), color="black", lw=2.5, label="cos(2x)·cos(3x)")
    axes[1].plot(x, 0.5 * np.cos(5 * x), color=GREEN, lw=1.3, label="½ cos(5x)  ← wanted 5")
    axes[1].plot(x, 0.5 * np.cos(x), color=RED, lw=1.3, label="½ cos(1x)  ← unwanted 3 − 2")
    axes[1].set_title("Failure 2: combining 2 and 3 gives half 5, half 1")
    axes[1].legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=9)
    for ax in axes:
        ax.set_yticks([-1, 0, 1])
    axes[1].set_xlabel("x")
    save(fig, "fig4_real_wave_fails.png")


# 5. Spinning wave: e^{iax} as a corkscrew
def fig_spin():
    x = np.linspace(0, 2 * np.pi, 600)
    fig = plt.figure(figsize=(12, 4))
    panels = [(3, BLUE, r"$e^{i3x}$: spins one way"),
              (-3, ORANGE, r"$e^{-i3x}$: spins the other way"),
              (5, GREEN, r"$e^{i2x} \cdot e^{i3x} = e^{i5x}$")]
    for k, (a, c, title) in enumerate(panels):
        ax = fig.add_subplot(1, 3, k + 1, projection="3d")
        ax.plot(x, np.cos(a * x), np.sin(a * x), color=c, lw=2)
        ax.plot(x, np.cos(a * x), -1.4 * np.ones_like(x), color=GREY, lw=1, alpha=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x")
        ax.set_ylabel("real (cos)")
        ax.set_zlabel("imag (sin)")
        ax.set_zlim(-1.4, 1.2)
        ax.view_init(18, -60)
    fig.text(0.5, -0.02, "Grey shadow = the real part alone. For ±3 the shadows are identical; "
             "the spin direction is what tells them apart.", ha="center", fontsize=10)
    save(fig, "fig5_spinning_waves.png")


# 6. Classical uncertainty: short sound -> many pitches
def fig_uncertainty():
    t = np.linspace(-20, 20, 4096)
    freqs = np.fft.fftshift(np.fft.fftfreq(t.size, t[1] - t[0]))
    fig, axes = plt.subplots(2, 2, figsize=(10, 4.6))
    for row, (width, label) in enumerate([(0.4, "short clap"), (6, "long note")]):
        s = np.exp(-t**2 / (2 * width**2)) * np.cos(2 * np.pi * 1.0 * t)
        spec = np.abs(np.fft.fftshift(np.fft.fft(s)))
        axes[row, 0].plot(t, s, color=BLUE, lw=1.5)
        axes[row, 0].set_xlim(-15, 15)
        axes[row, 0].set_ylabel(label)
        axes[row, 1].plot(freqs, spec / spec.max(), color=ORANGE, lw=2)
        axes[row, 1].set_xlim(0, 2)
        for ax in axes[row]:
            ax.set_yticks([])
    axes[0, 0].set_title("in time (where)")
    axes[0, 1].set_title("in pitch (which wave)")
    axes[1, 0].set_xlabel("time")
    axes[1, 1].set_xlabel("pitch")
    fig.suptitle("Ordinary sound, real numbers, no quantum: sharp in time ⇒ spread in pitch", y=1.0)
    save(fig, "fig6_classical_uncertainty.png")


# 7. Quantization as counting: windings around a ring
def fig_winding():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), subplot_kw={"aspect": "equal"})
    s = np.linspace(0, 2 * np.pi, 400)
    for ax, n in zip(axes, [1, 2, 2.5]):
        ax.plot(np.cos(s), np.sin(s), color=GREY, lw=1)
        for th in np.linspace(0, 2 * np.pi, 24, endpoint=False):
            ph = n * th
            px, py = np.cos(th), np.sin(th)
            ax.arrow(px, py, 0.22 * np.cos(ph), 0.22 * np.sin(ph), head_width=0.06,
                     color=BLUE if float(n).is_integer() else RED, lw=1.2)
        closes = float(n).is_integer()
        ax.set_title(f"{n} turn{'s' if n != 1 else ''} per lap: "
                     + ("closes ✓" if closes else "mismatch at the seam ✗"),
                     color="black" if closes else RED, fontsize=11)
        if not closes:
            ax.plot(1, 0, "o", ms=14, mfc="none", mec=RED, mew=2)
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        ax.axis("off")
    fig.suptitle("A spinning arrow carried around a ring must match itself when it gets back. "
                 "Only whole numbers of turns fit.", y=1.02)
    save(fig, "fig7_winding.png")


if __name__ == "__main__":
    fig_ladder()
    fig_dial()
    fig_shapes()
    fig_real_wave_fails()
    fig_spin()
    fig_uncertainty()
    fig_winding()
    print("done")
