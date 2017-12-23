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
from os.path import exists
from os import system
from sys import platform
configParser = configparser.RawConfigParser()

if platform == "linux" or platform == "linux2" or platform == "darwin":
    from os.path import expanduser
    home = expanduser("~")
    configFilePath = home + '/.crypto.cfg'
else:
    configFilePath = 'C:/.crypto.cfg'

comment = """
# The wiring for the LCD is as follows:
# 1 : GND                    - GROUND
# 2 : 5V                     - 5V
# 3 : Contrast (0-5V)*       - GROUND
# 4 : RS (Register Select)   - GPIO 26
# 5 : R/W (Read Write)       - GROUND
# 6 : Enable or Strobe       - GPIO 19
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4             - GPIO 13
# 12: Data Bit 5             - GPIO 06
# 13: Data Bit 6             - GPIO 05
# 14: Data Bit 7             - GPIO 11
# 15: LCD Backlight +5V**    - 5V
# 16: LCD Backlight GND      - GROUND

# Setting up the pin -> GPIO variables
# Change these if you use different GPIO pins
"""





"""Config Class to be shared throughout cryptowatch"""
class config(object):

    def __init__(self):
        self.createConfigFile()
        configParser.read(configFilePath)
        self.etherAddress = configParser.get('cryptoConsole-config', 'etherAddress').split(", ")
        self.bitcoinAddress = configParser.get('cryptoConsole-config', 'bitcoinAddress').split(", ")
        self.litecoinAddress = configParser.get('cryptoConsole-config', 'litecoinAddress').split(", ")
        self.bitcoinCashAddress = configParser.get('cryptoConsole-config', 'bitcoinCashAddress').split(", ")
        self.dashAddress = configParser.get('cryptoConsole-config', 'dashAddress').split(", ")
        self.fiatCurrency = configParser.get('cryptoConsole-config', 'fiatCurrency')
        self.registerSelect = configParser.get('cryptoPie-config', 'registerSelect')
        self.enable = configParser.get('cryptoPie-config', 'enable')
        self.db4 = configParser.get('cryptoPie-config', 'db4')
        self.db5 = configParser.get('cryptoPie-config', 'db5')
        self.db6 = configParser.get('cryptoPie-config', 'db6')
        self.db7 = configParser.get('cryptoPie-config', 'db7')
        self.cols = configParser.get('cryptoPie-config', 'cols')
        self.rows = configParser.get('cryptoPie-config', 'rows')

    def edit(self):
        self.openFile(configFilePath)

    def openFile(self,filePath):
        if platform == "linux" or platform == "linux2":
            system("nano " + filePath)
        elif platform == "darwin":
            system("open " + filePath)
        elif platform == "win32":
            system("start " + filePath)

    def createConfigFile(self):
        if not exists(configFilePath):
            with open(configFilePath, 'w+') as file:
                file.write("[cryptoConsole-config]\n")
                file.write("etherAddress = \n")
                file.write("bitcoinAddress = \n")
                file.write("litecoinAddress = \n")
                file.write("bitcoinCashAddress = \n")
                file.write("dashAddress = \n")
                file.write("fiatCurrency = USD\n\n")
                file.write("[cryptoPie-config]\n\n")
                file.write("# GPIO Configuration\n")
                file.write("registerSelect = 26\n")
                file.write("enable = 19\n")
                file.write("db4 = 13\n")
                file.write("db5 = 11\n")
                file.write("db6 = 5\n")
                file.write("db7 = 11\n\n")
                file.write("# LCD Screen Variables\n")
                file.write("cols = 16\n")
                file.write("rows = 2\n")
                file.write(comment)
