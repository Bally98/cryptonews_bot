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
    def round_num(num):
        num = round(num, 2)
        return num

    billion_cap = ''
    billion_vol = ''

    res = requests.get(url, params=parameters, headers=headers)
    res = res.json()
    price = str(res['data'][f'{symbol}']['quote']['USD']['price'])[:9]
    price = round_num(float(price))
    cap = res['data'][f'{symbol}']['quote']['USD']['market_cap']
    vol_24 = res['data'][f'{symbol}']['quote']['USD']['volume_24h']
    percent_change = round(res['data'][f'{symbol}']['quote']['USD']['percent_change_24h'], 3)
    cap_dominance = res['data'][f'{symbol}']['quote']['USD']['market_cap_dominance']
    if float(vol_24) > 999999999:
        vol_24 = vol_24 / 1e9
        billion_vol = 'Billion'
    else:
        vol_24 = vol_24 / 1e6
        billion_vol = 'Million'
    vol_24 = round_num(vol_24)
    if float(cap) > 999999999:
        cap = cap / 1e9
        billion_cap = 'Billion'
    else:
        cap = cap / 1e6
        billion_cap = 'Million'
    cap = round_num(cap)

    print(f'{symbol}',f'Price: {price}$', f'Capitalisation: {cap} {billion_cap}$', f'Volume 24h: {vol_24} {billion_vol}$', f'Percent change 24h: {percent_change}%',
          f'Capitalisation dominance: {cap_dominance}%', sep='\n')

get_data_cmc('BTC')
print()
get_data_cmc('ETH')
print()
get_data_cmc('ADA')
print()
get_data_cmc('RPL')
print()
get_data_cmc('GALA')
print()
get_data_cmc('SUI')
#
#

