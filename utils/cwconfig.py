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
"""Config Class to be shared throughout cryptowatch"""
class config(object):

    def __init__(self):

        self.etherAddress = ["0x585c4e1aa22d9Cc92d1a6b3fAe0c4a5274b5a884"] # ["0xea674fdde714fd979de3edf0f56aa9716b898ec8","0x585c4e1aa22d9Cc92d1a6b3fAe0c4a5274b5a884"]
        self.bitcoinAddress = ["1K7LpbNMHV5BZnj28XTianRaFZc5FwQpXr",
                               "1KJuLGpDoVMA4q4n6taDE2JVtnjkXhPYv2",
                               "1DvcjgkYntkQ8tqZDqHDz3nZ7dFL7U9VeR"]
        self.litecoinAddress = ["LYmpJZm1WrP5FSnxwkV2TTo5SkAF4Eha31"]
        self.fiatCurrency = "USD"
        pass
