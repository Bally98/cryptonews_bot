import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
url_binance = 'https://api.binance.com/api/v3/ticker/24hr'
url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

api_key = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
api_secret = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'
symbol = 'BTC'
params = {
    'symbol': symbol,
}
headers_123 = {
    'X-MBX-APIKEY': api_key,
    'X-MBX-SECRETKEY': api_secret
}
api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
data_binance = requests.get(url_binance, headers= headers_123).json()
okex_hike_name = ''
okex_hike_percent_change = 0
okex_hike_cap = 0
okex_drop_name = ''
okex_drop_percent_change = 999
okex_drop_cap = 0
binance_hike_name = ''
binance_hike_percent_change = 0
binance_hike_cap = 0
binance_drop_name = ''
binance_drop_percent_change = 999
binance_drop_cap = 0
data_okex = requests.get(url_okex).json()
params_cmc = {
        'start': 1,
        'limit': 50,
        'convert': 'USD'
    }
headers_cmc = {
        'X-CMC_PRO_API_KEY': api_key_cmc
    }

def get_cap_cmc(coin):

    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '3c6565ce-18c1-4496-8727-02b12ece3299',
    }
    url_cmc_cap = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin}'
    data_cmc_cap = requests.get(url_cmc_cap,  headers=headers).json()
    if float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap'])) == 0 or '0':
        return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['fully_diluted_market_cap']))
    else:
        return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap']))
    # return data_cmc_cap

#
for value_okex in data_okex['data']:
    symbol_okex = value_okex['instId']
    if symbol_okex.endswith('USDT') or symbol_okex.endswith('USDC'):
        if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_percent_change:
            x = value_okex['instId'].index('-')
            okex_hike_name = str(value_okex['instId'][:x])
            okex_hike_percent_change = round(
                (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            okex_hike_cap = get_cap_cmc(okex_hike_name)
        if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_percent_change:
            x = value_okex['instId'].index('-')
            okex_drop_name = str(value_okex['instId'][:x])
            okex_drop_percent_change = round(
                (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            okex_drop_cap = get_cap_cmc(okex_drop_name)
for value_binance in data_binance:
    symbol_binance = str(value_binance['symbol'])
    if symbol_binance.endswith('USDT'):
        if float(value_binance['priceChangePercent']) > binance_hike_percent_change:
            binance_hike_name = value_binance['symbol'][:-4]
            binance_hike_percent_change = float(value_binance['priceChangePercent'])
            binance_hike_cap = get_cap_cmc(binance_hike_name)
        if float(value_binance['priceChangePercent']) < binance_drop_percent_change:
            binance_drop_name = value_binance['symbol'][:-4]
            binance_drop_percent_change = float(value_binance['priceChangePercent'])
            binance_drop_cap = get_cap_cmc(binance_drop_name)
print(binance_hike_name, binance_hike_percent_change, binance_hike_cap,'\n',binance_drop_name, binance_drop_percent_change,binance_drop_cap)
print(okex_hike_name,okex_hike_cap, okex_drop_name,okex_drop_cap, sep='\n')
# print(binance_hike_name,binance_drop_name,binance_hike_cap, binance_drop_cap, sep='\n')








