#!python

import sys
import os
import platform
from distutils.extension import Extension
from shutil import move


def generate_pyx(name):
    result = []
    in_block = False
    replace_file = ""
    with open(name, 'r') as f:
        for line in f:
            if '#<PyxReplace>#' in line:
                in_block = True
                splitted = line.split(' ')
                if len(splitted) > 1:
                    replace_file = splitted[1].rstrip()
                else:
                    replace_file = ""
            if not in_block:
                result.append(line)
            if '#<EndReplace>#' in line:
                in_block = False
                if replace_file:
                    with open(replace_file, 'r') as f2:
                        for l2 in f2:
                            result.append(l2)
    with open(name + 'x', 'w') as f:
        f.writelines(result)


def pyx_extensions(files):
    result = []
    for f in files:
        s = f.split('.')
        generate_pyx(f)
        new_name = '_genpyx_' + '_'.join(platform.architecture()) + '_' + s[0]
        new_name_pyx = new_name + '.pyx'
        move(f + 'x', new_name_pyx)
        result.append(Extension(new_name, [new_name_pyx]))
    return result


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: %s [cython-options] sourcefile.py' % sys.argv[0])
        print('       %s -c sourcefile.py' % sys.argv[0])
        sys.exit(1)
    generate_pyx(argv[-1])
    if not '-c' in argv:
        result = os.system('cython %s' % ' '.join(argv) + 'x')
        if result:
            sys.exit('cython failed with code %s' % (os.WEXITSTATUS(result)))
