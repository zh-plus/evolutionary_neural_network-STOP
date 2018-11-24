import random
from copy import copy
from population import *


def mutation(arch: Arch):
    mutate = random.uniform(-10, 10)
    print("mutate", folder.file_name(arch), "from", arch.accuracy, "to", arch.accuracy+mutate)
    arch.accuracy += mutate
    return arch


C = 30
S = 5
print("Welcome to auto-ML!")
# deal with path
last_path = load_path()
response = None
if last_path != '':
    print("Notice the last visited path is: ", last_path)
    while response not in ('y', 'n'):
        response = input("Do you want to use that?(y/n): ").lower()
    if response == 'y':
        last_path = test_dir(last_path)
if response == 'n' or last_path == '' or response is None:
    last_path = input("Please choose a new path: ")
    last_path = test_dir(last_path)

folder = Folder(last_path)
p = Population(folder)

for i in range(0, p.__len__()):
    if p.individuals[i].accuracy == 0:
        a = random.randint(0, 20)
        print("random", folder.file_name(p.individuals[i]), "to", a)
        p.individuals[i].accuracy = a

while folder.history.__len__() < C:
    print("This is", folder.history.__len__()-p.__len__()+1, " cycle:")
    sample = random.sample(range(p.__len__()), k=S)

    parent = Arch()
    for s in sample:
        if p.individuals[s].accuracy > parent.accuracy:
            parent = copy(p.individuals[s])
    copy_parent = copy(parent)
    child = mutation(copy_parent)
    p.add(child)
    p.dead()

