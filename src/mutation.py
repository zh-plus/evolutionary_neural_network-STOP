import copy


class Mutation(object):
    def mutate(self, dna):
        pass


class AlterLearningRateMutation(Mutation):
    def mutate(self, dna):
        mutaed_dna = copy.deepcopy(dna)
        # TODO


class AddEdgeMutation(Mutation):
    def mutate(self, dna):
        pass


class AddVertexMutation(Mutation):
    def mutate(self, dna):
        pass
