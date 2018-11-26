from mutation import *
import random


test_arch = Arch.random_arch()
for i, n in enumerate(test_arch.arch):
    print(i)
    print(n)
    print('\n----\n')
print('------------------------')
mutations = [Mutation.hidenStateMutate, Mutation.opMutate]
mutation = random.choice(mutations)
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

