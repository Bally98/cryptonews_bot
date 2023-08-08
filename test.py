import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json, hmac, hashlib, time, base64
from datetime import datetime, timedelta
import datetime as DT
from functions import create_text, push_post

okex_hike_names = ['', '', '']
okex_hike_price_changes = [0, 0, 0]


okex_drop_names = ['', '', '']
okex_drop_price_changes = [0, 0, 0]

url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
data_okex = requests.get(url_okex).json()
def cut(num):
    num = round(num, 2)
    return num

# for i in data_binance:
#     if 'BTC' in i['symbol']:
#         a += 1
# print(a)
# for i in data_coinbase['products']:
#     if 'UPI' in i['base_currency_id']:
#         print(i)
# for value_okex in data_okex['data']:
#     symbol_okex = value_okex['instId']
#     if symbol_okex.endswith('USDT') or symbol_okex.endswith('USDC') or symbol_okex.endswith('TUSD'):
#         x_index = value_okex['instId'].index('-')
#         if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[0]:
#             okex_hike_price_changes[2] = okex_hike_price_changes[1]
#             okex_hike_price_changes[1] = okex_hike_price_changes[0]
#             okex_hike_names[0] = str(value_okex['instId'][:x_index])
#             okex_hike_price_changes[0] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
#         elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[1]:
#             okex_hike_price_changes[2] = okex_hike_price_changes[1]
#             okex_hike_names[1] = str(value_okex['instId'][:x_index])
#             okex_hike_price_changes[1] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
#         elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[2]:
#             okex_hike_names[2] = str(value_okex['instId'][:x_index])
#             okex_hike_price_changes[2] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
#
#
#         elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[0]:
#             okex_drop_price_changes[2] = okex_drop_price_changes[1]
#             okex_drop_price_changes[1] = okex_drop_price_changes[0]
#             okex_drop_names[0] = str(value_okex['instId'][:x_index])
#             okex_drop_price_changes[0] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
#         elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[1]:
#             okex_drop_price_changes[2] = okex_drop_price_changes[1]
#             okex_drop_names[1] = str(value_okex['instId'][:x_index])
#             okex_drop_price_changes[1] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
#         elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[2]:
#             okex_drop_names[2] = str(value_okex['instId'][:x_index])
#             okex_drop_price_changes[2] = round(
#                 (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)




# c = [900, 6, 22]
# b = [9999999, 999999999999, 9999999999]
# for i in range(3):
#     if c[i] < b[0]:
#         b[2] = b[1]
#         b[1] = b[0]
#         b[0] = c[i]
#     elif c[i] < b[1]:
#         b[2] = b[1]
#         b[1] = c[i]
#     elif c[i] < b[2]:
#         b[2] = c[i]
# print(b)
secretKey_coinbase = 'RjPwUtqwix3h6Nr0ng9ekjHyJh53ZIJh'
timestamp = str(int(time.time()))
payload = timestamp + "GET" + "/api/v3/brokerage/products".split('?')[0] + ""
signature = hmac.new(secretKey_coinbase.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()
# headers_binance = {
#     'X-MBX-APIKEY': api_key_binance,
#     'X-MBX-SECRETKEY': api_secret_binance
# }
headers_coinbase = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': '3uvoymeXCMUqcfo2',
    'CB-ACCESS-SIGN': f'{signature.hex()}',
    'CB-ACCESS-TIMESTAMP': f'{timestamp}'
}
url_coinbase = "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"
data_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
cb_gain_names = ['', '', '']
cb_gain_price_changes = [0, 0, 0]
cb_gain_prices = [0, 0, 0]
cb_gain_vols = [0, 0, 0]

cb_los_names = ['', '', '']
cb_los_price_changes = [0, 0, 0]
cb_los_prices = [0, 0, 0]
cb_los_vols = [100000000000, 100000000000, 100000000000]
for value_cb in data_coinbase['products']:
    symbol_cb = str(value_cb['quote_currency_id'])
    if symbol_cb.endswith('USDT') or symbol_cb.endswith('USDC') or symbol_cb.endswith('TUSD'):
        if value_cb['price_percentage_change_24h'] != '':
            volume_cb = float(value_cb['volume_24h']) * float(value_cb['price'])
            if volume_cb > float(cb_gain_vols[0]):
                cb_gain_vols[2] = cb_gain_vols[1]
                cb_gain_vols[1] = cb_gain_vols[0]
                cb_gain_names[0] = str(value_cb['base_currency_id'])
                cb_gain_prices[0] = float(value_cb['price'])
                cb_gain_price_changes[0] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_gain_vols[0] = round(volume_cb)
            elif volume_cb > float(cb_gain_vols[1]):
                cb_gain_vols[2] = cb_gain_vols[1]
                cb_gain_names[1] = str(value_cb['base_currency_id'])
                cb_gain_prices[1] = float(value_cb['price'])
                cb_gain_price_changes[1] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_gain_vols[1] = round(volume_cb)
            elif volume_cb > float(cb_gain_vols[2]):
                cb_gain_names[2] = str(value_cb['base_currency_id'])
                cb_gain_prices[2] = float(value_cb['price'])
                cb_gain_price_changes[2] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_gain_vols[2] = volume_cb

            elif volume_cb < cb_los_vols[0]:
                cb_los_vols[2] = cb_los_vols[1]
                cb_los_vols[1] = cb_los_vols[0]
                cb_los_names[0] = str(value_cb['base_currency_id'])
                cb_los_prices[0] = float(value_cb['price'])
                cb_los_price_changes[0] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_los_vols[0] = round(volume_cb)
            elif volume_cb < cb_los_vols[1]:
                cb_los_vols[2] = cb_los_vols[1]
                cb_los_names[1] = str(value_cb['base_currency_id'])
                cb_los_prices[1] = float(value_cb['price'])
                cb_los_price_changes[1] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_los_vols[1] = round(volume_cb)
            elif volume_cb < cb_los_vols[2]:
                cb_los_names[2] = str(value_cb['base_currency_id'])
                cb_los_prices[2] = float(value_cb['price'])
                cb_los_price_changes[2] = round(float(value_cb['price_percentage_change_24h']), 3)
                cb_los_vols[2] = round(volume_cb)
