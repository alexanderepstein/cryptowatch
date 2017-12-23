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

import json
from datetime import datetime
from sys import platform
from os import system

try:
    from colorclass import Color
except ImportError:
    raise ImportError("Error: no colorclass module found, install it with pip")
try:
    import requests
except ImportError:
    raise ImportError("Error: no requests module found, install it with pip")
try:
    from terminaltables import AsciiTable
except ImportError:
    raise ImportError("Error: no terminaltables module found, install it with pip")

import cryptoUtils.cwconfig as cfg

config = cfg.config()

"""
Parameter url: url to request
Output: JSON ready response from the server
Logic:
    - Request the url
    - Check for successful status code from server
    - Return the JSON response
"""
def request(url):
    response = requests.get(url)
    if response.status_code != 200 and response.status_code != 500 and response.status_code != 404:
        raise Exception('Error: requesting the api resulted in status code %s' %
                        response.status_code)
    return response.text


"""
Output: Clears the terminal
Logic:
    - We just want to know how to clear the terminal
    - Check the platform type
    - Clear the terminal in the right way
"""
def clear():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        system("clear")
    elif platform == "win32":
        system("cls")
    else:
        print("Uh-oh you are using an unsupported system :/")


"""
Output: Total crypto across all addresses in the config class
Parameters:
    - Cointype: Which coin do you want the total crypto for
Logic:
    - Start with 0 total crypto
    - For every respective address in the config file
        - Request respective api for balance
        - Add this balance to the total crypto
    - Return the total crypto
"""
def getTotalCrypto(coinType):
    totalCrypto = 0.0
    if coinType is "bitcoin":
        for address in config.bitcoinAddress:
            try:
                url =  url = "https://blockchain.info/rawaddr/" + address
                response = json.loads(request(url))
                totalCrypto += float(response['final_balance']) / pow(10, 8)
            except Exception:
                pass
    elif coinType is "ethereum":
        etherscanAPIKey = "V8ENE44FM98SCDPIXGGHQDFD2KCRSKJ8BJ"
        for address in config.etherAddress:
            try:
                url = "http://api.etherscan.io/api?module=account&action=balance&address=" + \
                address + "&tag=latest&apikey=" + etherscanAPIKey
                response = json.loads(request(url))
                totalCrypto += float(response['result']) / pow(10, 18)
            except Exception:
                pass
    elif coinType is "litecoin":
        for address in config.litecoinAddress:
                try:
                    url = url = "https://chain.so/api/v2/get_address_balance/LTC/" + address
                    response = json.loads(request(url))
                    totalCrypto += float(response['data']['confirmed_balance'])
                except Exception:
                    pass
    elif coinType == "bitcoin-cash": # Need to use == here and not is cannot figure out why
        for address in config.bitcoinCashAddress:
            try:
                url = "https://cashexplorer.bitcoin.com/api/addr/" + address + "/balance"
                response = json.loads(request(url))
                totalCrypto += float(response) / pow(10, 8)
            except Exception:
                pass
    elif coinType is "dash":
        for address in config.dashAddress:
                try:
                    url = url = "https://chain.so/api/v2/get_address_balance/DASH/" + address
                    response = json.loads(request(url))
                    print(response)
                    totalCrypto += float(response['data']['confirmed_balance'])
                except Exception:
                    pass
    return totalCrypto



"""
Output: Array of metrics related to the respective coin type
Parameters
    - Cointype: query coinmarketcap about this specified cointype
    - Colored: Do we want the colored version of the output (only when sending to terminal do we want this)
Logic:
    - Request info from coinmarket cap
    - Ready the response for JSON parsing
    - Parse the response and append each piece of info to the metrics array
    - Return the metrics array
"""
def getCryptoInfo(coinType, colored=False):
    metrics = []
    coinTypes = ["bitcoin", "ethereum", "litecoin", "bitcoin-cash", "dash"]
    if coinType not in coinTypes:
        raise ValueError("Invalid coinType")
    url = "https://api.coinmarketcap.com/v1/ticker/" + coinType + "/?convert=" + config.fiatCurrency
    response = json.loads(request(url))
    totalCrypto = getTotalCrypto(coinType)
    if not colored:
        metrics.append(response[0]['price_' + config.fiatCurrency.lower()])
        metrics.append(response[0]['24h_volume_' + config.fiatCurrency.lower()])
        metrics.append(response[0]['percent_change_7d'])
        metrics.append(response[0]['percent_change_24h'])
        metrics.append(response[0]['percent_change_1h'])
        metrics.append(totalCrypto)
        metrics.append(totalCrypto*float(response[0]['price_' + config.fiatCurrency.lower()]))
    else:
        metrics.append(Color("{autogreen}" + response[0]['price_' + config.fiatCurrency.lower()] + "{/autogreen}"))
        metrics.append(Color("{autogreen}" + response[0]['24h_volume_' + config.fiatCurrency.lower()] + "{/autogreen}"))
        if float(response[0]['percent_change_7d']) >= 0:
            metrics.append(Color("{autogreen}" + response[0]['percent_change_7d'] + "{/autogreen}"))
        else:
            metrics.append(Color("{autored}" + response[0]['percent_change_7d'] + "{/autored}"))
        if float(response[0]['percent_change_24h']) >= 0:
            metrics.append(Color("{autogreen}" + response[0]['percent_change_24h'] + "{/autogreen}"))
        else:
            metrics.append(Color("{autored}" + response[0]['percent_change_24h'] + "{/autored}"))
        if float(response[0]['percent_change_1h']) >= 0:
            metrics.append(Color("{autogreen}" + response[0]['percent_change_1h'] + "{/autogreen}"))
        else:
            metrics.append(Color("{autored}" + response[0]['percent_change_1h'] + "{/autored}"))
        metrics.append(Color("{autocyan}" + str(totalCrypto) + "{/autocyan}"))
        metrics.append(float(totalCrypto)*float(response[0]['price_' + config.fiatCurrency.lower()]))

    return metrics


