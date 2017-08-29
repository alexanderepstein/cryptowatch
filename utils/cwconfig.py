#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2017 Alex Epstein
#
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
import configparser
from os import path
from os import system
from sys import platform
configParser = configparser.RawConfigParser()

if platform == "linux" or platform == "linux2" or platform == "darwin":
    from os.path import expanduser
    home = expanduser("~")
    configFilePath = home + '/.crypto.cfg'
else:
    configFilePath = 'C:/.crypto.cfg'
    
configParser.read(configFilePath)
if not path.exists(configFilePath):
    with open(configFilePath, 'w+') as file:
        file.write("[cryptowatch-config]\n")
        file.write("etherAddress = \n")
        file.write("bitcoinAddress = \n")
        file.write("litecoinAddress = \n")
        file.write("fiatCurrency = USD\n")

"""Config Class to be shared throughout cryptowatch"""
class config(object):

    def __init__(self):
        self.etherAddress = configParser.get('cryptowatch-config', 'etherAddress').split(", ")
        self.bitcoinAddress = configParser.get('cryptowatch-config', 'bitcoinAddress').split(", ")
        self.litecoinAddress = configParser.get('cryptowatch-config', 'litecoinAddress').split(", ")
        self.fiatCurrency = configParser.get('cryptowatch-config', 'fiatCurrency')
        pass

    def edit(self):
        if not path.exists(configFilePath):
            with open(configFilePath, 'w+') as file:
                file.write("[cryptowatch-config]\n")
                file.write("etherAddress = \n")
                file.write("bitcoinAddress = \n")
                file.write("litecoinAddress = \n")
                file.write("fiatCurrency = USD\n")
        self.openFile(configFilePath)

    def openFile(self,filePath):
        if platform == "linux" or platform == "linux2":
            system("nano " + filePath)
        elif platform == "darwin":
            system("open " + filePath)
        elif platform == "win32":
            system("start " + filePath)
