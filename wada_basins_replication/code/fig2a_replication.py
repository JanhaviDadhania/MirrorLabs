"""Experiment 1: reproduce Fig. 2a (chaotic attractor in P+) of Ly & Gong, arXiv 2510.05606.
numpy float64. Step 0 checks the hand gradient against torch float64 autograd."""
import os
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(HERE, "reference", "mnn_dataset.npz"))
X, Y = d["X"], d["Y"]
e1 = np.array([1, 1, 0, 0]) / np.sqrt(2)
e2 = np.array([0, 0, 1, 1]) / np.sqrt(2)
LR = 2.5


def grad(theta):
    w1, w2 = theta[:2], theta[2:]
    h = np.tanh(np.sqrt(2) * X * w1)
    r = 0.5 * (h * w2).sum(1, keepdims=True) - Y
    g2 = (2 * r * 0.5 * h).mean(0)
    g1 = (2 * r * 0.5 * w2 * (1 - h**2) * np.sqrt(2) * X).mean(0)
    return np.concatenate([g1, g2])


def loss_t(th):
    Xt, Yt = torch.tensor(X), torch.tensor(Y)
    h = torch.tanh(np.sqrt(2) * Xt * th[:2])
    return ((0.5 * (h * th[2:]).sum(1, keepdim=True) - Yt) ** 2).mean()


# --- Step 0: gradient check against autograd on 200 random points (on and off P+)
rng = np.random.default_rng(1)
maxerr = 0.0
for _ in range(200):
    th = rng.normal(size=4) * 1.5
    t = torch.tensor(th, dtype=torch.float64, requires_grad=True)
    loss_t(t).backward()
    maxerr = max(maxerr, np.abs(t.grad.numpy() - grad(th)).max())
print(f"[gradient check] max |hand - autograd| over 200 points = {maxerr:.2e}")
assert maxerr < 1e-12, "gradient mismatch"

# --- Step 1-4: trajectory
np.random.seed(0)
a, b = np.random.rand(), np.random.rand()
theta = a * e1 + b * e2
T = 100_000
traj = np.empty((T + 1, 4)); traj[0] = theta
div = None
for i in range(T):
    theta = theta - LR * grad(theta)
    traj[i + 1] = theta
    if not np.isfinite(theta).all() or np.abs(theta).max() > 1e6:
        div = i + 1; traj = traj[:i + 1]; break
np.save(os.path.join(HERE, "fig2a_trajectory.npy"), traj)
print("start", np.round(traj[0], 4), "diverged at step:", div, " total iterates:", len(traj))
print("P+ check max|w1_1-w1_2|:", np.abs(traj[:, 0] - traj[:, 1]).max(),
      " max|w2_1-w2_2|:", np.abs(traj[:, 2] - traj[:, 3]).max())

# --- Step 5-6: drop last 6000, every second iterate
keep = traj[:len(traj) - 6000][::2]
ep = np.arange(0, len(traj) - 6000)[::2]
xk, yk = keep @ e1, keep @ e2
print(f"plotted points: {len(keep)}  x range [{xk.min():.2f}, {xk.max():.2f}]  y range [{yk.min():.2f}, {yk.max():.2f}]")

# --- Two-cluster question: do early and late dots separate?
third = len(keep) // 3
for name, s in [("early third", slice(0, third)), ("middle third", slice(third, 2 * third)), ("late third", slice(2 * third, None))]:
    print(f"{name:13s} mean(x,y)=({xk[s].mean():+.2f},{yk[s].mean():+.2f})  x[{xk[s].min():.2f},{xk[s].max():.2f}] y[{yk[s].min():.2f},{yk[s].max():.2f}]")
sign_frac = (xk > 0).mean()
print(f"fraction of plotted points with x>0: {sign_frac:.3f}")
# transitions between left (x<0) and right (x>0) halves
sg = np.sign(xk)
print("x sign flips between consecutive plotted points:", int((sg[1:] != sg[:-1]).sum()))
# is early/late separable by sign of x? (correlation of epoch with x)
print(f"corr(epoch, x)={np.corrcoef(ep, xk)[0,1]:+.3f}  corr(epoch, y)={np.corrcoef(ep, yk)[0,1]:+.3f}")

# --- figure
fig, axs = plt.subplots(1, 3, figsize=(17, 5.2))
sc = axs[0].scatter(xk, yk, c=ep / 1e4, s=0.6, cmap="viridis")
axs[0].set_title("Our Fig. 2a replication (seed-0 start, lr 2.5, float64)")
axs[0].set_xlabel(r"$\theta\cdot e_1$"); axs[0].set_ylabel(r"$\theta\cdot e_2$")
plt.colorbar(sc, ax=axs[0], label=r"Epoch ($\times10^4$)")
# same, shuffled draw order so late dots don't hide early ones
o = np.random.default_rng(0).permutation(len(xk))
axs[1].scatter(xk[o], yk[o], c=ep[o] / 1e4, s=0.6, cmap="viridis")
axs[1].set_title("Same points, random draw order"); axs[1].set_xlabel(r"$\theta\cdot e_1$")
axs[2].plot(ep / 1e4, xk, lw=0.3, label="x"); axs[2].plot(ep / 1e4, yk, lw=0.3, label="y")
axs[2].set_title("Coordinates vs epoch"); axs[2].set_xlabel(r"Epoch ($\times10^4$)"); axs[2].legend()
plt.tight_layout()
plt.savefig(os.path.join(HERE, "fig2a_replication.png"), dpi=140)
print("saved fig2a_replication.png")

# --- Optional: Lyapunov exponents (QR method), first 1e4 steps, torch float64 Hessian
N = 10_000
Q = np.eye(4)  # basis order: e1,e2,e3,e4 -> use columns as given below
Q = np.stack([e1, e2, np.array([1, -1, 0, 0]) / np.sqrt(2), np.array([0, 0, 1, -1]) / np.sqrt(2)], 1)
logs = np.zeros(4)
for i in range(N):
    t = torch.tensor(traj[i], dtype=torch.float64)
    H = torch.autograd.functional.hessian(loss_t, t).numpy()
    J = np.eye(4) - LR * H
    Q, R = np.linalg.qr(J @ Q)
    logs += np.log(np.abs(np.diag(R)))
lam = logs / N
print("Lyapunov (first 1e4 steps) lambda1..4 =", np.round(lam, 4), " paper: 0.1564 0.0256 -0.0645 -0.2047")
