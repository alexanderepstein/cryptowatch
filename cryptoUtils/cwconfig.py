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
        self.bitcoinAddress = map(str.strip, configParser.get('cryptoConsole-config', 'bitcoinAddress').split(","))
        self.etherAddress = map(str.strip, configParser.get('cryptoConsole-config', 'etherAddress').split(","))
        self.litecoinAddress = map(str.strip, configParser.get('cryptoConsole-config', 'litecoinAddress').split(","))
        try:
            self.bitcoinCashAddress = map(str.strip, configParser.get('cryptoConsole-config', 'bitcoinCashAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("bitcoinCash")
            configParser.read(configFilePath)
            self.bitcoinCashAddress = map(str.strip, configParser.get('cryptoConsole-config', 'bitcoinCashAddress').split(","))
            pass
        try:
            self.dashAddress = map(str.strip, configParser.get('cryptoConsole-config', 'dashAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("dash")
            configParser.read(configFilePath)
            self.dashAddress = map(str.strip, configParser.get('cryptoConsole-config', 'dashAddress').split(","))
            pass
        try:
            self.rippleAddress = map(str.strip, configParser.get('cryptoConsole-config', 'rippleAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("ripple")
            configParser.read(configFilePath)
            self.rippleAddress = map(str.strip, configParser.get('cryptoConsole-config', 'rippleAddress').split(","))
            pass
        try:
            self.digibyteAddress = map(str.strip, configParser.get('cryptoConsole-config', 'digibyteAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("digibyte")
            configParser.read(configFilePath)
            self.digibyteAddress = map(str.strip, configParser.get('cryptoConsole-config', 'digibyteAddress').split(","))
            pass
        try:
            self.stellarAddress = map(str.strip, configParser.get('cryptoConsole-config', 'stellarAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("stellar")
            configParser.read(configFilePath)
            self.stellarAddress = map(str.strip, configParser.get('cryptoConsole-config', 'stellarAddress').split(","))
            pass
        try:
            self.cardanoAddress = map(str.strip, configParser.get('cryptoConsole-config', 'cardanoAddress').split(","))
        except configparser.NoOptionError:
            self.addCrypto("cardano")
            configParser.read(configFilePath)
            self.cardanoAddress = map(str.strip, configParser.get('cryptoConsole-config', 'cardanoAddress').split(","))
            pass
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
        coinNames = ["bitcoin", "ether", "litecoin", "bitcoinCash"
                     "dash", "ripple", "digibyte", "stellar", "cardano"]
        if not exists(configFilePath):
            with open(configFilePath, 'w+') as file:
                file.write("[cryptoConsole-config]\n")
                for coin in coinNames: file.write("%sAddress = \n" % coin)
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

    def addCrypto(self, coinType):
        lines = []
        with open(configFilePath, "r") as inFile:
            for line in inFile: lines.append(line)
            with open(configFilePath, "w") as outFile:
                outFile.write("%s" % lines[0])
                outFile.write("%sAddress = \n" % coinType)
                for i in range(1,len(lines)):
                    outFile.write("%s" % lines[i])
