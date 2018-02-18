#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == '__main__':

    if os.geteuid() != 0:
        print('You must have root privileges to do that! Running sudo...')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

    os.system('cp vhcreate.py /usr/local/bin/vhcreate')
    os.system('chmod 755 /usr/local/bin/vhcreate')