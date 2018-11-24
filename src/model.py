import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

from architecture import Arch


# class Model(nn.Module):
#     def __init__(self, architecture):
#         """
#
#         :type architecture: List
#         """
#         super(Model, self).__init__()
#         self.architecture = architecture
#         self.accuracy = 0
#         cell_codes = []
#         # construct this nn model according to the DNA
#
#         for i in range(5):
#             network.append(cell)  # normal cell
#         network.append(reduction_cell)
#         for i in range(5):
#
#         self.network = nn.Sequential(*network)
#
#         cell = []
#         [sep3x3, ]
#         for block in cell:  # c b
#             self.oper1_1_1 = nn.Conv2d
#             self.oper1_1_2 = nn.Conv2d
#
#         self.sep3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=0, dilation=1, groups=64)
#         self.sep5 = nn.Conv2d(64, 64, 5, 1, 0, 1, groups=64)
#         self.sep7 = nn.Conv2d(64, 64, 7, 1, 0, 1, groups=64)
#
#         self.avg_pool = nn.AvgPool2d(3)
#
#         # for
#
#     def forward(self, x):  # (1, 28, 28)
#         i, j =
#         i = block1[3]
#         y1 = self.oper1_1_1(x[i])
#         i = block1[4]
#         y2 = self.oper1_1_2(x[j])
#         x.append(y1 + y2)
#         i = block2[3]
#         y1 = self.oper1_2_1(x[i])
#         i = block1[4]
#         y2 = self.oper1_2_2(x[i])
#         x.append(y1 + y2)
#
#         y1 = self.sep3(x)
#         y2 = self.sep5(x)
#         y3 = self.sep7(x)
#         y4 = self.avg_pool(x)
#         return x7, x
#
#         # for cell in self.architecture.arch:
#
#         # return output


class CellModel(nn.Module):
    def __init__(self, architecture, channels):
        super(CellModel, self).__init__()

        op_dict = {
            'identical': lambda x: x,
            'sep_3x3': nn.Conv2d(in_channels=channels, out_channels=channels, kernel_size=3,
                                 stride=1, padding=1, dilation=1, groups=channels),  # padding = (k_s - 1) / 2 =
            'sep_5x5': nn.Conv2d(channels, channels, 5, 1, 2, 1, channels),
            'sep_7x7': nn.Conv2d(channels, channels, 7, 1, 3, 1, channels),
            'avg_3x3': nn.AvgPool2d(2),
            'max_3x3': nn.MaxPool2d(2),
            'dil_3x3': nn.Conv2d(channels, channels, 3, 1, 1, dilation=1, groups=1),
            'sep_1x7_7x1': nn.Sequential(
                nn.Conv2d(channels, channels, kernel_size=(1, 7), padding=(0, 3), groups=channels),
                nn.Conv2d(channels, channels, kernel_size=(7, 1), padding=(3, 0), groups=channels)
            ),
        }

        self.archi = architecture

        self.ops = [(op_dict['identical'], op_dict['identical']), [(op_dict['identical'], op_dict['identical'])]]
        self.ops.extend([(op_dict[x[0]], op_dict[x[1]]) for x in architecture[2:-1]])  # 7 OP in total

        self.inputs = [(0, 0), (0, 0)]
        self.inputs.extend([(x[2], x[3]) for x in architecture[2:-1]])
        self.inputs.append(architecture[-1])

        print(self.archi)
        print(self.ops)
        print(self.inputs)

    def forward(self, x, y):
        output = [x, y, 0, 0, 0, 0, 0]  # at most 7 intermediate output there
        for i in range(2, 7):
            operations = self.ops[i]
            index_x, index_y = self.inputs[i]
            x, y = output[index_x], output[index_y]

            # assert x != 0 or y != 0

            print('x:', x.shape, 'y:', y.shape)

            print(operations[0], operations[1])
            output[i] = operations[0](x) + operations[1](y)

        result = 0
        for last_input in self.inputs[-1]:
            result += output[last_input]

        return result


if __name__ == '__main__':
    a = Arch.random_arch()
    cell = CellModel(a.arch[0], 16)

    data1 = torch.rand(1, 1, 28, 28)
    data1 = nn.Conv2d(1, 16, 1)(data1)

    data2 = torch.rand(1, 1, 28, 28)
    data2 = nn.Conv2d(1, 16, 1)(data2)

    cell.forward(data1, data2)

    # out = cell(data1, data2)
    # print(out)
