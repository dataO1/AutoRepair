import random
import ast
import copy
from copy import deepcopy
from debuggingbook.Repairer import StatementMutator, ConditionMutator

class NameMutator(StatementMutator):
    """Mutate variable names into other variable names present in the program"""

    def __init__(self, *args, **kwargs):
        """Constructor. Arguments are as with `StatementMutator` constructor."""
        super().__init__(*args, **kwargs)
        if self.log:
            print("Initialized NameMutator")

    #  def mutate(self, tree):
        #  # randomly choose one of the provided mutators and mutate
        #  mutator = random.choice(self._mutators)
        #  tree = mutator.mutate(tree)
        #  #  print(tree)
        #  return tree
