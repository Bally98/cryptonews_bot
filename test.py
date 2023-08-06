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
top1_name = ''
top2_name = ''
top3_name = ''
top1_volume_24h = 0
top2_volume_24h = 0
top3_volume_24h = 0

los1_name = ''
los2_name = ''
los3_name = ''
los1_volume_24h = 0
los2_volume_24h = 0
los3_volume_24h = 0

for cmc_value in data_cmc['data']:
    percent_change = cmc_value['quote']['USD']['percent_change_24h']
    if percent_change > top1_volume_24h:
        top3_volume_24h = top2_volume_24h
        top2_volume_24h = top1_volume_24h
        top1_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        top1_name = cmc_value['name']
    elif percent_change > top2_volume_24h:
        top3_volume_24h = top2_volume_24h
        top2_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        top2_name = cmc_value['name']
    elif percent_change > top3_volume_24h:
        top3_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        top3_name = cmc_value['name']
    elif percent_change < los2_volume_24h:
        los3_volume_24h = los2_volume_24h
        los2_volume_24h = los1_volume_24h
        los1_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        los1_name = cmc_value['name']
    elif percent_change < los2_volume_24h:
        los3_volume_24h = los2_volume_24h
        los2_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        los2_name = cmc_value['quote']['USD']['percent_change_24h']
    elif percent_change < los3_volume_24h:
        los3_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
        los3_name = cmc_value['name']
print(f'{top1_name}: {top1_volume_24h}\n{top2_name}: {top2_volume_24h}\n{top3_name}: {top3_volume_24h}')
print(f'{los1_name}: {los1_volume_24h}\n{los2_name}: {los2_volume_24h}\n{los3_name}: {los3_volume_24h}')



