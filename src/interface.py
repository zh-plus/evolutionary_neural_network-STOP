from copy import copy
import worker
from mutation import Mutation
from population import *


C = 30
S = 1
print("Welcome to auto-ML!")
# deal with path
# last_path = load_path()
config = load_config()
response = None
gen_num = config['gen_num']
if config["path"] != '':
    print("Notice the last visited path is: ", config["path"])
    while response not in ('y', 'n'):
        response = input("Do you want to use that?(y/n): ").lower()
    if response == 'y':
        last_path = test_dir(config["path"])
if response == 'n' or config["path"] == '' or response is None:
    last_path = input("Please choose a new path: ")
    last_path = test_dir(last_path)

folder = Folder(config["path"])
p = Population(folder)

# train initial individuals
for i in range(0, p.__len__()):
    if p.individuals[i].accuracy == 0:
        a = p.individuals[i]
        acc = worker.test(a)
        p.individuals[i].accuracy = acc
        a.accuracy = acc
        print("train", folder.file_name(p.individuals[i]), "to", acc)
        folder.create_file(a.to_proto())

# begin evolution
while folder.history.__len__() < C:
    print("This is", folder.history.__len__()-p.__len__()+1, " cycle:")
    sample = random.sample(range(p.__len__()), k=S)

    parent = Arch()
    for s in sample:
        if p.individuals[s].accuracy > parent.accuracy:
            parent = copy(p.individuals[s])
    child = copy(parent)
    # mutation
    Mutation.hidenStateMutate(child)
    acc = worker.test(child)
    child.accuracy = acc
    print("train child to", acc)
    p.add(child)
    p.dead()

