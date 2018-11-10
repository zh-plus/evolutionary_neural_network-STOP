from architecture import *
from mutation import *
from worker import *
from population import Population

def show(architecture):
    for i, n in enumerate(architecture.arch):
        print(i)
        print('type:', n.type)
        for nn in n.nodes:
            print('left: ', nn.left_edge.op if nn.left_edge else '', nn.left_edge.enter_node if nn.left_edge else '')
            print('right: ', nn.right_edge.op if nn.right_edge else '', nn.right_edge.enter_node if nn.right_edge else '')
            print('out', nn.out)
            if nn.type == 2:
                print('final in', end=' ')
                for x in nn.out_enter_edge:
                    print(x)

            print('-------------------------')

        print('\n------------------------------------------\n')

test_arch = random_architecture()
show(test_arch)

mutation = OpMutation()
mutation.mutate(test_arch)
show(test_arch)



# # model = Model(test_arch)
#
# fitness = train_and_eval(model)
# print(fitness)

