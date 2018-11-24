import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

from architecture import Arch


class Model(nn.Module):
    def __init__(self, architecture, device, nor_number=1):
        """

        :type architecture: List
        """
        super(Model, self).__init__()
        self.architecture = architecture
        self.N = nor_number
        self.accuracy = 0
        self.device = device

        channels = [4, 4, 8, 8, 16]
        self.increase_channel = nn.Conv2d(1, channels[0], 3, 1, 1)

        self.cells = nn.ModuleList()
        for i in range(5):
            if i % 2 == 0:  # normal cells
                self.cells.extend([CellModel(self.architecture[0], channels[i]) for _ in range(self.N)])
                # self.add_module()
            else:  # reduction cells
                self.cells.append(nn.Sequential(
                    CellModel(self.architecture[1], channels[i]),
                    nn.Conv2d(channels[i], channels[i + 1], 3, 1, 1),
                    nn.MaxPool2d(2)
                ))

        self.FC1 = nn.Sequential(
            nn.Linear(784, 256),
            nn.LeakyReLU(),
            nn.BatchNorm1d(256)
        )
        self.FC2 = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64)
        )
        self.out = nn.Linear(64, 10)

        # print(self.cells)

    def forward(self, input):
        input = self.increase_channel(input)

        x, y = input, input
        for i, cell in enumerate(self.cells):
            output = cell((x, y))
            x, y = (y, output) if (i + 1) % (self.N + 1) != 0 else (output, output)
            # print(i)
            # print(x.shape, y.shape)

        result = y.view(y.size(0), -1)
        result = self.FC1(result)
        result = self.FC2(result)
        output = self.out(result)

        return output


class Identical(nn.Module):
    def forward(self, x):
        return x


class CellModel(nn.Module):
    def __init__(self, architecture, channel):
        super(CellModel, self).__init__()

        op_dict = {
            'identical': Identical(),
            'sep_3x3': nn.Conv2d(in_channels=channel, out_channels=channel, kernel_size=3,
                                 stride=1, padding=1, dilation=1, groups=channel),  # padding = (k_s - 1) / 2 =
            'sep_5x5': nn.Conv2d(channel, channel, 5, 1, 2, 1, groups=channel),
            'sep_7x7': nn.Conv2d(channel, channel, 7, 1, 3, 1, groups=channel),
            'bn': nn.BatchNorm2d(channel),
            'dil_3x3': nn.Conv2d(channel, channel, 3, 1, 1, dilation=1, groups=1),
            'sep_1x7_7x1': nn.Sequential(
                nn.Conv2d(channel, channel, kernel_size=(1, 7), padding=(0, 3), groups=channel),
                nn.Conv2d(channel, channel, kernel_size=(7, 1), padding=(3, 0), groups=channel)
            ),
        }

        self.archi = architecture
        # print(architecture)
        self.ops = nn.ModuleDict()
        for i, node in enumerate(architecture[0:-1]):
            self.ops[str((i + 2, 0))] = op_dict[node[0]]
            self.ops[str((i + 2, 1))] = op_dict[node[1]]

        # self.ops = [(op_dict['identical'], op_dict['identical']), [(op_dict['identical'], op_dict['identical'])]]
        # self.ops.extend([(op_dict[x[0]], op_dict[x[1]]) for x in architecture[0:-1]])  # 7 OP in total

        self.inputs = [(0, 0), (0, 0)]
        self.inputs.extend([(x[2], x[3]) for x in architecture[0:-1]])
        self.inputs.append(architecture[-1])

        # print(self.inputs)
        #
        # print(self.archi)
        # print(self.ops)
        # print(self.inputs)

    def forward(self, input):
        x, y = input
        output = [x, y, 0, 0, 0, 0, 0]  # at most 7 intermediate output there
        for i in range(2, 7):
            op0, op1 = self.ops[str((i, 0))], self.ops[str((i, 1))]
            index_x, index_y = self.inputs[i]

            x, y = output[index_x], output[index_y]

            # print(x.shape, y.shape)
            # print(op0, op1)
            # print('============\n')

            output[i] = op0(x) + op1(y)

        result = 0
        for last_input in self.inputs[-1]:
            result += output[int(last_input)]

        return result


if __name__ == '__main__':
    arc = Arch.random_arch()
    # cell = CellModel(arc.arch[0], 4)
    #
    # data1 = torch.rand(1, 1, 28, 28)
    # data1 = nn.Conv2d(1, 4, 1)(data1)
    #
    # data2 = torch.rand(1, 1, 28, 28)
    # data2 = nn.Conv2d(1, 4, 1)(data2)
    #
    # result = cell((data1, data2))

    model = Model(arc.arch, 2)
    print(model)
