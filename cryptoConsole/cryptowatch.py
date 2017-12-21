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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse

from time import sleep
from os.path import exists
from sys import platform
from re import sub
from os.path import expanduser


from cryptoUtils.cryptoUtils import clear
from cryptoUtils.cryptoUtils import getCryptoData
import cryptoUtils.cwconfig as cfg


config = cfg.config()

def printHeader():
    print('_________                        __                         __         .__')
    print('\_   ___ \_______ ___.__._______/  |_  ______  _  _______ _/  |_  ____ |  |__')
    print('/    \  \/\_  __ <   |  |\____ \   __\/  _ \ \/ \/ /\__  \\\\   __\/ ___\|  |  \\')
    print('\     \____|  | \/\___  ||  |_> >  | (  <_> )     /  / __ \|  | \  \___|   Y  \\')
    print('\______  /|__|   / ____||   __/|__|   \____/ \/\_/  (____  /__|  \___  >___|  /')
    print('       \/        \/     |__|                             \/          \/     \/')
    print("         Created by: Alex Epstein https://github.com/alexanderepstein")

def cryptoFile(filePath):
    if platform in ["linux", "linux2", "darwin"]:
        if "~" in filePath:
            filePath = sub("~", expanduser("~"), filePath)
    if exists(filePath):
        answer = input("File already exists at %s, overwrite it? [Y/n] " % filePath)
        answer = answer.lower()
        if answer != 'y' and answer != "yes":
            exit()
    try:
        with open(filePath, 'w+') as file:
            data = getCryptoData()
            file.write(data)
    except IsADirectoryError:
        print("Error: the path provided is a directory")
        exit()
    printHeader()


def consoleLoop():
    try:
        while True:
            print(getCryptoData(True))
            sleep(30)
    except KeyboardInterrupt:
        clear()
        printHeader()

def main():
    parser = argparse.ArgumentParser(prog="Cryptowatch",description='Track prices and account balances for bitcoin, ethereum, and litecoin', epilog="By: Alex Epstein https://github.com/alexanderepstein")
    parser.add_argument("-m", "--monitor",help="Choose which cryptowatch monitor to use")
    parser.add_argument("-f", "--file", default="", help="Output the current cryptowatch data to the specified file path")
    parser.add_argument("-c", "--config", action = "store_true", help="Edit the config file for cryptowatch")
    parser.add_argument("-v", "--version", action="store_true", help="Display the current version of cryptowatch")
    args = parser.parse_args()
    if (args.version or args.config or args.file or args.monitor) and not (bool(args.version) ^ bool(args.config) ^ bool(args.monitor) ^ bool(args.file != "")):
        print("Error: all options for cryptowatch are mutually exclusive")
        exit()
    if args.version:
        print("Cryptowatch Version 0.0.6")
    elif args.config:
        config.edit()
    elif args.file != "":
        cryptoFile(args.file)
    elif args.monitor:
        if args.monitor == "pie" or args.monitor == "rpi":
            import cryptoPie.cryptoPie as pie
            printHeader()
            pie.main()
        elif args.monitor == "console" or args.monitor == "terminal" or args.monitor == "":
            consoleLoop()
        else:
            print("Error: invalid monitor type")
    else:
        print(getCryptoData())
