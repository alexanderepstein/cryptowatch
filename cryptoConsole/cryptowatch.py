#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Alex Epstein

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from os.path import exists, expanduser
from re import sub
from sys import platform
from time import sleep

import cryptoUtils.cwconfig as cfg
from cryptoUtils.cryptoUtils import clear
from cryptoUtils.cryptoUtils import get_crypto_table


HEADER = '''\
_________                        __                         __         .__
\_   ___ \_______ ___.__._______/  |_  ______  _  _______ _/  |_  ____ |  |__
/    \  \/\_  __ <   |  |\____ \   __\/  _ \ \/ \/ /\__  \\\\   __\/ ___\|  |  \\
\     \____|  | \/\___  ||  |_> >  | (  <_> )     /  / __ \|  | \  \___|   Y  \\
\______  /|__|   / ____||   __/|__|   \____/ \/\_/  (____  /__|  \___  >___|  /
       \/        \/     |__|                             \/          \/     \/
         Created by: Alex Epstein https://github.com/alexanderepstein
'''


def print_header():
    print(HEADER)


def crypto_file(file_path):
    if platform in ("linux", "linux2", "darwin") and "~" in file_path:
        file_path = sub("~", expanduser("~"), file_path)
    if exists(file_path):
        answer = input("File already exists at %s, overwrite it? [Y/n] "
                       % file_path)
        if answer.lower().strip() not in ('y', 'yes'):
            exit()
    try:
        with open(file_path, 'w+') as file:
            data = get_crypto_table(False, False)
            file.write(data)
            file.write("\n")
    except IsADirectoryError:
        print("Error: the path provided is a directory")
        exit()
    print_header()


def console_loop():
    try:
        while True:
            print(get_crypto_table(True))
            sleep(30)
    except KeyboardInterrupt:
        clear()
        print_header()


def main():
    parser = argparse.ArgumentParser(
        prog="Cryptowatch",
        description='Track prices and account balances for bitcoin, '
                    'ethereum, litecoin, bitcoin cash and dash',
        epilog="By: Alex Epstein https://github.com/alexanderepstein"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        "--monitor",
        choices=('pie', 'rpi', 'console', 'terminal'),
        help="Choose which cryptowatch monitor to use"
    )
    group.add_argument(
        "-f",
        "--file",
        help="Output the current cryptowatch data to the specified file path"
    )
    group.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="Edit the config file for cryptowatch"
    )
    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Display the current version of cryptowatch"
    )
    args = parser.parse_args()

    if args.version: print("Cryptowatch Version 0.0.11")
    elif args.config: cfg.config().edit()
    elif args.file: crypto_file(args.file)
    elif args.monitor:
        if args.monitor in ("pie", "rpi"):
            import cryptoPie.cryptoPie as pie
            print_header()
            pie.main()
        else: console_loop()
    else: print(get_crypto_table())
