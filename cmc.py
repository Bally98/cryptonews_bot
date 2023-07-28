import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
def get_data_cmc(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol':f'{symbol}',
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '3c6565ce-18c1-4496-8727-02b12ece3299',
    }
    res = requests.get(url, params=parameters, headers=headers)
    res = res.json()
    return print(float(round(res['data'][f'{symbol}']['quote']['USD']['market_cap'])))
get_data_cmc('ACM')

# ACM
# VGX
# SSWP