import requests
import random
import math
from decimal import *

# random top3 from cmc
def get_top_10_currencies():
    api_key = '3c6565ce-18c1-4496-8727-02b12ece3299'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': 1,
        'limit': 30,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    top_30 = data['data']
    price_list = [i['quote']['USD']['price'] for i in top_30]
    price_list_2 = []
    price_list_3 = []
    for i in price_list:
        with localcontext(Context(prec=32, rounding=ROUND_05UP,
                                  Emin=0, Emax=0, clamp=1, capitals=0)):
            i = Decimal(str(i))
            price_list_2.append(str(i))
    for j in range(30):
        if len(price_list_2[j]) > 22:
            x = price_list_2[j][:9]
            price_list_3.append(x)
        else:
            x = price_list_2[j][:7]
            price_list_3.append(x)
    name_list = [i['name'] for i in top_30]
    change_list = [round(i['quote']['USD']['percent_change_24h'],2) for i in top_30]
    volume_list = [round(i['quote']['USD']['volume_24h'],2) for i in top_30]
    # print(name_list)
    # print(price_list_3)
    # print(volume_list)
    # print(change_list)
    for value in range(3):
        x = random.randint(0 ,29)
        print(f'{name_list[x]} \nPrice: {price_list_3[x]}$\nVolume 24h: '
              f'{volume_list[x]}$\nChange 24h: {change_list[x]}%\n')
get_top_10_currencies()




















def get_top_10_currencies(comand):
    name_list = []
    change_list = []
    api_key = '3c6565ce-18c1-4496-8727-02b12ece3299'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': 1,
        'limit': 30,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    top_30 = data['data']
    if comand == 'change':
        print("Топ-30 валют по объёму за 24 часа на CoinMarketCap:")
        for i in top_30:
            i['quote']['USD']['percent_change_24h'] = round(i['quote']['USD']['percent_change_24h'], 2)
            print(f"{i['symbol']} Volume 24h: {i['quote']['USD']['percent_change_24h']}%")
    elif comand == 'cap':
        print("Топ-30 валют по капитализации на CoinMarketCap:")
        for currency in top_30:
            currency['quote']['USD']['market_cap'] = currency['quote']['USD']['market_cap'] / 1e9
            currency['quote']['USD']['market_cap'] = round(currency['quote']['USD']['market_cap'], 2)
            print(f"{currency['symbol']} Капитализация: {currency['quote']['USD']['market_cap']} Миллиард $")
# get_top_10_currencies('change')
#
