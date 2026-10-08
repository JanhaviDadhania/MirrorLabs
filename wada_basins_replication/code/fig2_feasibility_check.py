"""FEASIBILITY CHECK ONLY (not the replication). Numbers only, no figure.
Mirrors Code/mnn_main.py::characterize_attractor(2.5, 1e5) from the authors' repo, in plain numpy float64."""
import numpy as np

# --- data exactly as create_random_dataset(8, 1): seed 0, X then Y
np.random.seed(0)
X = np.random.randn(8, 1)
Y = np.random.randn(8, 1)

# --- start exactly as characterize_attractor: seed 0, uniform[0,1) coefficients on e1, e2
np.random.seed(0)
e1 = np.array([1, 1, 0, 0]) / np.sqrt(2)
e2 = np.array([0, 0, 1, 1]) / np.sqrt(2)
theta = np.random.rand() * e1 + np.random.rand() * e2     # (w1_1, w1_2, w2_1, w2_2)

def grad(theta):
    w1, w2 = theta[:2], theta[2:]
    s = np.sqrt(2) * X * w1                 # (8,2)
    h = np.tanh(s)
    f = 0.5 * (h * w2).sum(1, keepdims=True)           # (8,1)
    r = f - Y
    g2 = (2 * r * 0.5 * h).mean(0)                     # d/dw2
    g1 = (2 * r * 0.5 * w2 * (1 - h**2) * np.sqrt(2) * X).mean(0)   # d/dw1
    return np.concatenate([g1, g2])

lr, T = 2.5, 100_000
traj = np.empty((T + 1, 4)); traj[0] = theta
div = None
for i in range(T):
    theta = theta - lr * grad(theta)
    traj[i + 1] = theta
    if not np.isfinite(theta).all() or np.abs(theta).max() > 1e6:
        div = i + 1; traj = traj[:i + 1]; break

x = traj @ e1; y = traj @ e2
print("X[:3]", np.round(X[:3, 0], 4), " Y[:3]", np.round(Y[:3, 0], 4))
print("start theta", np.round(traj[0], 4), " rand()s =", np.round(traj[0] @ e1, 4), np.round(traj[0] @ e2, 4))
print("diverged at step:", div)
keep = traj[:max(len(traj) - 6000, 1)]
xk = keep @ e1; yk = keep @ e2
print("kept points:", len(keep), " x range", np.round([xk.min(), xk.max()], 2), " y range", np.round([yk.min(), yk.max()], 2))
print("off-plane check max|w1_1-w1_2|:", np.abs(traj[:, 0] - traj[:, 1]).max(), " max|w2_1-w2_2|:", np.abs(traj[:, 2] - traj[:, 3]).max())
