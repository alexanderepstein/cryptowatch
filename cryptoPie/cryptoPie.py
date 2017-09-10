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


import time

import cryptoUtils.cryptoUtils as crypto
import cryptoUtils.cwconfig as cfg
import cryptoPie.Adafruit_CharLCD as Char_LCD

config = cfg.config()

registerSelect = int(config.registerSelect)
enable = int(config.enable)
db4 = int(config.db4)
db5 = int(config.db5)
db6 = int(config.db6)
db7 = int(config.db7)

# Screen Size
cols = int(config.cols)
rows = int(config.rows)
screen = Char_LCD.Adafruit_CharLCD(registerSelect,enable,db4,db5,db6,db7,cols,rows) # initializing the screen
delayTime = 10
waitTime = 500


def sleepMicroseconds(microseconds):
    # Busy wait in loop because delays are generally very short (few microseconds).
    end = time.time() + (microseconds / 1000000.0)
    while time.time() < end:
        pass


def scrollRight():
    for x in range(cols):
        screen.move_right()
        sleepMicroseconds(delayTime)


def showCryptoStats(coinType,response):
    coinType = coinType.lower()
    if coinType == "ethereum":
        cryptoTicker = "ETH"
        address = config.etherAddress
        screen.clear()
        screen.home()
    elif coinType == "bitcoin":
        cryptoTicker = "BTC"
        address = config.bitcoinAddress
        screen.clear()
        screen.home()
    elif coinType == "litecoin":
        cryptoTicker = "LTC"
        address = config.litecoinAddress
        screen.clear()
        screen.home()
    else:
        raise ValueError('Error: invalid coin type')
    exchangeRate = crypto.parseCryptoData(response, "ER")
    hourlyPercentage = crypto.parseCryptoData(response, "HP")
    dailyPercentage = crypto.parseCryptoData(response, "DP")
    totalFiat = crypto.getTotalFiat(crypto.parseCryptoData(response, "ER"), coinType)
    totalCrypto = float(totalFiat) / float(exchangeRate)
    screen.message("%s->%s:%.2f" % (cryptoTicker, config.fiatCurrency, float(exchangeRate)))
    screen.set_cursor(2, 1)
    if len("1H: %.2f  24H: %.2f" % (float(hourlyPercentage), float(dailyPercentage))) <= cols:
        screen.message("1H: %.2f  24H: %.2f" % (float(hourlyPercentage), float(dailyPercentage)))
    else:
        if len("1H: %.2f " % float(hourlyPercentage)) <= cols:
            screen.message("1H: %.2f " % float(hourlyPercentage))
        else:
            screen.message("1H: Daaayum")
    sleepMicroseconds(waitTime)
    if totalFiat != 0 and address is not None :
        scrollRight()
        screen.clear()
        screen.home()
        screen.message("%s: %.2f" % (cryptoTicker, float(totalCrypto)))
        screen.set_cursor(2, 1)
        screen.message("%s: %.2f" % (config.fiatCurrency, float(totalFiat)))
        sleepMicroseconds(waitTime)
    sleepMicroseconds(delayTime)



def main():
    screen.enable_display()  # just in case
    screen.clear()  # just in case
    etherResponse = crypto.queryCMC("ethereum")
    screen.home()  # start at inital position
    while True:
        showCryptoStats("ethereum",etherResponse)
        bitcoinResponse = crypto.queryCMC("bitcoin")
        scrollRight()
        screen.clear()
        screen.home()
        showCryptoStats("bitcoin",bitcoinResponse)
        litecoinResponse = crypto.queryCMC("litecoin")
        scrollRight()
        screen.clear()
        screen.home()
        showCryptoStats("litecoin",litecoinResponse)
        etherResponse = crypto.queryCMC("ethereum")
        scrollRight()
        screen.clear()
        screen.home()
