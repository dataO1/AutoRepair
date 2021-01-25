import random
import math


def factorial1(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


def factorial_testcase():
    n = random.randrange(100)
    return n


def factorial1_test(n):
    m = factorial1(n)
    assert m == math.factorial(n)


def factorial_passing_testcase():
    while True:
        try:
            n = factorial_testcase()
            _ = factorial1_test(n)
            return (n,)
        except AssertionError:
            pass


def factorial_failing_testcase():
    while True:
        try:
            n = factorial_testcase()
            _ = factorial1_test(n)
        except AssertionError:
            return (n,)


def get_tests(ntests):
    passing = [factorial_passing_testcase() for i in range(ntests)]
    failing = [factorial_failing_testcase() for i in range(ntests)]

    return passing + failing
