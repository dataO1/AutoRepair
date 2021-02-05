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
        self.load = []
        self.store = []

    def visit_Name(self, node):
        if isinstance(node.ctx,ast.Load)==True:
            self.load.append(node)
        if isinstance(node.ctx,ast.Store)==True:
            self.store.append(node)

        return super().generic_visit(node)

    # ignore func name in call, but get arguments
    #  def visit_Call(self, node):
        #  for arg in node.args:
            #  super().generic_visit(arg)
        #  return node


class AllMightyVisitor(NodeVisitor):
    def __init__(self):
        self.conditions = []
        self.conditions_seen = set()
        self.definitions = []
        self.definitions_seen = set()
        super().__init__()

    def add_to(self,target_str, node, attr=None):
        """ add the attribute of a node to the target list of seen attributes """
        target = getattr(self, target_str)
        target_seen = getattr(self, target_str + "_seen")

        if attr:
            elems = getattr(node, attr, [])
        else:
            elems = node
        if not isinstance(elems, list):
            elems = [elems]
        for elem in elems:
            elem_str = astor.to_source(elem)
            if elem_str not in target_seen:
                target.append(elem)
                target_seen.add(elem_str)

    def visit_FunctionDef(self, node):
        self.add_to('definitions', node)
        return super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.visit_FunctionDef(node)

    def visit_BoolOp(self, node):
        self.add_to('conditions', node, 'values')
        return super().generic_visit(node)

    def visit_Name(self, node):
        self.add_to('definitions', node)

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

    def _mark_parents(self, root):
        for node in ast.walk(root):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                #  if  not type(child) in (int, float, bool, str):
                self._mark_parents(child)
        return node

    def _get_child_attr_name(self, parent, child):
        for _child in dir(parent):
            if getattr(parent,_child) is child:
                return _child

    def _setattr(self, node, target, expr):
        self._mark_parents(node)
        attr = self._get_child_attr_name(target.parent, target)
        #  print(attr)
        if(attr):
            setattr(target.parent, attr, expr)

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
        swap_func_name = "swap_" + rand.choice(['condition',
            'one_off_error','two_occurrences', 'operator',
            'definition_and_occurrences'])
        swap_func = getattr(self, swap_func_name)
        return swap_func(node)
        #  return self.swap_condition(node)

    def swap_condition(self, node):
        return ConditionMutator.swap(self, node)


    #  def swap_new_name(self, node):
        #  node = deepcopy(node)
        #  visitor = NameVisitor()
        #  visitor.visit(node)
        #  names = visitor.names
        #  #  print(names)
        #  if not names:
            #  return super().swap(node)
        #  # choose a random name from definitions to swap
        #  target = rand.choice(names)
        #  #  new_name = rand.choice(self.definitions).id + "_autofixed"
        #  new_name = "laskdfjlaskjf"
        #  target.id = new_name
        #  return node

    def swap_definition_and_occurrences(self, node):
        node = deepcopy(node)
        visitor = NameVisitor()
        visitor.visit(node)
        store = visitor.store
        load = visitor.load
        if not store or (len(load)<1):
            return self.swap(node)
        # get first definition in node
        store_target = store[0] # take the first, not random
        # filter out all occurrences of same name as store_target
        load_targets = [name for name in load if name.id == store_target.id]
        #  print(names)
        new_id = "fixed_by_autorepair_var"
        store_target.id = new_id
        for load_target in load_targets:
            load_target.id = new_id
        return node

    def swap_two_occurrences(self, node):
        #  if isinstance(node, ast.Return):
            #  return self.swap(node)
        node = deepcopy(node)
        #  # get all names, with ctx Load
        visitor = NameVisitor()
        visitor.visit(node)
        names = visitor.load
        #  #  print(names)
        #  #  print("COLLECTED ALL NAMES")
        if not names or len(names) < 2:
            return self.swap(node)
        #  print("before:")
        #  print( astor.to_source(node))
        #  print(f"names:{[name.id for name in names]}")
        target1 = rand.choice(names)
        target2 = rand.choice(names)
        # as long as drawing the same name redraw
        while (target1.id == target2.id):
            target2 = rand.choice(names)
        # swap the two names in the node
        h = deepcopy(target1.id)
        target1.id = target2.id
        target2.id = h
        #  print("after:")
        #  print( astor.to_source(node))
        return node

    def swap_one_off_error(self, node):
        node = deepcopy(node)
        # get all names, with ctx Load
        visitor = NameVisitor()
        visitor.visit(node)
        names = visitor.load
        if not names:
            return self.swap(node)
        # choose a random name from definitions to increment or decrement
        target = rand.choice(names)
        target_id = target.id
        expr = rand.choice(["n+1","n-1"])
        expr = ast.parse(expr).body[0].value
        expr.left.id = target_id
        # now exchange n with the chosen name and replace name with that
        self._setattr(node, target, expr)
        return node

    def swap_operator(self, node):
        node = deepcopy(node)
        visitor = OperatorVisitor()
        visitor.visit(node)
        operators = visitor.operators
        if not operators:
            return self.swap(node)
        # choose a random operator to swap
        target = rand.choice(operators)
        operators = [ast.Add, ast.Mult, ast.Div]
        target.op = rand.choice(operators)()
        return node
