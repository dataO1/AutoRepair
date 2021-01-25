from debuggingbook import Repairer
from test.tests import Tester, ALL_TESTS
from autorepair.debugger import simple_debug_and_repair
#!/usr/bin/env python

def main():
    Tester(simple_debug_and_repair, ALL_TESTS).run_tests()

if __name__ == "__main__":
    main()
