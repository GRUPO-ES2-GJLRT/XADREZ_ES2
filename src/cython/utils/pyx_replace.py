#!python

import sys
import os
import platform
from distutils.extension import Extension
from shutil import move, copy
import hashlib


def read_file(name, result, base=""):
    checksum = 0L
    in_block = False
    replace_file = ""
    fname = os.path.join(base, name)
    with open(fname, 'r') as f:
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
                    checksum += read_file(replace_file, result, base)
    return checksum + int(hashlib.sha256(
        open(fname, 'rb').read()).digest().encode("hex"), 16)


def generate_pyx(name):
    result = []
    checksum = read_file(name, result)
    result.insert(0, "CHECKSUM = {0}\n".format(checksum))
    with open('_genpyx_' + name, 'w') as f:
        f.writelines(result)


def pyx_extensions(files):
    result = []
    for f in files:
        s = f.split('.')
        generate_pyx(f)
        new_name = '_genpyx_' + '_'.join(platform.architecture()) + '_' + s[0]
        new_name_py = new_name + '.py'
        new_name_pxd = new_name + '.pxd'
        move('_genpyx_' + f, new_name_py)
        copy(s[0] + '.pxd', new_name_pxd)
        result.append(Extension(new_name, [new_name_py]))
    return result


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: %s [cython-options] sourcefile.py' % sys.argv[0])
        print('       %s -c sourcefile.py' % sys.argv[0])
        sys.exit(1)
    generate_pyx(argv[-1])
    name = argv[-1].split('.')
    copy(name[0] + '.pxd', '_genpyx_' + name[0] + '.pxd')
    argv[-1] = '_genpyx_' + name[0] + '.py'
    if not '-c' in argv:
        result = os.system('cython %s' % ' '.join(argv))
        if result:
            sys.exit('cython failed with code %s' % (result))
