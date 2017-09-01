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
from sys import platform
from os import system
from os.path import exists

import utils.cryptoUtils as crypto
import utils.cwconfig as cfg
import cryptoConsole.cryptoCurses as myCurses

config = cfg.config()




def clear():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        system("clear")
    elif platform == "win32":
        system("cls")


def printHeader():
    print('_________                        __                         __         .__')
    print('\_   ___ \_______ ___.__._______/  |_  ______  _  _______ _/  |_  ____ |  |__')
    print('/    \  \/\_  __ <   |  |\____ \   __\/  _ \ \/ \/ /\__  \\\\   __\/ ___\|  |  \\')
    print('\     \____|  | \/\___  ||  |_> >  | (  <_> )     /  / __ \|  | \  \___|   Y  \\')
    print('\______  /|__|   / ____||   __/|__|   \____/ \/\_/  (____  /__|  \___  >___|  /')
    print('       \/        \/     |__|                             \/          \/     \/')


"""
Output: Appends the information about a certain cryptocurrency to a file
Parameter coinType: Specifcies which coin to write the information about
Logic:
    - Get the respective address array for the coinType
    - Query coinmarketcap about the coinType
    - Parse the response
    - Get total amount fiat amount
    - Determine total crypto amount
    - Format and write the data to the monitorFilePath
"""
def consoleMonitor(coinType, monitorFilePath):
    coinType = coinType.lower()
    if coinType == "ethereum":
        cryptoTicker = "ETH"
        address = config.etherAddress
    elif coinType == "bitcoin":
        cryptoTicker = "BTC"
        address = config.bitcoinAddress
    elif coinType == "litecoin":
        cryptoTicker = "LTC"
        address = config.litecoinAddress
    else:
        raise ValueError('Error: invalid coin type')
    response = crypto.queryCMC(coinType)
    exchangeRate = float(crypto.parseCryptoData(response, "ER"))
    hourlyPercentage = float(crypto.parseCryptoData(response, "HP"))
    dailyPercentage = float(crypto.parseCryptoData(response, "DP"))
    weeklyPercentage = float(crypto.parseCryptoData(response, "WP"))
    dailyVolume = float(crypto.parseCryptoData(response, "DV"))
    totalFiat = float(crypto.getTotalFiat(crypto.parseCryptoData(response, "ER"), coinType))
    totalCrypto = float(totalFiat) / float(exchangeRate)
    with open(monitorFilePath, 'a+') as file:
        file.write("%s->%s:%.2f\n" % (cryptoTicker, config.fiatCurrency, exchangeRate))
        file.write("1H: %.2f%%  24H: %.2f%%\n" % (hourlyPercentage, dailyPercentage))
        file.write("7 day: %.2f%%   24H Volume: %.2f\n" % (weeklyPercentage, dailyVolume))
        if address is not None :
            file.write("%s: %.2f   %s: %.2f\n" % (cryptoTicker, totalCrypto, config.fiatCurrency, totalFiat))
        file.write("\n")
    return totalFiat

def cryptoFile(filePath):
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        if "~" in filePath:
            from re import sub
            from os.path import expanduser
            filePath = sub("~",expanduser("~"),filePath)
    if exists(filePath):
        answer = input("File already exists at %s, overwrite it? [Y/n] " % filePath)
        answer = answer.lower()
        if answer != "y" and answer != "yes":
            exit()
    try:
        open(filePath, 'w+').close()
    except IsADirectoryError:
        print("Error: the path provided is a directory")
        exit()
    print("Loading...")
    totalFiat = 0.00
    totalFiat += consoleMonitor("ethereum", filePath)
    totalFiat += consoleMonitor("bitcoin", filePath)
    totalFiat += consoleMonitor("litecoin", filePath)
    with open(filePath, 'a+') as file:
        file.write("Total %s: %.2f\n" %(config.fiatCurrency, totalFiat))
    clear()
    printHeader()

def printCryptoData():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        from os.path import expanduser
        home = expanduser("~")
        monitorFilePath = home + '/.cryptoConsole'
    else:
        monitorFilePath = 'C:/.cryptoConsole'
    print("Loading...")
    open(monitorFilePath, 'w+').close()
    totalFiat = 0.00
    totalFiat += consoleMonitor("ethereum", monitorFilePath)
    totalFiat += consoleMonitor("bitcoin", monitorFilePath)
    totalFiat += consoleMonitor("litecoin", monitorFilePath)
    clear()
    printHeader()
    with open(monitorFilePath, 'a+') as file:
        file.write("Total %s: %.2f\n" %(config.fiatCurrency, totalFiat))
    with open(monitorFilePath, 'r') as file:
        print(file.read())
    open(monitorFilePath, 'w').close()

def cursesLoop():
    from curses import wrapper as wrapper
    cryptoCurses = wrapper(myCurses.cryptoCurses)
    etherResponse = crypto.queryCMC("ethereum")
    bitcoinResponse = crypto.queryCMC("bitcoin")
    litecoinResponse = crypto.queryCMC("litecoin")
    cryptoCurses.refresh()
    try:
        while True:
            cryptoCurses.checkResize()
            etherRate, etherCrypto = cryptoCurses.fillData(etherResponse,"ethereum")
            cryptoCurses.checkResize()
            bitcoinRate, bitcoinCrypto = cryptoCurses.fillData(bitcoinResponse,"bitcoin")
            cryptoCurses.checkResize()
            litecoinRate, litecoinCrypto = cryptoCurses.fillData(litecoinResponse,"litecoin")
            cryptoCurses.checkResize()
            cryptoCurses.fillBalanceData(etherCrypto,etherRate,bitcoinCrypto,bitcoinRate,litecoinCrypto,litecoinRate)
            cryptoCurses.refresh()
            etherResponse = crypto.queryCMC("ethereum")
            bitcoinResponse = crypto.queryCMC("bitcoin")
            litecoinResponse = crypto.queryCMC("litecoin")
    except KeyboardInterrupt:
        cryptoCurses.destruct()
        printHeader()
    except Exception as err:
        cryptoCurses.destruct()
        printHeader()
        print("Fatal error: " + err)
        print("Report any issues to: https:github.com/alexanderepstein/cryptowatch/issues")

def main():
    parser = argparse.ArgumentParser(prog="Cryptowatch",description='Track prices and account balances for bitcoin, ethereum, and litecoin', epilog="By: Alex Epstein https://github.com/alexanderepstein")
    parser.add_argument("-m", "--monitor",help="Choose which cryptowatch monitor to use")
    parser.add_argument("-f", "--file", default="", help="Output the current cryptowatch data to the specified file path")
    parser.add_argument("-c", "--config", action = "store_true", help="Edit the config file for cryptowatch")
    parser.add_argument("-v", "--version", action="store_true", help="Display the current version of cryptowatch")
    args = parser.parse_args()
    if args.version:
        print("Cryptowatch Version 0.0.4")
    elif args.config:
        config.edit()
    elif args.file != "":
        cryptoFile(args.file)
    elif args.monitor:
        if args.monitor == "pie" or args.monitor == "rpi":
            import cryptoPie.cryptoPie as pie
            printHeader()
            pie.main()
        elif args.monitor == "console" or args.monitor == "terminal":
            cursesLoop()
        else:
            print("Error: invalid monitor type")
    else:
        printCryptoData()
    exit()
