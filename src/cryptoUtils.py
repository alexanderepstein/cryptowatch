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
import cwconfig as cfg

config = cfg.config()


"""
Parameter addressType: address type to return
Output: An array of addresses respective to the the corresponding addressType
Logic: Go through the config class and retrive the respective addresses
"""
def getAddress(addressType="ether"):
    if addressType == "ether":
        etherAddress = config.etherAddress
        if etherAddress is None:
            raise ValueError("No ether address to return")
        return etherAddress
    elif addressType == "bitcoin":
        bitcoinAddress = config.bitcoinAddress
        if bitcoinAddress is None:
            raise ValueError("No bitcoin address to return")
        return bitcoinAddress
    elif addressType == "litecoin":
        litecoinAddress = config.litecoinAddress
        if litecoinAddress is None:
            raise ValueError("No litecoin address to return")
        return litecoinAddress
    else:
        raise Exception('Error: invalid address type %s' % addressType)


"""
Parameter url: url to request
Output: JSON ready response from the server
Logic:
    - Request the url
    - Check for successful status code from server
    - Return the JSON response
"""
def request(url):
    try:
        import requests
    except ImportError:
        raise ImportError("Error: no requests module found, install it with pip")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error: requesting the api resulted in status code %s' %
                        response.status_code)
    return response.text


"""
Output: Total ether across all addresses in the config class
Logic:
    - For every address
        - Request etherscan for balance
        - Add this balance to the total ether
    - Return the total ether
"""
def getTotalEther():
    import json
    totalEther = 0.0
    etherscanAPIKey = "V8ENE44FM98SCDPIXGGHQDFD2KCRSKJ8BJ"
    for address in getAddress("ether"):
        url = "https://api.etherscan.io/api?module=account&action=balance&address=" + \
            address + "&tag=latest&apikey=" + etherscanAPIKey
        response = json.loads(request(url))
        try:
            totalEther += float(response['result']) / pow(10, 18)
        except ValueError:
            raise ValueError('Error: ether address %s is invalid' % address)
    return totalEther


"""
Output: Total bitcoin across all addresses in the config class
Logic:
    - For every address
        - Request blockchain for balance
        - Add this balance to the total bitcoin
    - Return the total bitcoin
"""
def getTotalBitcoin():
    import json
    totalBitcoin = 0.0
    for address in getAddress("bitcoin"):
        url = "https://blockchain.info/rawaddr/" + address
        response = json.loads(request(url))
        try:
            totalBitcoin += float(response['final_balance']) / pow(10, 8)
        except ValueError:
            raise ValueError('Error: bitcoin address %s is invalid' % address)
    return totalBitcoin


"""
Output: Total litecoin across all addresses in the config class
Logic:
    - For every address
        - Request blockchain for balance
        - Add this balance to the total litecoin
    - Return the total litecoin
"""
def getTotalLitecoin():
    import json
    totalLitecoin = 0.0
    for address in getAddress("litecoin"):
        url = "https://chain.so/api/v2/get_address_balance/LTC/" + address
        response = json.loads(request(url))
        try:
            totalLitecoin += float(response['data']['confirmed_balance'])
        except ValueError:
            raise ValueError('Error: litecoin address %s is invalid' % address)
    return totalLitecoin


"""
Output: JSON response from coinmarketcap for information on specific cryptocurrency
Parameter cointype: query coinmarketcap about this specified cointype
Logic:
    - Request info from coinmarket cap
    - Ready the response for JSON parsing and return
"""
def queryCMC(coinType="ethereum"):
    import json
    url = "https://api.coinmarketcap.com/v1/ticker/" + coinType + "/?convert=" + config.fiatCurrency
    return json.loads(request(url))


"""
Output: Returns the type of data specified in returnData from the response
Parameter response: A coinmarketcap response generated by queryCMC
Parameter returnData: type of data to return about the cryptocurrency
Logic: Parse the JSON and return the specified data
"""
def parseCryptoData(response, returnData="ER"):
    returnData = returnData.upper()
    if returnData == "ER":
        return response[0]['price_' + config.fiatCurrency.lower()]
    elif returnData == "DV":
        return response[0]['24h_volume_' + config.fiatCurrency.lower()]
    elif returnData == "HP":
        return response[0]['percent_change_1h']
    elif returnData == "DP":
        return response[0]['percent_change_24h']
    elif returnData == "WP":
        return response[0]['percent_change_7d']
    else:
        raise ValueError('Error: attempting to access invalid field')


"""
Output: Total fiat currency
Parameter exchangeRate: Exchange rate for the cryptocurrency to fiat
Parameter coinType: Cryptocurrency type to get total fiat for
Logic:
    - Get total cryptocurrency balance
    - If exchange rate wasn't passed in then get it
    - Convert total cryptocurrency balance to fiat and return

"""
def getTotalFiat(exchangeRate="", coinType="ethereum"):
    if coinType == "ethereum":
        totalEther = getTotalEther()
        if exchangeRate == "":
            response = queryCMC("ethereum")
            exchangeRate = getCryptoData(response, "ER")
        return float(totalEther) * float(exchangeRate)
    elif coinType == "bitcoin":
        totalBitcoin = getTotalBitcoin()
        if exchangeRate == "":
            response = queryCMC("bitcoin")
            exchangeRate = getCryptoData(response, "ER")
        return float(totalBitcoin) * float(exchangeRate)
    elif coinType == "litecoin":
        totalLitecoin = getTotalLitecoin()
        if exchangeRate == "":
            response = queryCMC("litecoin")
            exchangeRate = getCryptoData(response, "ER")
        return float(totalLitecoin) * float(exchangeRate)
    else:
        raise ValueError("Error: invalid coin type")


"""
Output: Print all available data about a specific cryptocurrency and the respective config addresses
Parameter: Coin type to print data on
Logic:
    - Check valid coinType
    - Query coinmarketcap about coinType
    - Get the exchangeRate
    - Get the totalFiat using exchangeRate
    - Get the totalCrypto using exchangeRate and totalFiat
    - Print all available information to the console
"""
def printCryptoData(coinType):
    if coinType != "ethereum" and coinType != "bitcoin" and coinType != "litecoin":
        raise ValueError("Error: invalid coin type")
    response = queryCMC(coinType)
    exchangeRate = parseCryptoData(response, "ER")
    totalFiat = getTotalFiat(exchangeRate, coinType)
    totalCrypto = float(totalFiat) / float(exchangeRate)
    print "%s Price (%s): %s" % (coinType, config.fiatCurrency, exchangeRate)
    print "Daily Volume (%s): %s" % (config.fiatCurrency, parseCryptoData(response, "DV"))
    print "1 Hour Percent Change: %s%%" % parseCryptoData(response, "HP")
    print "1 Day Percent Change: %s%%" % parseCryptoData(response, "DP")
    print "1 Week Percent Change: %s%%" % parseCryptoData(response, "WP")
    print "Total %s: %s" % (coinType, totalCrypto)
    print "Total Fiat (%s): %s" % (config.fiatCurrency, totalFiat)


"""
Output: Prints out all crypo data about the 3 supported currencies
Logic: Print data about each currency one after another
"""
def printAllCryptoData():
    print
    printCryptoData("ethereum")
    print
    printCryptoData("bitcoin")
    print
    printCryptoData("litecoin")
    print
