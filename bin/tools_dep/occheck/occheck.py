import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/packages")
import occheck.__main__ as check

if __name__ == '__main__':
    check.run_check()
