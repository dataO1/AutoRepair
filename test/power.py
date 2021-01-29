import random

def power(x, n):
    res = 1
    for i in range(0, x):
        res *= n
    return res


def power_testcase():
    x = random.randrange(100)
    n = random.randrange(100)
    return x, n

def power_test(x, n):
    m = power(x, n)
    assert m == pow(x, n)

def power_passing_testcase():
    while True:
        try:
            x, n = power_testcase()
            _ = power_test(x, n)
            return x, n
        except AssertionError:
            pass

def power_failing_testcase():
    while True:
        try:
            x, n = power_testcase()
            _ = power_test(x, n)
        except AssertionError:
            return x, n


def get_tests(ntests):
    passing = [power_passing_testcase() for i in range(ntests)]
    failing = [power_failing_testcase() for i in range(ntests)]

    return passing + failing
