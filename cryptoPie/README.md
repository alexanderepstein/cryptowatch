# CryptoPie
###### CryptoPie is the Raspberry Pi Cryptowatch monitor

## Circuit
The code for cryptoPie is based around a 16x2 LCD screen.

My screen broke just before I went to test this... so let me know of any issues and I will look to test myself when a new screen comes in.

However by setting the size of screen in ```cryptowatch --config``` should allow you to use other screen size as well with no trouble at all.

I am using a Raspberry Pi 2 Model B V1.1.

Other models may be used but if the GPIO layout needs adjusting make sure to setup the correct GPIO variables in ```cryptowatch --config```

<img src="https://s26.postimg.org/4u2qontnt/Cryptowatch_First_Circuit.png" height="600px" width="700px" align= "center">

In between LCD Backlight +5V I used a 1k ohm resistor to prevent overpowering the backlight this may not be necessary but for the first attempt is definitely a good idea.

## Usage

* After installing cryptowatch run ```cryptowatch --config``` and setup your account addresses.
* Make sure the circuit is wired identical to the picture or that you have changed the config file respectively.
* Run ```cryptowatch --monitor pie``` or ```cryptowatch --monitor rpi``` to run cryptoPie
* Profit???

## License

MIT License

Copyright (c) 2017 Alex Epstein

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
