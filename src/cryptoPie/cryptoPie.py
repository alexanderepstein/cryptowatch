#!/usr/bin/env python
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
import os
import sys

sys.path.append("..")
import cryptoUtils as crypto
import cwconfig as cfg
sys.path.remove("..")

config = cfg.config()
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
registerSelect = 26
enable = 19
db4 = 13
db5 = 6
db6 = 5
db7 = 11

# Screen Size
cols = 16
rows = 2
# screen = Adafruit_CharLCD.Adafruit_CharLCD(registerSelect,enable,db4,db5,db6,db7,cols,rows) # initialiing the screen
delayTime = 10
waitTime = 500


def sleepMicroseconds(self, microseconds):
    # Busy wait in loop because delays are generally very short (few microseconds).
    end = time.time() + (microseconds / 1000000.0)
    while time.time() < end:
        pass


def scrollRight():
    for x in range(16):
        screen.move_right()
        sleepMicroseconds(delayTime)


def showCryptoStats(coinType="ethereum"):
    coinType = coinType.lower()
    if coinType == "ethereum":
        cryptoTicker = "ETH"
    elif coinType == "bitcoin":
        cryptoTicker = "BTC"
    elif coinType == "litecoin":
        cryptoTicker = "LTC"
    else:
        raise ValueError('Error: invalid coin type')
    response = crypto.queryCMC(coinType)
    exchangeRate = crypto.parseCryptoData(response, "ER")
    hourlyPercentage = crypto.parseCryptoData(response, "HP")
    dailyPercentage = crypto.parseCryptoData(response, "DP")
    totalFiat = crypto.getTotalFiat(crypto.parseCryptoData(response, "ER"), coinType)
    totalCrypto = float(totalFiat) / float(exchangeRate)
    screen.message("%s->%s:%.2f" % (cryptoTicker, config.fiatCurrency, exchangeRate))
    screen.set_cursor(2, 1)
    if len("1H: %.2f  24H: %.2f" % (hourlyPercentage, dailyPercentage)) <= cols:
        screen.message("1H: %.2f  24H: %.2f" % (hourlyPercentage, dailyPercentage))
    else:
        if len("1H: %.2f " % hourlyPercentage) <= cols:
            screen.message("1H: %.2f " % hourlyPercentage)
        else:
            screen.message("1H: Daaayum")
    sleepMicroseconds(waitTime)
    scrollRight()
    if totalFiat != 0:
        screen.clear()
        screen.home()
        screen.message("%s: %.2f" % (cryptoTicker, totalCrypto))
        screen.set_cursor(2, 1)
        screen.message("%s: %.2f" % (config.fiatCurrency, totalFiat))
        sleepMicroseconds(waitTime)
        scrollRight()
    sleepMicroseconds(delayTime)
    screen.clear()


def main():
    screen.enable_display()  # just in case
    screen.clear()  # just in case
    screen.home()  # start at inital position
    while True:
        showCryptoStats("ethereum")
        showCryptoStats("bitcoin")
        showCryptoStats("litecoin")


if __name__ == '__main__':
    # main()
    crypto.printAllCryptoData()  # useful for debugging
