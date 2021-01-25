from debuggingbook.StatisticalDebugger import OchiaiDebugger
from debuggingbook.Repairer import Repairer, ConditionMutator, CrossoverOperator
from debuggingbook.DeltaDebugger import DeltaDebugger

def simple_debug_and_repair(f, testcases, function_test, 
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
                        mutator_class=ConditionMutator,
                        crossover_class=CrossoverOperator,
                        reducer_class=DeltaDebugger,
                        log=log)

    # Ensure that you specify a sufficient number of
    # iterations to evolve.
    best_tree, fitness = repairer.repair(iterations=100)

    return astor.to_source(best_tree)
