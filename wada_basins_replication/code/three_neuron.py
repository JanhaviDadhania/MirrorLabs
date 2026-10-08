"""Three-hidden-neuron variant of the paper's minimal model (1 -> 3 tanh -> 1, 6 weights, no biases).
f(x) = (1/3) * sum_i w2_i * tanh(sqrt(2) * w1_i * x)   (alpha1 = sqrt(2), alpha2 = 1/n, mean-field)
theta = (w1_0, w1_1, w1_2, w2_0, w2_1, w2_2). Same 8-point dataset, full-batch GD, numpy float64.

Start lies in the invariant subspace S = {neurons 0 and 1 identical}: (a, a, b, c, c, d).
GD stays in S exactly. S is 4D: a=pair input, c=pair output, b=third input, d=third output.
3D plots use (a, c, b) and (a, c, d).

usage: python three_neuron.py test   # short lr scan + gradient check
       python three_neuron.py full LR [T]
"""
import os, sys
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(HERE, "reference", "mnn_dataset.npz"))
X, Y = d["X"], d["Y"]
N = 3
A1, A2 = np.sqrt(2), 1.0 / N


def grad(theta):
    w1, w2 = theta[:N], theta[N:]
    h = np.tanh(A1 * X * w1)
    r = A2 * (h * w2).sum(1, keepdims=True) - Y
    g2 = (2 * r * A2 * h).mean(0)
    g1 = (2 * r * A2 * w2 * (1 - h**2) * A1 * X).mean(0)
    return np.concatenate([g1, g2])


def loss_t(th):
    Xt, Yt = torch.tensor(X), torch.tensor(Y)
    h = torch.tanh(A1 * Xt * th[:N])
    return ((A2 * (h * th[N:]).sum(1, keepdim=True) - Yt) ** 2).mean()


def grad_check():
    rng = np.random.default_rng(1)
    err = 0.0
    for _ in range(200):
        th = rng.normal(size=2 * N) * 1.5
        t = torch.tensor(th, requires_grad=True)
        loss_t(t).backward()
        err = max(err, np.abs(t.grad.numpy() - grad(th)).max())
    return err


def start():
    np.random.seed(0)
    a, c, b, dd = np.random.rand(4)
    return np.array([a, a, b, c, c, dd])


def run(lr, T):
    th = start()
    traj = np.empty((T + 1, 2 * N)); traj[0] = th
    div = None
    for i in range(T):
        th = th - lr * grad(th)
        traj[i + 1] = th
        if not np.isfinite(th).all() or np.abs(th).max() > 1e6:
            div = i + 1; traj = traj[:i + 1]; break
    return traj, div


def lyapunov(traj, n):
    Q = np.eye(2 * N); logs = np.zeros(2 * N)
    for i in range(n):
        H = torch.autograd.functional.hessian(loss_t, torch.tensor(traj[i])).numpy()
        Q, R = np.linalg.qr((np.eye(2 * N) - LR_CUR * H) @ Q)
        logs += np.log(np.abs(np.diag(R)))
    return logs / n


mode = sys.argv[1]
err = grad_check()
print(f"[gradient check] max |hand - autograd| over 200 points = {err:.2e}")
assert err < 1e-12

if mode == "test":
    T = 20000
    print(f"start {np.round(start(), 4)}  T={T}")
    print(f"{'lr':>5} {'diverged':>9} {'in S (max dev)':>15} {'last-2000 std':>14} {'|theta| max':>12}")
    for lr in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        traj, div = run(lr, T)
        dev = max(np.abs(traj[:, 0] - traj[:, 1]).max(), np.abs(traj[:, 3] - traj[:, 4]).max())
        tail = traj[-2000:]
        print(f"{lr:5.1f} {str(div):>9} {dev:15.1e} {tail.std(0).max():14.4f} {np.abs(traj).max():12.2f}")
else:
    LR_CUR = float(sys.argv[2]); T = int(sys.argv[3]) if len(sys.argv) > 3 else 100_000
    traj, div = run(LR_CUR, T)
    tag = f"three_neuron_lr{LR_CUR}"
    np.save(os.path.join(HERE, tag + "_trajectory.npy"), traj)
    dev = max(np.abs(traj[:, 0] - traj[:, 1]).max(), np.abs(traj[:, 3] - traj[:, 4]).max())
    print(f"lr {LR_CUR} T {T}: diverged at {div}, iterates {len(traj)}, max deviation from S = {dev:.1e}")
    cut = len(traj) - 6000 if div else len(traj)
    keep = traj[:max(cut, 1)][::2]
    ep = np.arange(0, max(cut, 1))[::2]
    a, c, b, dd = keep[:, 0], keep[:, 3], keep[:, 2], keep[:, 5]
    for n_, v in zip("a c b d".split(), (a, c, b, dd)):
        print(f"  {n_}: [{v.min():.2f}, {v.max():.2f}]")
    print("plotted points:", len(keep))
    nl = min(10_000, len(traj) - 1)
    lam = lyapunov(traj, nl)
    print(f"Lyapunov (first {nl} steps), 6 exponents:", np.round(lam, 4))
    fig = plt.figure(figsize=(16, 7))
    for k, (z, zl) in enumerate([(b, "third input b"), (dd, "third output d")]):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        p = ax.scatter(a, c, z, c=ep / 1e4, s=0.6, cmap="viridis")
        ax.set_xlabel("pair input a"); ax.set_ylabel("pair output c"); ax.set_zlabel(zl)
        ax.view_init(22, -55)
        fig.colorbar(p, ax=ax, shrink=0.6, label=r"Epoch ($\times10^4$)")
    fig.suptitle(f"3 hidden neurons, start in S (neurons 0,1 identical), lr {LR_CUR}, float64")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, tag + ".png"), dpi=140)
    print("saved", tag + ".png")
