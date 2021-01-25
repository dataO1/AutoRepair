import random
import math


def factorial_testcase():
    n = random.randrange(100)
    return n


def factorial2(n): 
    i = 1
    for i in range(1, n + 1):
        i *= i
    return i


def factorial2_test(n):
    m = factorial2(n)
    assert m == math.factorial(n)


def factorial_passing_testcase():
    while True:
        try:
            n = factorial_testcase()
            _ = factorial2_test(n)
            return (n,)
        except AssertionError:
            pass


def factorial_failing_testcase():
    while True:
        try:
            n = factorial_testcase()
            _ = factorial2_test(n)
        except AssertionError:
            return (n,)


def get_tests(ntests):
    passing = [factorial_passing_testcase() for i in range(ntests)]
    failing = [factorial_failing_testcase() for i in range(ntests)]

    return passing + failing
