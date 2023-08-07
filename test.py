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




url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
headers_cmc = {
    'X-CMC_PRO_API_KEY': api_key_cmc
}
params_cmc = {
    'start': 1,
    'limit': 50,
    'convert': 'USD'
}
data_cmc_cap = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
data_cmc = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()

top_names = ['', '', '']
top_volumes_24h = [0, 0, 0]

for cmc_value in data_cmc['data']:
    percent_change = cmc_value['quote']['USD']['percent_change_24h']
    if percent_change > top_volumes_24h[0]:
        top_volumes_24h[2] = top_volumes_24h[1]
        top_volumes_24h[1] = top_volumes_24h[0]
        top_volumes_24h.insert(0, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
        top_names.insert(0, cmc_value['name'])
    elif percent_change > top_volumes_24h[1]:
        top_volumes_24h[2] = top_volumes_24h[1]
        top_volumes_24h.insert(1, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
        top_names.insert(1, cmc_value['name'])
    elif percent_change > top_volumes_24h[2]:
        top_volumes_24h.insert(2, round(float(cmc_value['quote']['USD']['percent_change_24h']), 2))
        top_names.insert(2, cmc_value['name'])
# print(f'{top_names[0]}: {top_volumes_24h[0]}\n{top_names[1]}: {top_volumes_24h[1]}\n{top_names[2]}: {top_volumes_24h[2]}')

top3 = ''

for i in range(3):
    top3 += f"<li>{top_names[i]} - {top_volumes_24h[i]}%</li>"

print(top3)

binance_top2_gain_name = ''
binance_top2_gain_price_change = 0
binance_top2_gain_price = 0
binance_top2_gain_vol = 0

binance_top2_los_name = ''
binance_top2_los_price_change = 0
binance_top2_los_price = 0
binance_top2_los_vol = 999999999

binance_top3_gain_name = ''
binance_top3_gain_price_change = 0
binance_top3_gain_price = 0
binance_top3_gain_vol = 0

binance_top3_los_name = ''
binance_top3_los_price_change = 0
binance_top3_los_price = 0
binance_top3_los_vol = 999999999

gain_los_names = []
gain_los_price = []
gain_los_change = []
gain_los_vol = []

cb_top1_gain_name = ''
cb_top1_gain_price_change = 0
cb_top1_gain_price = 0
cb_top1_gain_vol = 0

cb_top1_los_name = ''
cb_top1_los_price_change = 0
cb_top1_los_price = 0
cb_top1_los_vol = 999999999

cb_top2_gain_name = ''
cb_top2_gain_price_change = 0
cb_top2_gain_price = 0
cb_top2_gain_vol = 0

cb_top2_los_name = ''
cb_top2_los_price_change = 0
cb_top2_los_price = 0
cb_top2_los_vol = 999999999

cb_top3_gain_name = ''
cb_top3_gain_price_change = 0
cb_top3_gain_price = 0
cb_top3_gain_vol = 0

cb_top3_los_name = ''
cb_top3_los_price_change = 0
cb_top3_los_price = 0
cb_top3_los_vol = 999999999

okex_top1_gain_name = ''
okex_top1_gain_price = 0
okex_top1_gain_price_change = 0
okex_top1_gain_vol = 0

okex_top1_los_name = ''
okex_top1_los_price = 0
okex_top1_los_price_change = 0
okex_top1_los_vol = 999999999

okex_top2_gain_name = ''
okex_top2_gain_price = 0
okex_top2_gain_price_change = 0
okex_top2_gain_vol = 0

okex_top2_los_name = ''
okex_top2_los_price = 0
okex_top2_los_price_change = 0
okex_top2_los_vol = 999999999

okex_top3_gain_name = ''
okex_top3_gain_price = 0
okex_top3_gain_price_change = 0
okex_top3_gain_vol = 0

okex_top3_los_name = ''
okex_top3_los_price = 0
okex_top3_los_price_change = 0
okex_top3_los_vol = 999999999