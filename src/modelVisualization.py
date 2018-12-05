from model import Model
from architecture import Arch
from torchviz import make_dot, make_dot_from_trace
import torch
import torch.nn as nn


a = Arch.random_arch()
print("training", a.id)
model = Model(a, 1)
print(model)

data = torch.rand(128, 1, 28, 28)

with torch.onnx.set_training(model, False):
    trace, _ = torch.jit.get_trace_graph(model, args=(data,))


dot = make_dot_from_trace(trace)
dot.format = 'png'
dot.render()
