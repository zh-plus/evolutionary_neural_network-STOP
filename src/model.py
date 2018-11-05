import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

from dna import DNA


class Model(nn.Module):
    def __init__(self, DNA):
        super(Model, self).__init__()
        self.DNA = DNA
        self.accuracy = 0
        # construct this nn model according to the DNA

    def forward(self, x):
        pass
        # return output