print(cb_gain_names)
print(cb_gain_prices)
print(cb_gain_price_changes)
print(cb_gain_vols)
print()
print(cb_los_names)
print(cb_los_prices)
print(cb_los_price_changes)
print(cb_los_vols)


# for value_binance in data_binance:
#     symbol_binance = str(value_binance['symbol'])
#     # if value_binance['symbol'][:-4] == 'STRAX':
#     #     print(value_binance)
#
#     if symbol_binance.endswith('TUSD'):
#         binance_value = round(float(value_binance['quoteVolume']), 2)
#
#         if float(value_binance['quoteVolume']) > 0:
#             if binance_value > float(binance_gain_vols[0]):
#                 binance_gain_vols[2] = binance_gain_vols[1]
#                 binance_gain_vols[1] = binance_gain_vols[0]
#                 binance_gain_vols[0] = round(float(value_binance['quoteVolume']))
#                 binance_gain_names[0] = value_binance['symbol'][:-4]
#                 binance_gain_prices[0] = cut(float(value_binance['lastPrice']))
#                 binance_gain_price_changes[0] = float(value_binance['priceChangePercent'])
#             elif binance_value > float(binance_gain_vols[1]):
#                 binance_gain_vols[2] = binance_gain_vols[1]
#                 binance_gain_vols[1] = round(float(value_binance['quoteVolume']))
#                 binance_gain_names[1] = value_binance['symbol'][:-4]
#                 binance_gain_prices[1] = cut(float(value_binance['lastPrice']))
#                 binance_gain_price_changes[1] = float(value_binance['priceChangePercent'])
#             elif binance_value > float(binance_gain_vols[2]):
#                 binance_gain_vols[2] =  round(float(value_binance['quoteVolume']))
#                 binance_gain_names[2] = value_binance['symbol'][:-4]
#                 binance_gain_prices[2] = cut(float(value_binance['lastPrice']))
#                 binance_gain_price_changes[2] = float(value_binance['priceChangePercent'])
#
#             elif binance_value < float(binance_los_vols[0]):
#                 binance_los_vols[2] = binance_los_vols[1]
#                 binance_los_vols[1] = binance_los_vols[0]
#                 binance_los_vols[0] =  round(float(value_binance['quoteVolume']))
#                 binance_los_names[0] = value_binance['symbol'][:-4]
#                 binance_los_prices[0] = float(value_binance['lastPrice'])
#                 binance_los_price_changes[0] =float(value_binance['priceChangePercent'])
#             elif binance_value < float(binance_los_vols[1]):
#                 binance_los_vols[2] = binance_los_vols[1]
#                 binance_los_vols[1] = round(float(value_binance['quoteVolume']))
#                 binance_los_names[1] = value_binance['symbol'][:-4]
#                 binance_los_prices[1] = float(value_binance['lastPrice'])
#                 binance_los_price_changes[1] = float(value_binance['priceChangePercent'])
#             elif binance_value < float(binance_los_vols[2]):
#                 binance_los_vols[2] = round(float(value_binance['quoteVolume']))
#                 binance_los_names[2] = value_binance['symbol'][:-4]
#                 binance_los_prices[2] = float(value_binance['lastPrice'])
#                 binance_los_price_changes[2] = float(value_binance['priceChangePercent'])
#
# print(binance_gain_names)
# print(binance_gain_prices)
# print(binance_gain_vols)
# print(binance_los_names)
# print(binance_los_prices)
# print(binance_los_vols)




# url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
# headers_cmc = {
#     'X-CMC_PRO_API_KEY': api_key_cmc
# }
# params_cmc = {
#     'start': 1,
#     'limit': 50,
#     'convert': 'USD'
# }
# data_cmc_cap = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
# data_cmc = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
#
# top_names = ['', '', '']
# top_volumes_24h = [0, 0, 0]
#
# for cmc_value in data_cmc['data']:
#     percent_change = cmc_value['quote']['USD']['percent_change_24h']
#     if percent_change > top_volumes_24h[0]:
#         top_volumes_24h[2] = top_volumes_24h[1]
#         top_volumes_24h[1] = top_volumes_24h[0]
#         top_volumes_24h.insert(0, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
#         top_names.insert(0, cmc_value['name'])
#     elif percent_change > top_volumes_24h[1]:
#         top_volumes_24h[2] = top_volumes_24h[1]
#         top_volumes_24h.insert(1, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
#         top_names.insert(1, cmc_value['name'])
#     elif percent_change > top_volumes_24h[2]:
#         top_volumes_24h.insert(2, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
#         top_names.insert(2, cmc_value['name'])
# print(f'{top_names[0]}: {top_volumes_24h[0]}\n{top_names[1]}: {top_volumes_24h[1]}\n{top_names[2]}: {top_volumes_24h[2]}')
