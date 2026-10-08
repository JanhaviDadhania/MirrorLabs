"""Henon attractor: a 2D map, one dot per step, colored by step (same style as the paper's Fig. 2)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

a, b = 1.4, 0.3
n = 20000
x, y = 0.1, 0.1
pts = np.empty((n, 2))
for i in range(n):
    x, y = 1 - a * x * x + y, b * x      # one "training step"
    pts[i] = (x, y)

fig, ax = plt.subplots(figsize=(6, 4.5))
sc = ax.scatter(pts[:, 0], pts[:, 1], c=np.arange(n), s=0.4, cmap="viridis")
fig.colorbar(sc, label="step")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("Henon attractor: each dot = one step of the map")
plt.tight_layout(); plt.savefig("henon_demo.png", dpi=150)
print("saved")
