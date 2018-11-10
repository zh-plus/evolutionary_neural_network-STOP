import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

from architecture import Architecture

class sep3x3():


class Model(nn.Module):
    def __init__(self, architecture):
        super(Model, self).__init__()
        self.architecture = architecture
        self.accuracy = 0
        cell_codes = []
        # construct this nn model according to the DNA

        cell = []
        [sep3x3, ]
        for block in cell:      # c b
            self.oper1_1_1 = nn.Conv2d
            self.oper1_1_2 = nn.Conv2d



        self.sep3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=0, dilation=1, groups=64)
        self.sep5 = nn.Conv2d(64, 64, 5, 1, 0, 1, groups=64)
        self.sep7 = nn.Conv2d(64, 64, 7, 1, 0, 1, groups=64)

        self.avg_pool = nn.AvgPool2d(3)

        # for

    def forward(self, x):   # (1, 28, 28)
        i, j =
        i = block1[3]
        y1 = self.oper1_1_1(x[i])
        i = block1[4]
        y2 = self.oper1_1_2(x[j])
        x.append(y1+y2)
        i = block2[3]
        y1 = self.oper1_2_1(x[i])
        i = block1[4]
        y2 = self.oper1_2_2(x[i])
        x.append(y1+y2)




        y1 = self.sep3(x)
        y2 = self.sep5(x)
        y3 = self.sep7(x)
        y4 = self.avg_pool(x)
        return x7, x

        # for cell in self.architecture.arch:

        # return output

class network
    network = []
    self.cell1 = cell

    for i in range(5):
        network.append(cell) # normal cell
    network.append(reduction_cell)
    for i in range(5):

    self.network = nn.Sequential(*network)

    def forward(self, x):
        x = self
        y = self.network(x)

