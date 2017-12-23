# CryptoUtils
## Usage
```python
import cryptoUtils.cryptoUtils as crypto
crypto.get_total_crypto()
```
## Documentation on methods


```python
request(url)

Output: JSON ready response from the server

Parameter url: url to request

Logic:
* Request the url
* Check for successful status code from server
* Return the JSON response
```

```python
clear()

Output: Clears the terminal

Logic:
    - We just want to know how to clear the terminal
    - Check the platform type
    - Clear the terminal in the right way
```

```python
get_total_crypto(coinType)


Output: Total crypto across all addresses in the config class

Parameters:
    - Cointype: Which coin do you want the total crypto for

Logic:
    - Start with 0 total crypto
    - For every respective address in the config file
        - Request respective api for balance
        - Add this balance to the total crypto
    - Return the total crypto
```

```python
get_crypto_info(coinType, colored=False)


Output: Array of metrics related to the respective coin type

Parameters
    - Cointype: query coinmarketcap about this specified cointype
    - Colored: Do we want the colored version of the output (only when sending to terminal do we want this)

Logic:
    - Request info from coinmarket cap
    - Ready the response for JSON parsing
    - Parse the response and append each peice of info to the metrics array
    - Return the metrics array
```

```python
get_crypto_table(clearConsole=False, colored=False)

Output: Returns an ascii table for all cryptocurrencies and their data

Parameters:
    - clearConsole: Do we want to clear the console before returning this data (we do want to do this when running in monitor mode)
    - Colored: Do we want the table to be colored

Logic:
    - Create header
    - Get metrics on each legal currency and insert into their own array
    - Get the total fiat by adding the last index of each metrics array together
    - Insert cointypes into the respective array
    - Combine the header and the crypoto metrics into one big metrics array
    - Create the ascii table from this data and return it
```

# Config Class

## Usage

```python
import cryptoUtils.cwconfig as cfg
config = cfg.config()
config.etherAddress
```
## Methods

```python
openFile(self,filePath)
Opens the specified file in a text editor
```
```python
edit(self)
Calls the openFile method for the config file
```
```python
createConfigFile(self)
Checks if the config file exists, if not create it and format the file
```
## Properties:
* ###### Cryptocurrency Addresses
* ###### GPIO Variables
* ###### LCD Screen Variables
