"""Interactive (rotatable) 3D plot of the saved three-neuron trajectory. Writes a standalone HTML file.
usage: python three_neuron_interactive.py [LR]   (default 3.5)"""
import os, sys
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = os.path.dirname(os.path.abspath(__file__))
lr = sys.argv[1] if len(sys.argv) > 1 else "3.5"
tag = f"three_neuron_lr{lr}"
traj = np.load(os.path.join(HERE, tag + "_trajectory.npy"))
cut = len(traj) - 6000                      # same as the static plot: drop last 6000, every 2nd iterate
keep = traj[:cut][::2]
ep = np.arange(0, cut)[::2] / 1e4
a, c, b, d = keep[:, 0], keep[:, 3], keep[:, 2], keep[:, 5]

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "scene"}]],
                    subplot_titles=("(a, c, b): pair input, pair output, third input",
                                    "(a, c, d): pair input, pair output, third output"))
for col, (z, zn) in enumerate([(b, "third input b"), (d, "third output d")], 1):
    fig.add_trace(go.Scatter3d(x=a, y=c, z=z, mode="markers",
                               marker=dict(size=1.5, color=ep, colorscale="Viridis", opacity=0.7,
                                           colorbar=dict(title="Epoch (x1e4)", x=0.46 if col == 1 else 1.0, len=0.6) ),
                               hovertemplate="a=%{x:.3f}<br>c=%{y:.3f}<br>z=%{z:.3f}<extra></extra>"), row=1, col=col)
    fig.update_scenes(dict(xaxis_title="pair input a", yaxis_title="pair output c", zaxis_title=zn), row=1, col=col)
fig.update_layout(title=f"3 hidden neurons, lr {lr}, float64 (drag to rotate, scroll to zoom)",
                  height=700, margin=dict(l=0, r=0, t=70, b=0))
out = os.path.join(HERE, tag + "_interactive.html")
fig.write_html(out, include_plotlyjs=True)
print("saved", out, f"({os.path.getsize(out)/1e6:.1f} MB, {len(keep)} points)")
