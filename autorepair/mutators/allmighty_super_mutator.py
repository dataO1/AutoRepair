from random import Random
import random
import ast
from ast import NodeVisitor
import astor
import copy
from copy import deepcopy
from debuggingbook.Repairer import StatementMutator, ConditionMutator

def get_all_mutation_sources(trees, tp=None):
    """Return all conditions from the AST (or AST list) `trees`.
    If `tp` is given, return only elements of that type."""
    if not isinstance(trees, list):
        assert isinstance(trees, ast.AST)
        trees = [trees]

    visitor = AllMightyVisitor()
    for tree in trees:
        visitor.visit(tree)
    conditions = visitor.conditions
    if tp is not None:
        conditions = [c for c in conditions if isinstance(c, tp)]

    return conditions

class AllMightyVisitor(NodeVisitor):
    def __init__(self):
        self.conditions = []
        self.conditions_seen = set()
        self.definitions = []
        self.definitions_seen = set()
        self.names = []
        self.names_seen = set()
        super().__init__()

    def add_to(self,target_str, node, attr):
        """ add the attribute of a node to the target list of seen attributes """
        target = getattr(self, target_str)
        target_seen = getattr(self, target_str + "_seen")

        elems = getattr(node, attr, [])
        if not isinstance(elems, list):
            elems = [elems]
        for elem in elems:
            elem_str = astor.to_source(elem)
            if elem_str not in target_seen:
                self.conditions.append(elem)
                self.conditions_seen.add(elem_str)

    def visit_FunctionDef(self, node):
        self.add_to('definitions', node, 'name')
        return super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Class(self, node):
        self.visit_FunctionDef(node)

    def visit_BoolOp(self, node):
        self.add_to('conditions', node, 'values')
        return super().generic_visit(node)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            self.add_to('conditions', node, 'operand')
        return super().generic_visit(node)

    def generic_visit(self, node):
        if hasattr(node, 'test'):
            self.add_to('conditions', node, 'test')
        return super().generic_visit(node)

class AllMightySuperMutator(ConditionMutator):
    """Mutate all kinds of stuff in an AST"""

    def __init__(self, *args, **kwargs):
        """Constructor. Arguments are as with `StatementMutator` constructor."""
        super().__init__(*args, **kwargs)
        self.rand = Random()
        self.rand.seed(42)
        self.conditions = get_all_mutation_sources(self.source)
        if self.log:
            print("Found conditions",
                  [astor.to_source(cond).strip() 
                   for cond in self.conditions])

    def choose_condition(self):
        """Return a random condition from source."""
        return copy.deepcopy(random.choice(self.conditions))

    def choose_bool_op(self):
        return random.choice(['set', 'not', 'and', 'or'])

    def swap(self, node):
        # i dont know why, but i need another random instance or things stop
        # working
        swap_func_name = "swap_" + self.rand.choice(['condition'])
        swap_func = getattr(self, swap_func_name)
        return swap_func(node)
        #  return self.swap_condition(node)

    def swap_condition(self, node):
        return ConditionMutator.swap(self, node)

    def swap_name(self, node):
        raise Exception("TODO: Implement")

    def swap_operator(self, node):
        raise Exception("TODO: Implement")
