#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import textwrap
import re


def get_check_filename(check_name):
    return check_name.replace('-', '_') + ".py"


def get_check_classname(check_name):
    classname = ''.join(map(lambda x: x.capitalize(), check_name.split('-'))) + 'Check'
    return classname


def write_implementation(module_path, check_name):
    filename = os.path.join(module_path, get_check_filename(check_name))
    classname = get_check_classname(check_name)

    with open(filename, 'w') as f:
        text = textwrap.dedent('''\
    from occheck.checks import BaseCheck
    
    
    class %s(BaseCheck):
        
        def __init__(self):
            super().__init__()
        
        def initialize(self):
            """Initialize this check here."""
    
        def begin_check(self, filename):
            """Begin check a new file."""
    
        def finish_check(self, filename):
            """Finished check the file."""
    
    ''' % classname)
        f.write(text)


def add_module(module_path):
    filename = os.path.join(module_path, '__init__.py')
    os.makedirs(module_path)

    with open(filename, 'w') as f:
        f.write(textwrap.dedent('''\
        from .. import CheckRegistry


        def register_checks():
            pass


        register_checks()

        '''))


def adapt_module(module_path, module_name, check_name):
    srcfile = os.path.join(module_path, '__init__.py')
    dstfile = os.path.join(module_path, '__init__.py.add_check')
    classname = get_check_classname(check_name)
    canonical_check_name = '%s-%s' % (module_name, check_name)

    with open(srcfile, 'r') as f:
        lines = f.readlines()

    with open(dstfile, 'w') as f:
        import_added = False
        check_added = False

        for line in lines:
            if not import_added:
                if line == "from .. import CheckRegistry\n":
                    f.write(line)
                    f.write('from .%s import %s\n' % (check_name.replace('-', '_'), classname))
                    import_added = True
                    continue

            if not check_added:
                match = re.search(r'def\s+register_checks\(\)\s*:', line)
                if match:
                    f.write(line)
                    f.write('    CheckRegistry.register_check("%s", %s)\n' % (canonical_check_name, classname))
                    check_added = True
                    continue

            f.write(line)

    os.remove(srcfile)
    os.rename(dstfile, srcfile)


def check_exists(module_path, check_name):
    try:
        files = os.listdir(module_path)
        filename = get_check_filename(check_name)
        return filename in files
    except OSError:
        pass

    return False


def module_exists(module_path):
    return os.path.exists(module_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", nargs="?")
    parser.add_argument("check", nargs="?")

    args = parser.parse_args()

    module_name = args.module
    check_name = args.check

    if not module_name or not check_name:
        print("Module and check must be specified.\n")
        parser.print_usage()
        sys.exit(1)

    if check_name.startswith(module_name):
        print("Check name '%s' must not start with the module '%s'.\n" % (check_name, module_name))
        sys.exit(1)

    root_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    module_path = os.path.join(root_path, 'checks', module_name)

    if check_exists(module_path, check_name):
        print("Check '%s' exists in the module '%s'." % (check_name, module_name))
        sys.exit(1)

    if not module_exists(module_path):
        add_module(module_path)

    write_implementation(module_path, check_name)
    adapt_module(module_path, module_name, check_name)

    print("Done.")
    sys.exit(0)


if __name__ == '__main__':
    main()

