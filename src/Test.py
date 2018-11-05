from dna import DNA
from mutation import *
from worker import *
from population import Population


dna = DNA()
# simple mutation to dna TODO

model = Model(dna)

fitness = train_and_eval(model)
print(fitness)
