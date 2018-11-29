import matplotlib.pyplot as plt
import numpy as np
from architecture import Arch
from file_system import load_path, test_dir, Folder, read_file

print("Welcome to analysis system!")
# deal with path
last_path = load_path()
response = None
if last_path != '':
    print("Notice the last store path is: ", last_path)
    while response not in ('y', 'n'):
        response = input("Do you want to use that?(y/n): ").lower()
    if response == 'y':
        last_path = test_dir(last_path)
if response == 'n' or last_path == '' or response is None:
    last_path = input("Please choose a new store path: ")
    last_path = test_dir(last_path)

last_path = test_dir(last_path)
folder = Folder(last_path)
data = np.zeros(folder.max_id)
best = []

for file in folder.history:
    # alive file
    if not folder.alive(file):
        dead_file_path = folder.dead_file_path(file)
        arch_proto = read_file(dead_file_path)
        arch = Arch(arch_proto)
        data[arch.id-1] = arch.accuracy

    # dead file
    else:
        file_path = folder.file_path(file)
        arch_proto = read_file(file_path)
        arch = Arch(arch_proto)
        # add it to population
        data[arch.id-1] = arch.accuracy


for arch in data:
    good = 0
    if best:
        good = best[-1]
    if arch > good:
        best.append(arch)
    else:
        best.append(good)


print("data", data)
x_values = list(range(1, data.__len__()+1))
y_values = [data[x-1] for x in x_values]
plt.figure()
plt.scatter(x_values, y_values, s=1)
plt.ylim((95, 100))
plt.xlabel('generation')
plt.ylabel('accuracy')
plt.show()


# best individual curve
print("best",best)
x_values = list(range(1, data.__len__()+1))
y_values = [best[x-1] for x in x_values]
plt.figure()
plt.plot(x_values, y_values)
plt.ylim((95, 100))
plt.xlabel('generation')
plt.ylabel('accuracy of best')
plt.show()
print("data:",data)

interval = []
cnt = 0
acc = 0
len = 9

for i in range(0, folder.max_id):
    if cnt < len:
        acc += data[i]
        cnt += 1
    else:
        interval.append(acc/cnt)
        cnt = 0
        acc = 0
if cnt > 0 and acc > 0:
    interval.append(acc / cnt)
    cnt = 0
    acc = 0



print("interval",interval)
x_values = list(range(len+1, folder.max_id+len, len+1))
print(x_values)
y_values = [interval[int(x/(len+1))-1] for x in x_values]
plt.figure()
plt.plot(x_values, y_values)
plt.ylim((80, 100))
plt.xlabel('generation')
plt.ylabel('average accuracy')
plt.show()


"""
f = open("Store/output.txt", "r")
line = f.readline()
while line:             #直到读取完文件
    line = f.readline()  #读取一行文件，包括换行符
    line = line[:-1]     #去掉换行符，也可以不去
line = f.readline()
while line:             #直到读取完文件
    line = f.readline()  #读取一行文件，包括换行符
    line = line[:-1]     #去掉换行符，也可以不去
    a = line.split()
    if a and a[0] == 'elapse:':
        acc = float(a[5])
        data.append(acc)
        good = 0
        if best:
            good = best[-1]
        if acc > good:
            best.append(acc)
        else:
            best.append(good)

f.close()
"""