import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch import device
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from tensorboardX import SummaryWriter

from time import perf_counter

from model import Model
from architecture import Arch


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
        # if batch_idx % 100 == 0:
        # print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        #    epoch, batch_idx * len(data), len(train_loader.dataset),
        #           100. * batch_idx / len(train_loader), loss.item()), end=' === ')
        # print('with learning rate:', optimizer.param_groups[0]['lr'])


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
    # print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
    #    test_loss, correct, len(test_loader.dataset), acc))

    return acc


def train_and_eval(model):
    start = perf_counter()

    EPOCH = 3
    BATCH_SIZE = 128
    learning_rate = 0.01002

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model.to(device)

    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.7)

    kwargs = {'num_workers': 8, 'pin_memory': True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('MNIST-data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=BATCH_SIZE, shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('MNIST-data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=BATCH_SIZE, shuffle=True, **kwargs)

    for epoch in range(1, EPOCH + 1):
        train(model, device, train_loader, optimizer, epoch)
        # acc = validate(model, device, test_loader)

    elapse = perf_counter() - start
    print('elapse: {}\t'.format(elapse), end='')

    return validate(model, device, test_loader)

def visualize(model):
    dummy_data = torch.rand(1, 2, 28, 28)

    with SummaryWriter(comment='chosen model') as writer:
        writer.add_graph(model, ((dummy_data, dummy_data), ))


if __name__ == "__main__":
    from architecture import Arch
    from model import CellModel
    import sys
    import platform


    print(sys.version_info)

    a = Arch.random_arch().arch
    cell = CellModel(a[0], 2)
    
    visualize(cell)