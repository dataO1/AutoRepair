import math
import random
import re

from .factorial1 import factorial1, factorial1_test
from .factorial1 import get_tests as get_tests_factorial1
from .factorial2 import factorial2, factorial2_test
from .factorial2 import get_tests as get_tests_factorial2
from .factorial3 import factorial3, factorial3_test
from .factorial3 import get_tests as get_tests_factorial3
from .middle import get_tests as get_tests_middle
from .middle import middle, middle_assert, middle_test
from .power import get_tests as get_tests_power
from .power import power, power_test

TESTS = 100


class Test:
    def __init__(self, function, testcases, test_function, assert_function):
        self.function = function
        self.testcases = testcases
        self.test_function = test_function
        self.assert_function = assert_function

    def run(self, repair_function):
        repaired = repair_function(self.function, self.testcases, self.test_function)
        repaired = re.sub(self.function.__name__, "foo", repaired)
        exec(repaired, globals())

        for test in self.testcases:
            res = foo(*test)
            assert res == self.assert_function(*test)


test0 = Test(factorial1, get_tests_factorial1(TESTS), factorial1_test, math.factorial)
test1 = Test(factorial2, get_tests_factorial2(TESTS), factorial2_test, math.factorial)
test2 = Test(factorial3, get_tests_factorial3(TESTS), factorial3_test, math.factorial)
test3 = Test(middle, get_tests_middle(TESTS), middle_test, middle_assert)
test4 = Test(power, get_tests_power(TESTS), power_test, pow)

ALL_TESTS = [test0, test1, test2, test3, test4]


class Tester:

    def __init__(self, function, tests):
        self.function = function
        self.tests = tests
        random.seed(42)  # We use this seed for our evaluation; don't change it.

    def run_tests(self):
        for test in self.tests:
            try:
                test.run(self.function)
                print(f'Test {test.function.__name__}: OK')
            except AssertionError:
                print(f'Test {test.function.__name__}: Failed')
