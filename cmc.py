import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
def get_data_cmc(symbol):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}'

    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '3c6565ce-18c1-4496-8727-02b12ece3299',
    }
    res = requests.get(url,  headers=headers)
    res = res.json()
    # if res['data'][f'{symbol}']['quote']['USD']['market_cap'] == 0 or '0':
    #     return print(float(round(res['data'][f'{symbol}']['quote']['USD']['fully_diluted_market_cap'])))
    # else:
    #     return print(float(round(res['data'][f'{symbol}']['quote']['USD']['market_cap'])))
    print(res['data'][f'{symbol}']['symbol'])
    return print(float(round(res['data'][f'{symbol}']['quote']['USD']['market_cap'])))
    # return print(res)
get_data_cmc('SKEB')
get_data_cmc('SSWP')
# SKEB
# SSWP

# ACM
# VGX
# SSWP