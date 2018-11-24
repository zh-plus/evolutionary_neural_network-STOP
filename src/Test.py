from architecture import *
from mutation import *

test_arch = Arch.random_arch()

for i, n in enumerate(test_arch.arch):
    print(i)
    print(n)
    print('\n----\n')
print('------------------------')
mutation = random.choice([Mutation.hidenStateMutate, Mutation.opMutate])
mutation(test_arch)
print('after mutation')
print('--------------------------\n')
for i, n in enumerate(test_arch.arch):
    print(i)
    print(n)
    print('\n----\n')

# # model = Model(test_arch)
#
# fitness = train_and_eval(model)
# print(fitness)