"""
Output: Returns an ascii table for all cryptocurrencies and their data
Parameters:
    - clearConsole: Do we want to clear the console before returning this data (we do want to do this when running in monitor mode)
    - Colored: Do we want the table to be colored
Logic:
    - Create header
    - Get metrics on each legal currency and insert into their own array
    - Get the total fiat by adding the last index of each metrics array together
    - Insert cointypes into the respective array
    - Combine the header and the crypto metrics into one big metrics array
    - Create the ascii table from this data and return it
"""
def getCryptoTable(clearConsole=False, colored=True):
    metrics = []
    bitcoinMetrics = getCryptoInfo("bitcoin", colored)
    ethereumMetrics = getCryptoInfo("ethereum", colored)
    litecoinMetrics = getCryptoInfo("litecoin", colored)
    bitcoinCashMetrics = getCryptoInfo("bitcoin-cash", colored)
    dashMetrics = getCryptoInfo("dash", colored)
    totalFiat = bitcoinMetrics[-1] + ethereumMetrics[-1] + litecoinMetrics[-1] + bitcoinCashMetrics[-1] + dashMetrics[-1]
    if colored:
        header = [Color("{automagenta}Coin Type{/automagenta}"), Color("{automagenta}Price " + config.fiatCurrency+"{/automagenta}"),
        Color("{automagenta}24h Volume{/automagenta}"), Color("{automagenta}7d % Change{/automagenta}"), Color("{automagenta}24h % Change{/automagenta}"),
        Color("{automagenta}1h % Change{/automagenta}"), Color("{automagenta}Crypto Balance{/automagenta}"), Color("{automagenta}" + config.fiatCurrency.upper() + " Balance" + "{/automagenta}")]
        bitcoinMetrics.insert(0, Color("{autocyan}Bitcoin{/autocyan}"))
        ethereumMetrics.insert(0, Color("{autocyan}Ethereum{/autocyan}"))
        litecoinMetrics.insert(0, Color("{autocyan}Litecoin{/autocyan}"))
        bitcoinCashMetrics.insert(0, Color("{autocyan}Bitcoin Cash{/autocyan}"))
        dashMetrics.insert(0, Color("{autocyan}Dash{/autocyan}"))
        footer = Color("{automagenta}Last Updated: %s{/automagenta}\t\t\t\t\t\t\t      {autogreen}Total %s: %.2f{/autogreen}" % (str(datetime.now()), config.fiatCurrency, totalFiat))
    else:
        header = ["Coin Type","Price " + config.fiatCurrency, "24h Volume", "7d % Change", "24h % Change", "1h % Change", "Crypto Balance",config.fiatCurrency.upper() + " Balance"]
        bitcoinMetrics.insert(0, "Bitcoin")
        ethereumMetrics.insert(0, "Ethereum")
        litecoinMetrics.insert(0, "Litecoin")
        bitcoinCashMetrics.insert(0, "Bitcoin Cash")
        dashMetrics.insert(0, "Dash")
        footer = "Last Updated: %s \t\t\t\t\t\t\t      Total %s: %.2f" % (str(datetime.now()), config.fiatCurrency, totalFiat)
    metrics.append(header)
    metrics.append(bitcoinMetrics)
    metrics.append(ethereumMetrics)
    metrics.append(litecoinMetrics)
    metrics.append(bitcoinCashMetrics)
    metrics.append(dashMetrics)
    table = AsciiTable(metrics)
    if clearConsole:
        clear()
    return table.table + "\n" + footer
