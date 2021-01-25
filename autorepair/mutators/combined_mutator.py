import random
from copy import deepcopy
from debuggingbook.Repairer import StatementMutator, ConditionMutator

class CombinedMutator(StatementMutator):
    """Combines several mutators, that subclass the StatementMutator"""


    def __init__(self, *args, **kwargs):
        """Constructor. Arguments are as with `StatementMutator` constructor."""
        self._mutators = [\
                StatementMutator(*args, **kwargs), \
                ConditionMutator(*args, **kwargs), \
                ]
        super().__init__(*args, **kwargs)
        if self.log:
            print("Initialized combined mutator")

    def mutate(self, tree):
        # randomly choose one of the provided mutators and mutate
        mutator = random.choice(self._mutators)
        return mutator.mutate(tree)
