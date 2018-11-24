import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch import device
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.optim import Optimizer

import random
from collections import deque

from architecture import Arch
from population import Population
from model import Model


def train(model, device, train_loader, optimizer, epoch):
    """
    :type epoch: int
    :type optimizer: Optimizer
    :type train_loader: DataLoader
    :type device: device
    :type model: Model
    """
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()), end=' === ')
            print('with learning rate:', optimizer.param_groups[0]['lr'])


def validate(model, device, test_loader):
    """
    Run the model in validation set, then return the fitness.
    :type device: device
    :type test_loader: DataLoader
    :type model: Model
    """
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    acc = 100. * correct / len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset), acc))

    return acc


def train_and_eval(model):
    EPOCH = 30
    BATCH_SIZE = 128
    learning_rate = 0.01002

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model.to(device)

    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.7)

    kwargs = {'num_workers': 8, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('/MNIST-data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=BATCH_SIZE, shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('/MNIST-data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=BATCH_SIZE, shuffle=True, **kwargs)

    for epoch in range(1, EPOCH + 1):
        train(model, device, train_loader, optimizer, epoch)
        acc = validate(model, device, test_loader)

    return validate(model, device, test_loader)


def random_model():
    dna = Arch.random_arch()
    model = Model(dna)
    return model


class Worker():
    """Used to select, mutate, evolve populations"""

    def __init__(self, population, population_size_setpoint):
        """

        :type population: Population
        """
        self._population_size_setpoint = population_size_setpoint
        self.population = population

    def _population_size(self):
        return len(self.population)

    def select(self):
        """
        Return the available individuals.
        :rtype: DNA
        """
        pass

    def _edge_mutation(self):
        pass

    def _vertex_mutation(self):
        pass

    def mutation(self, dna):
        """
        Return the mutated dna.
        :rtype: DNA
        """
        pass

    def evolve(self):
        total_population_num = self._population_size_setpoint
        cycles = 50
        sample_size = 5

        population = deque()
        history = []
        while len(population) < total_population_num:
            model = random_model()  # type: Model
            model.accuracy = train_and_eval(model)
            population.append(model)
            history.append(model)

        while len(history) < cycles:
            sample = random.sample(population, sample_size)
            parent = max(sample, key=lambda x: x.accuracy)
            child = Model(self.mutation(parent.dna))
            child.accuracy = train_and_eval(child)

            population.append(child)
            history.append(child)
            # reserve best //TODO
            # 轮盘
            population.popleft()

        return max(history, key=lambda x: x.accuracy)


if __name__ == '__main__':
    a = Arch.random_arch()

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model = Model(a.arch, device, 1)
    train_and_eval(model)

    # out = cell(data1, data2)
    # print(out)