"""Same 8 points, full-batch GD, start on P+ (identical neurons). Vary only the learning rate."""
import math, torch
from tiny_net import TinyNet

torch.manual_seed(0)
x = torch.randn(8, 1); y = torch.randn(8, 1)

def run(lr, steps=20000):
    net = TinyNet()
    with torch.no_grad():
        net.w1.copy_(torch.tensor([0.7, 0.7]))     # identical neurons
        net.w2.copy_(torch.tensor([0.9, 0.9]))
    path, losses = [], []
    for _ in range(steps):
        loss = ((net(x) - y) ** 2).mean()
        net.zero_grad(); loss.backward()
        with torch.no_grad():
            for p in net.parameters(): p -= lr * p.grad
        path.append((net.w1[0].item(), net.w2[0].item())); losses.append(loss.item())
    return path, losses

print(f"{'lr':>6} | {'loss last':>9} | {'loss std (last 2000)':>20} | {'mean jump (last 2000)':>21} | {'x range (last 2000)':>19}")
for lr in [0.05, 0.3, 1.0, 2.0, 2.5, 3.0]:
    p, l = run(lr)
    if not math.isfinite(l[-1]) or l[-1] > 1e6:
        print(f"{lr:>6} | diverged"); continue
    t = torch.tensor(p[-2000:]); L = torch.tensor(l[-2000:])
    jump = (t[1:] - t[:-1]).norm(dim=1).mean().item()
    xr = (t[:, 0].max() - t[:, 0].min()).item()
    print(f"{lr:>6} | {l[-1]:9.4f} | {L.std().item():20.6f} | {jump:21.6f} | {xr:19.4f}")
