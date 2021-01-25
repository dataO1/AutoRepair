import random


def middle(x, y, z):
    if x < x:
        if y < z:
            return y
        if x < z:
            return z
        return x
    if x < z:
        return x
    if y < z:
        return z
    return y


def middle_testcase():
    x = random.randrange(10)
    y = random.randrange(10)
    z = random.randrange(10)
    return x, y, z


def middle_assert(x, y, z):
    return sorted([x, y, z])[1]


def middle_test(x, y, z):
    m = middle(x, y, z)
    assert m == middle_assert(x, y, z)


def middle_passing_testcase():
    while True:
        try:
            x, y, z = middle_testcase()
            _ = middle_test(x, y, z)
            return x, y, z
        except AssertionError:
            pass


def middle_failing_testcase():
    while True:
        try:
            x, y, z = middle_testcase()
            _ = middle_test(x, y, z)
        except AssertionError:
            return x, y, z


def get_tests(ntests):
    passing = [middle_passing_testcase() for i in range(ntests)]
    failing = [middle_failing_testcase() for i in range(ntests)]

    return passing + failing
