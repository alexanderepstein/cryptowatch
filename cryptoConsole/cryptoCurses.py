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
import curses
from textwrap import fill as textFill
from utils import cryptoUtils as crypto
from utils import cwconfig as cfg

config = cfg.config()

class cryptoCurses(object):
    def __init__(self, screen):
        self.screen = curses.initscr()
        #self.screen.immedok(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.scrollok(0)
        self.createMonitors()
        self.refresh()

    def drawEthereumBox(self):
        height,width = self.screen.getmaxyx()
        self.ethereumBox = curses.newwin(int(height/2) - 2,int(width/2) - 2 ,1,1)
        self.ethereumBox.immedok(True)
        self.ethereumBox.box()
        self.ethereumBox.addstr("Ethereum Monitor")

    def drawBitcoinBox(self):
        height,width = self.screen.getmaxyx()
        self.bitcoinBox = curses.newwin(int(height/2) - 2, int(width/2) - 1,1,int(width/2))
        self.bitcoinBox.immedok(True)
        self.bitcoinBox.box()
        self.bitcoinBox.addstr("Bitcoin Monitor")

    def drawLitecoinBox(self):
        height,width = self.screen.getmaxyx()
        self.litecoinBox = curses.newwin(int(height/2) - 2, int(width/2) - 2,int(height/2),1)
        self.litecoinBox.immedok(True)
        self.litecoinBox.box()
        self.litecoinBox.addstr("Litecoin Monitor")

    def drawBalanceBox(self):
        height,width = self.screen.getmaxyx()
        self.balanceBox = curses.newwin(int(height/2) - 2, int(width/2) - 1,int(height/2),int(width/2))
        self.balanceBox.immedok(True)
        self.balanceBox.box()
        self.balanceBox.addstr("Balance Monitor")

    def createMonitors(self):
        self.drawEthereumBox()
        self.drawBitcoinBox()
        self.drawLitecoinBox()
        self.drawBalanceBox()


    def refresh(self):
        self.screen.refresh()

    def clearWindow(self,box):
        if box == "ethereum":
            self.ethereumBox.clear()
        elif box == "bitcoin":
            self.bitcoinBox.clear()
        elif box == "litecoin":
            self.litecoinBox.clear()
        elif box == "balance":
            self.balanceBox.clear()

    def addText(self, text, box, xOffset, yOffset):
        xOffset = int(xOffset)
        yOffset = int(yOffset)
        if box == "ethereum":
            self.ethereumBox.addstr(yOffset,xOffset,text)
        elif box == "bitcoin":
            self.bitcoinBox.addstr(yOffset,xOffset,text)
        elif box == "litecoin":
            self.litecoinBox.addstr(yOffset,xOffset,text)
        elif box == "balance":
            self.balanceBox.addstr(yOffset,xOffset,text)
        elif box == "screen":
            self.screen.addstr(yOffset,xOffset,text)


    def destruct(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def clearScreen(self):
        self.screen.clear()

    def fillBalanceData(self,etherTotal,etherRate,bitcoinTotal,bitcoinRate,litecoinTotal,litecoinRate):
        self.height,self.width = self.ethereumBox.getmaxyx()
        self.center =  int(self.width/3 - self.width/15)
        self.initialHeight = int(self.height/5)
        self.textMax = self.width - self.center
        self.totalFiat = str(float(etherRate) * float(etherTotal) + float(bitcoinRate) * float(bitcoinTotal) + float(litecoinRate) * float(litecoinTotal))
        self.balanceBox.clear()
        self.drawBalanceBox()
        self.addText(textFill("ETH: " + etherTotal + "      " + config.fiatCurrency + ": " +str(float(etherTotal) * float(etherRate)) , self.textMax),"balance",self.center,self.initialHeight)
        self.addText(textFill("BTC: " + bitcoinTotal + "      " + config.fiatCurrency + ": " +str(float(bitcoinTotal) * float(bitcoinRate)) , self.textMax),"balance",self.center,self.initialHeight*2)
        self.addText(textFill("LTC: " + litecoinTotal + "      " + config.fiatCurrency + ": " +str(float(litecoinTotal) * float(litecoinRate)) , self.textMax),"balance",self.center,self.initialHeight*3)
        self.addText(textFill("Total " + config.fiatCurrency + ": " + self.totalFiat, self.textMax),"balance",self.center + 10,self.initialHeight*4)

    def fillData(self, response, box):
        if box == "ethereum":
            self.cryptoTicker = "ETH"
            self.address = config.etherAddress
            self.height,self.width = self.ethereumBox.getmaxyx()
        elif box == "bitcoin":
            self.cryptoTicker = "BTC"
            self.address = config.bitcoinAddress
            self.height,self.width = self.bitcoinBox.getmaxyx()
        elif box == "litecoin":
            self.cryptoTicker = "LTC"
            self.address = config.litecoinAddress
            self.height,self.width = self.litecoinBox.getmaxyx()
        else:
            raise ValueError('Error: invalid coin type')
        self.center =  int(self.width/3 - self.width/15)
        self.initialHeight = int(self.height/4)
        self.textMax = self.width - self.center
        self.exchangeRate = str(round(float(crypto.parseCryptoData(response, "ER")),2))
        self.hourlyPercentage = str(crypto.parseCryptoData(response, "HP"))
        self.dailyPercentage = str(crypto.parseCryptoData(response, "DP"))
        self.weeklyPercentage = str(crypto.parseCryptoData(response, "WP"))
        self.dailyVolume = str(round(float(crypto.parseCryptoData(response, "DV")),2))
        self.totalFiat = str(round(float(crypto.getTotalFiat(crypto.parseCryptoData(response, "ER"), box)),2))
        self.totalCrypto = str(float(self.totalFiat) / float(self.exchangeRate))
        if box == "ethereum":
            self.ethereumBox.clear()
            self.drawEthereumBox()
        elif box == "bitcoin":
            self.bitcoinBox.clear()
            self.drawBitcoinBox()
        elif box == "litecoin":
            self.litecoinBox.clear()
            self.drawLitecoinBox()
        self.addText(textFill(self.cryptoTicker + "->" + config.fiatCurrency + " " + self.exchangeRate, self.textMax),box,self.center,self.initialHeight)
        self.addText(textFill("1H: " + self.hourlyPercentage + "%   24H: " + self.dailyPercentage + "%", self.textMax),box, self.center,self.initialHeight * 2)
        self.addText(textFill("7 day: " + self.weeklyPercentage + "%   24H Volume: " + self.dailyVolume, self.textMax),box , self.center,self.initialHeight * 3)
        if self.address is not None :
            self.addText(textFill(self.cryptoTicker + ": " + self.totalCrypto + "    "  + config.fiatCurrency + ": " + self.totalFiat, self.textMax),box,self.center, self.initialHeight * 4)
        return self.exchangeRate, self.totalCrypto
