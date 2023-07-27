import requests
import random
import math
from decimal import *

# random top3 from cmc
def get_3_biggest_crypto():
    top1_name = ''
    top2_name = ''
    top3_name = ''
    top1_volume_24h = 0
    top2_volume_24h = 0
    top3_volume_24h = 0

    api_key = '3c6565ce-18c1-4496-8727-02b12ece3299'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': 1,
        'limit': 5,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    # for i in data['data']:
    #
    #     if i['quote']['USD']['percent_change_24h'] > top1_volume_24h:
    #         top3_volume_24h = top2_volume_24h
    #         top2_volume_24h = top1_volume_24h
    #         top1_volume_24h = round(float(i['quote']['USD']['percent_change_24h']),2)
    #         top1_name = i['name']
    #     elif i['quote']['USD']['percent_change_24h'] > top2_volume_24h:
    #         top3_volume_24h = top2_volume_24h
    #         top2_volume_24h = round(float(i['quote']['USD']['percent_change_24h']),2)
    #         top2_name = i['name']
    #     elif i['quote']['USD']['percent_change_24h'] > top3_volume_24h:
    #         top3_volume_24h = round(float(i['quote']['USD']['percent_change_24h']),2)
    #         top3_name = i['name']
    # return print(f'Top 1 - {top1_name}:{top1_volume_24h}\nTop 2 - {top2_name}:'
    #              f'{top2_volume_24h}\nTop 3 - {top3_name}:{top3_volume_24h}\n ')
    top_caps = [[], [], [], [], []]
    def top_5_cap():

        for top5 in range(5):
            top_caps[top5].insert(0, str(data['data'][top5]['symbol']))
            top_caps[top5].insert(1, str(data['data'][top5]['quote']['USD']['price']))
            top_caps[top5].insert(2, str(data['data'][top5]['quote']['USD']['percent_change_24h']))
            top_caps[top5].insert(3, str(data['data'][top5]['quote']['USD']['volume_24h']))
        return print(top_caps)
    top_5_cap()




















get_3_biggest_crypto()





















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
