from random import Random
import random
import ast
from ast import NodeVisitor
import astor
import copy
from copy import deepcopy
from debuggingbook.Repairer import StatementMutator, ConditionMutator

rand = Random()
rand.seed(42)

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
    definitions = visitor.definitions
    if tp is not None:
        conditions = [c for c in conditions if isinstance(c, tp)]
        definitions = [c for c in definitions if isinstance(c, tp)]

    return conditions, definitions

class OperatorVisitor(NodeVisitor):

    def __init__(self):
        self.operators = []

    def visit_BinOp(self, node):
        self.operators.append(node)
        return super().generic_visit(node)

    def visit_AugAssign(self, node):
        return self.visit_BinOp(node)

class NameVisitor(NodeVisitor):

    def __init__(self):
        self.names = []

    # TODO: group all names in the same context, so we can substitute each of
    # them or just one at a time


class AllMightyVisitor(NodeVisitor):
    def __init__(self):
        self.conditions = []
        self.conditions_seen = set()
        self.definitions = []
        self.definitions_seen = set()
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
                target.append(elem)
                target_seen.add(elem_str)

    def visit_FunctionDef(self, node):
        self.add_to('definitions', node, 'name')
        return super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.visit_FunctionDef(node)

    def visit_BoolOp(self, node):
        self.add_to('conditions', node, 'values')
        return super().generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            self.add_to('definitions', target, 'name')

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
        self.conditions, self.definitions = get_all_mutation_sources(self.source)

    def choose_condition(self):
        """Return a random condition from source."""
        return copy.deepcopy(random.choice(self.conditions))

    def choose_name(self):
        """ Return a random name from source. """
        return copy.deepcopy(random.choice(self.names))

    def choose_bool_op(self):
        return random.choice(['set', 'not', 'and', 'or'])

    def swap(self, node):
        # i dont know why, but i need another random instance or things stop
        # working
        swap_func_name = "swap_" + rand.choice(['condition', 'operator' ])
        swap_func = getattr(self, swap_func_name)
        return swap_func(node)
        #  return self.swap_condition(node)

    def swap_condition(self, node):
        return ConditionMutator.swap(self, node)

    def swap_name(self, node):
        node = deepcopy(node)
        visitor = NameVisitor()
        visitor.visit(node)
        names = visitor.names
        if not names:
            return super().swap(node)
        # choose a random name from definitions to swap
        target = rand.choice(names)
        target.name = rand.choice(self.definitions)
        return node

    def swap_operator(self, node):
        node = deepcopy(node)
        visitor = OperatorVisitor()
        visitor.visit(node)
        operators = visitor.operators
        if not operators:
            return super().swap(node)
        # choose a random operator to swap
        target = rand.choice(operators)
        operators = [ast.Add ,ast.Mult]
        target.op = rand.choice(operators)()
        return node
