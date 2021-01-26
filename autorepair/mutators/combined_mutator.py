import random
import ast
import copy
from copy import deepcopy
from debuggingbook.Repairer import StatementMutator, ConditionMutator

class CombinedMutator(StatementMutator):
    """Combines several mutators, that subclass the StatementMutator"""


    def __init__(self, *args, **kwargs):
        """Constructor. Arguments are as with `StatementMutator` constructor."""
        self._mutators = [\
                #  StatementMutator(*args, **kwargs), \
                ConditionMutator(*args, **kwargs), \
                ]
        super().__init__(*args, **kwargs)
        if self.log:
            print("Initialized combined mutator")

    def mutate(self, tree):
        # randomly choose one of the provided mutators and mutate
        mutator = random.choice(self._mutators)
        tree = mutator.mutate(tree)
        print(tree)
        return tree


    #  def mutate(self, tree):
        #  """Mutate the given AST `tree` in place. Return mutated tree."""

        #  assert isinstance(tree, ast.AST)

        #  tree = copy.deepcopy(tree)

        #  if not self.source:
            #  self.source = all_statements(tree)

        #  for node in ast.walk(tree):
            #  node.mutate_me = False

        #  node = self.node_to_be_mutated(tree)
        #  node.mutate_me = True

        #  self.mutations = 0

        #  tree = self.visit(tree)

        #  if self.mutations == 0:
            #  warnings.warn("No mutations found")

        #  ast.fix_missing_locations(tree)
        #  return tree
