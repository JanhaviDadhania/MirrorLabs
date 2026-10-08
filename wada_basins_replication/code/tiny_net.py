"""The paper's minimal model: 1 input -> 2 hidden tanh neurons -> 1 output.
4 weights in total, no biases. (Ly & Gong, arXiv 2510.05606, Eq. 3)"""
import math
import torch
import torch.nn as nn


class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.w1 = nn.Parameter(torch.randn(2))   # input weights : neuron 1, neuron 2
        self.w2 = nn.Parameter(torch.randn(2))   # output weights: neuron 1, neuron 2
        self.a1 = math.sqrt(2)                   # fixed scale on layer 1
        self.a2 = 0.5                            # fixed scale on layer 2

    def forward(self, x):                        # x: (N, 1)
        h = torch.tanh(self.a1 * x * self.w1)    # (N, 2)  one column per hidden neuron
        return self.a2 * (h * self.w2).sum(dim=1, keepdim=True)   # (N, 1)


if __name__ == "__main__":
    torch.manual_seed(0)
    x = torch.randn(8, 1)                        # 8 inputs, one number each
    y = torch.randn(8, 1)                        # 8 targets, one number each
    net = TinyNet()
    print("x", tuple(x.shape), " out", tuple(net(x).shape))
    print("weights:", [p.numel() for p in net.parameters()], "-> 4 total")
    print("loss:", ((net(x) - y) ** 2).mean().item())
