from test.factorial1 import factorial1, factorial1_test
from test.factorial1 import get_tests as get_tests_factorial1
from test.factorial2 import factorial2, factorial2_test
from test.factorial2 import get_tests as get_tests_factorial2
from test.factorial3 import factorial3, factorial3_test
from test.factorial3 import get_tests as get_tests_factorial3
from test.middle import get_tests as get_tests_middle
from test.middle import middle, middle_assert, middle_test
from test.power import get_tests as get_tests_power
from test.power import power, power_test

from autorepair.mutators.allmighty_super_mutator import AllMightySuperMutator
from debuggingbook.StatisticalDebugger import OchiaiDebugger
from debuggingbook.Repairer import Repairer, ConditionMutator, CrossoverOperator
from debuggingbook.DeltaDebugger import DeltaDebugger

import astor

def debug_and_repair(f, testcases, function_test, 
                            log=False):
    '''
    Debugs a function with the given testcases and the test_function
    and tries to repair it afterwards.

    Parameters
    ----------
    f : function
        The faulty function, to be debugged and repaired
    testcases : List
        A list that includes test inputs for the function under test
    test_function : function
        A function, that takes the test inputs and tests whether the
        function under test produces the correct output.
    log: bool
        Turn logging on/off.
    Returns
    -------
    str
        The repaired version of f as a string.
    '''

    debugger = OchiaiDebugger()

    for i in testcases:
        with debugger:
            function_test(*i)  # Ensure that you use *i here.

    repairer = Repairer(debugger,
                        mutator_class=AllMightySuperMutator,
                        crossover_class=CrossoverOperator,
                        reducer_class=DeltaDebugger,
                        log=log)

    # Ensure that you specify a sufficient number of
    # iterations to evolve.
    best_tree, fitness = repairer.repair(iterations=100)

    return astor.to_source(best_tree)
