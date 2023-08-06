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
def main():
    url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url_binance = 'https://api.binance.com/api/v3/ticker/24hr'
    url_coinbase = "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"
    url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

    api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
    secretKey_coinbase = 'RjPwUtqwix3h6Nr0ng9ekjHyJh53ZIJh'
    api_key_binance = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
    api_secret_binance = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'

    timestamp = str(int(time.time()))
    payload = timestamp + "GET" + "/api/v3/brokerage/products".split('?')[0] + ""
    signature = hmac.new(secretKey_coinbase.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()
    headers_binance = {
            'X-MBX-APIKEY': api_key_binance,
            'X-MBX-SECRETKEY': api_secret_binance
        }
    headers_coinbase = {
        'Content-Type': 'application/json',
        'CB-ACCESS-KEY': '3uvoymeXCMUqcfo2',
        'CB-ACCESS-SIGN': f'{signature.hex()}',
        'CB-ACCESS-TIMESTAMP': f'{timestamp}'
    }
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
    data_binance = requests.get(url_binance, headers=headers_binance).json()
    data_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
    data_okex = requests.get(url_okex).json()

    def get_cap_cmc(coin):
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '3c6565ce-18c1-4496-8727-02b12ece3299',
        }
        url_cmc_cap = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin}'
        data_cmc_cap = requests.get(url_cmc_cap, headers=headers).json()
        if float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap'])) == 0 or '0':
            return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['fully_diluted_market_cap']))
        else:
            return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap']))

    def cut(num):
        num = round(num, 2)
        return num

    def format_number(num):
        formatted_num = "{:,.0f}".format(num).replace(',', '.')
        return formatted_num

    top1_name = ''
    top2_name = ''
    top3_name = ''
    top1_volume_24h = 0
    top2_volume_24h = 0
    top3_volume_24h = 0

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

        binance_top1_gain_name = ''
        binance_top1_gain_price_change = 0
        binance_top1_gain_price = 0
        binance_top1_gain_vol = 0
        binance_top1_los_name = ''
        binance_top1_los_price_change = 0
        binance_top1_los_price = 0
        binance_top1_los_vol = 999999999

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

    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT') or symbol_binance.endswith('USDC'):
            if float(value_binance['quoteVolume']) > 0:
                if round(float(value_binance['quoteVolume']), 2) > float(binance_top1_gain_vol):
                    binance_top3_gain_vol = binance_top2_gain_vol
                    binance_top2_gain_vol = binance_top1_gain_vol
                    binance_top1_gain_vol = round(float(value_binance['quoteVolume']))
                    binance_top1_gain_name = value_binance['symbol'][:-4]
                    binance_top1_gain_price = cut(float(value_binance['lastPrice']))
                    binance_top1_gain_price_change = float(value_binance['priceChangePercent'])
                elif round(float(value_binance['quoteVolume']), 2) > float(binance_top2_gain_vol):
                    binance_top3_gain_vol = binance_top2_gain_vol
                    binance_top2_gain_vol = round(float(value_binance['quoteVolume']))
                    binance_top2_gain_name = value_binance['symbol'][:-4]
                    binance_top2_gain_price = cut(float(value_binance['lastPrice']))
                    binance_top2_gain_price_change = float(value_binance['priceChangePercent'])
                elif round(float(value_binance['quoteVolume']), 2) > float(binance_top3_gain_vol):
                    binance_top3_gain_vol = round(float(value_binance['quoteVolume']))
                    binance_top3_gain_name = value_binance['symbol'][:-4]
                    binance_top3_gain_price = cut(float(value_binance['lastPrice']))
                    binance_top3_gain_price_change = float(value_binance['priceChangePercent'])
                elif round(float(value_binance['quoteVolume']), 2) < float(binance_top1_los_vol):
                    binance_top3_los_vol = binance_top2_los_vol
                    binance_top2_los_vol = binance_top1_los_vol
                    binance_top1_los_vol = round(float(value_binance['quoteVolume']))
                    binance_top1_los_name = value_binance['symbol'][:-4]
                    binance_top1_los_price = cut(float(value_binance['lastPrice']))
                    binance_top1_los_price_change = float(value_binance['priceChangePercent'])
                elif round(float(value_binance['quoteVolume']), 2) < float(binance_top2_los_vol):
                    binance_top3_los_vol = binance_top2_los_vol
                    binance_top2_los_vol = round(float(value_binance['quoteVolume']))
                    binance_top2_los_name = value_binance['symbol'][:-4]
                    binance_top2_los_price = cut(float(value_binance['lastPrice']))
                    binance_top2_los_price_change = float(value_binance['priceChangePercent'])
                elif round(float(value_binance['quoteVolume']), 2) < float(binance_top3_los_vol):
                    binance_top3_los_vol = round(float(value_binance['quoteVolume']))
                    binance_top3_los_name = value_binance['symbol'][:-4]
                    binance_top3_los_price = cut(float(value_binance['lastPrice']))
                    binance_top3_los_price_change = float(value_binance['priceChangePercent'])
    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT') or symbol_binance.endswith('USDC'):
            if value_cb['price_percentage_change_24h'] != '':
                volume_cb = float(value_cb['volume_24h']) * float(value_cb['price'])
                if float(value_cb['price']) > 0:
                    if volume_cb > cb_top1_gain_vol:
                        cb_top3_gain_vol = cb_top2_gain_vol
                        cb_top2_gain_vol = cb_top1_gain_vol
                        cb_top1_gain_name = str(value_cb['base_currency_id'])
                        cb_top1_gain_price = float(value_cb['price'])
                        cb_top1_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top1_gain_vol = round(volume_cb)
                    elif volume_cb > cb_top2_gain_vol:
                        cb_top3_gain_vol = cb_top2_gain_vol
                        cb_top2_gain_name = str(value_cb['base_currency_id'])
                        cb_top2_gain_price = float(value_cb['price'])
                        cb_top2_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top2_gain_vol = round(volume_cb)
                    elif volume_cb > cb_top3_gain_vol:
                        cb_top3_gain_name = str(value_cb['base_currency_id'])
                        cb_top3_gain_price = float(value_cb['price'])
                        cb_top3_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top3_gain_vol = round(volume_cb)
                    elif volume_cb < cb_top1_gain_vol:
                        cb_top3_los_vol = cb_top2_los_vol
                        cb_top2_los_vol = cb_top1_los_vol
                        cb_top1_los_name = str(value_cb['base_currency_id'])
                        cb_top1_los_price = round(float(value_cb['price']), 4)
                        cb_top1_los_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top1_los_vol = cut(volume_cb)
                    elif volume_cb < cb_top2_gain_vol:
                        cb_top3_los_vol = cb_top2_los_vol
                        cb_top2_los_name = str(value_cb['base_currency_id'])
                        cb_top2_los_price = float(value_cb['price'])
                        cb_top2_los_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top2_los_vol = round(volume_cb)
                    elif volume_cb < cb_top3_los_vol:
                        cb_top3_los_name = str(value_cb['base_currency_id'])
                        cb_top3_los_price = float(value_cb['price'])
                        cb_top3_los_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top3_los_vol = round(volume_cb)
    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_binance.endswith('USDC'):
            if float(value_okex['last']) > 0 :
                x = value_okex['instId'].index('-')
                if float(value_okex['volCcy24h']) > okex_top1_gain_vol:
                    okex_top3_gain_vol = okex_top2_gain_vol
                    okex_top2_gain_vol = okex_top1_gain_vol
                    okex_top1_gain_name = str(value_okex['instId'][:x])
                    okex_top1_gain_price = cut(float(value_okex['last']))
                    okex_top1_gain_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top1_gain_vol = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) > okex_top2_gain_vol:
                    okex_top3_gain_vol = okex_top2_gain_vol
                    okex_top2_gain_name = str(value_okex['instId'][:x])
                    okex_top2_gain_price = cut(float(value_okex['last']))
                    okex_top2_gain_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top2_gain_vol = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) > okex_top3_gain_vol:
                    okex_top3_gain_name = str(value_okex['instId'][:x])
                    okex_top3_gain_price = cut(float(value_okex['last']))
                    okex_top3_gain_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top3_gain_vol = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) < okex_top1_los_vol:
                    okex_top3_los_vol = okex_top2_los_vol
                    okex_top2_los_vol = okex_top1_los_vol
                    okex_top1_los_name = str(value_okex['instId'][:x])
                    okex_top1_los_price = cut(float(value_okex['last']))
                    okex_top1_los_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top1_los_vol = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) < okex_top2_los_vol:
                    okex_top3_los_vol = okex_top2_los_vol
                    okex_top2_los_name = str(value_okex['instId'][:x])
                    okex_top2_los_price = cut(float(value_okex['last']))
                    okex_top2_los_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top2_los_vol = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) < okex_top3_los_vol:
                    okex_top3_los_name = str(value_okex['instId'][:x])
                    okex_top3_los_price = cut(float(value_okex['last']))
                    okex_top3_los_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top3_los_vol = round(float(value_okex['volCcy24h']))
    binance1_hike_name = ''
    binance1_hike_percent_change = 0
    binance1_hike_cap = 0
    binance1_drop_name = ''
    binance1_drop_percent_change = 999
    binance1_drop_cap = 0

    binance2_hike_name = ''
    binance2_hike_percent_change = 0
    binance2_hike_cap = 0
    binance2_drop_name = ''
    binance2_drop_percent_change = 999
    binance2_drop_cap = 0

    binance3_hike_name = ''
    binance3_hike_percent_change = 0
    binance3_hike_cap = 0
    binance3_drop_name = ''
    binance3_drop_percent_change = 999
    binance3_drop_cap = 0

    cb1_hike_name = ''
    cb1_hike_percent_change = 0
    cb_hike_cap = 0
    cb1_drop_name = ''
    cb1_drop_percent_change = 999
    cb1_drop_cap = 0

    cb2_hike_name = ''
    cb2_hike_percent_change = 0
    cb2_hike_cap = 0
    cb2_drop_name = ''
    cb2_drop_percent_change = 999
    cb2_drop_cap = 0

    cb3_hike_name = ''
    cb3_hike_percent_change = 0
    cb3_hike_cap = 0
    cb3_drop_name = ''
    cb3_drop_percent_change = 999
    cb3_drop_cap = 0

    okex1_hike_name = ''
    okex1_hike_percent_change = 0
    okex1_hike_cap = 0
    okex1_drop_name = ''
    okex1_drop_percent_change = 999
    okex1_drop_cap = 0

    okex2_hike_name = ''
    okex2_hike_percent_change = 0
    okex2_hike_cap = 0
    okex2_drop_name = ''
    okex2_drop_percent_change = 999
    okex2_drop_cap = 0

    okex3_hike_name = ''
    okex3_hike_percent_change = 0
    okex3_hike_cap = 0
    okex3_drop_name = ''
    okex3_drop_percent_change = 999
    okex3_drop_cap = 0

    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT') or symbol_binance.endswith('USDC'):
            if float(value_binance['priceChangePercent']) > binance1_hike_percent_change:
                binance3_hike_percent_change = binance2_hike_percent_change
                binance2_hike_percent_change = binance1_hike_percent_change
                binance1_hike_name = value_binance['symbol'][:-4]
                binance1_hike_percent_change = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) > binance2_hike_percent_change:
                binance3_hike_percent_change = binance2_hike_percent_change
                binance2_hike_name = value_binance['symbol'][:-4]
                binance2_hike_percent_change = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) > binance3_hike_percent_change:
                binance3_hike_name = value_binance['symbol'][:-4]
                binance3_hike_percent_change = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance1_drop_percent_change:
                binance3_drop_percent_change = binance2_drop_percent_change
                binance2_drop_percent_change = binance1_drop_percent_change
                binance1_drop_name = value_binance['symbol'][:-4]
                binance1_drop_percent_change = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance2_drop_percent_change:
                binance3_drop_percent_change = binance2_drop_percent_change
                binance2_drop_name = value_binance['symbol'][:-4]
                binance2_drop_percent_change = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance3_drop_percent_change:
                binance3_hike_name = value_binance['symbol'][:-4]
                binance3_hike_percent_change = float(value_binance['priceChangePercent'])
    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT') or symbol_cb.endswith('USDC'):
            if value_cb['price_percentage_change_24h'] != '':
                percent = float(value_cb['price_percentage_change_24h'])
                if percent > cb1_hike_percent_change:
                    cb3_hike_percent_change = cb2_hike_percent_change
                    cb2_hike_percent_change = cb1_hike_percent_change
                    cb1_hike_name = str(value_cb['base_currency_id'])
                    cb1_hike_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent > cb2_hike_percent_change:
                    cb3_hike_percent_change = cb2_hike_percent_change
                    cb2_hike_name = str(value_cb['base_currency_id'])
                    cb2_hike_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent > cb3_hike_percent_change:
                    cb3_hike_name = str(value_cb['base_currency_id'])
                    cb3_hike_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent < cb1_drop_percent_change:
                    cb3_dro_percent_change = cb2_dro_percent_change
                    cb2_dro_percent_change = cb1_dro_percent_change
                    cb1_drop_name = str(value_cb['base_currency_id'])
                    cb1_drop_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent < cb2_drop_percent_change:
                    cb3_drop_percent_change = cb2_drop_percent_change
                    cb2_drop_name = str(value_cb['base_currency_id'])
                    cb2_drop_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent < cb3_drop_percent_change:
                    cb3_drop_name = str(value_cb['base_currency_id'])
                    cb3_drop_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_okex.endswith('USDC'):
            x_index = value_okex['instId'].index('-')
            if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex1_hike_percent_change:
                okex3_hike_percent_change = okex2_hike_percent_change
                okex2_hike_percent_change = okex1_hike_percent_change
                okex1_hike_name = str(value_okex['instId'][:x_index])
                okex1_hike_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex2_hike_percent_change:
                okex3_hike_percent_change = okex2_hike_percent_change
                okex2_hike_name = str(value_okex['instId'][:x_index])
                okex2_hike_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex3_hike_percent_change:
                okex3_hike_name = str(value_okex['instId'][:x_index])
                okex3_hike_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex1_drop_percent_change:
                okex3_drop_percent_change = okex2_drop_percent_change
                okex2_drop_percent_change = okex1_drop_percent_change
                okex1_drop_name = str(value_okex['instId'][:x_index])
                okex1_drop_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex2_drop_percent_change:
                okex3_drop_percent_change = okex2_drop_percent_change
                okex2_drop_name = str(value_okex['instId'][:x_index])
                okex2_drop_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex3_drop_percent_change:
                okex3_drop_name = str(value_okex['instId'][:x_index])
                okex3_drop_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)


    binance1_hike_cap = format_number(get_cap_cmc(binance1_hike_name))
    binance2_hike_cap = format_number(get_cap_cmc(binance2_hike_name))
    binance3_hike_cap = format_number(get_cap_cmc(binance3_hike_name))

    binance1_drop_cap = format_number(get_cap_cmc(binance1_drop_name))
    binance2_drop_cap = format_number(get_cap_cmc(binance2_drop_name))
    binance3_drop_cap = format_number(get_cap_cmc(binance3_drop_name))

    cb1_hike_cap = format_number(get_cap_cmc(cb1_hike_name))
    cb2_hike_cap = format_number(get_cap_cmc(cb2_hike_name))
    cb3_hike_cap = format_number(get_cap_cmc(cb3_hike_name))

    cb1_drop_cap = format_number(get_cap_cmc(cb1_drop_name))
    cb2_drop_cap = format_number(get_cap_cmc(cb_drop_name))
    cb3_drop_cap = format_number(get_cap_cmc(cb_drop_name))

    okex1_hike_cap = format_number(get_cap_cmc(okex1_hike_name))
    okex2_hike_cap = format_number(get_cap_cmc(okex2_hike_name))
    okex3_hike_cap = format_number(get_cap_cmc(okex3_hike_name))

    okex1_drop_cap = format_number(get_cap_cmc(okex1_drop_name))
    okex2_drop_cap = format_number(get_cap_cmc(okex2_drop_name))
    okex3_drop_cap = format_number(get_cap_cmc(okex3_drop_name))

    binance_top1_gain_vol = format_number(binance_top1_gain_vol)
    binance_top2_gain_vol = format_number(binance_top2_gain_vol)
    binance_top3_gain_vol = format_number(binance_top3_gain_vol)

    binance_top1_los_vol = format_number(binance_top1_los_vol)
    binance_top1_los_vol = format_number(binance_top2_los_vol)
    binance_top1_los_vol = format_number(binance_top3_los_vol)

    cb_top1_gain_vol = format_number(cb_top1_gain_vol)
    cb_top2_gain_vol = format_number(cb_top2_gain_vol)
    cb_top3_gain_vol = format_number(cb_top3_gain_vol)

    cb_top1_los_vol = format_number(cb_top1_los_vol)
    cb_top2_los_vol = format_number(cb_top2_los_vol)
    cb_top3_los_vol = format_number(cb_top3_los_vol)

    okex_top1_gain_vol = format_number(okex_top1_gain_vol)
    okex_top2_gain_vol = format_number(okex_top2_gain_vol)
    okex_top3_gain_vol = format_number(okex_top3_gain_vol)

    okex_top1_los_vol = format_number(okex_top1_los_vol)
    okex_top2_los_vol = format_number(okex_top2_los_vol)
    okex_top3_los_vol = format_number(okex_top3_los_vol)


    title = create_text('title')
    text_all = create_text('text')

    lst1 = [top1_name, top1_volume_24h, top2_name, top2_volume_24h, top3_name, top3_volume_24h,
            binance_top_gain_name, binance_top_gain_price, binance_top_gain_price_change, binance_top_gain_vol,
            cb_top_gain_name, cb_top_gain_price, cb_top_gain_price_change, cb_top_gain_vol,
            okex_top_gain_name, okex_top_gain_price, okex_top_gain_price_change, okex_top_gain_vol,
            binance_hike_name, binance_hike_percent_change, binance_hike_cap,
            cb_hike_name, cb_hike_percent_change, cb_hike_cap,
            okex_hike_name, okex_hike_percent_change, okex_hike_cap,
            binance_top_los_name, binance_top_los_price, binance_top_los_price_change, binance_top_los_vol,
            cb_top_los_name, cb_top_los_price, cb_top_los_price_change, cb_top_los_vol,
            okex_top_los_name, okex_top_los_price, okex_top_los_price_change, okex_top_los_vol,
            binance_drop_name, binance_drop_percent_change, binance_drop_cap,
            cb_drop_name, cb_drop_percent_change, cb_drop_cap,
            okex_drop_name, okex_drop_percent_change, okex_drop_cap,top_caps[0][0], round(top_caps[0][1]),top_caps[0][2],format_number(top_caps[0][3]),
            top_caps[1][0], top_caps[1][1],top_caps[1][2],format_number(top_caps[1][3]), top_caps[2][0], top_caps[2][1],top_caps[2][2],format_number(top_caps[2][3])]

    lst2 = ['{top1_name}', '{top1_volume_24h}', '{top2_name}', '{top2_volume_24h}', '{top3_name}', '{top3_volume_24h}',
            '{binance_top_gain_name}', '{binance_top_gain_price}', '{binance_top_gain_price_change}', '{binance_top_gain_vol}',
            '{cb_top_gain_name}', '{cb_top_gain_price}', '{cb_top_gain_price_change}', '{cb_top_gain_vol}',
            '{okex_top_gain_name}', '{okex_top_gain_price}', '{okex_top_gain_price_change}', '{okex_top_gain_vol}',
            '{binance_hike_name}', '{binance_hike_percent_change}', '{binance_hike_cap}',
            '{cb_hike_name}', '{cb_hike_percent_change}', '{cb_hike_cap}',
            '{okex_hike_name}', '{okex_hike_percent_change}', '{okex_hike_cap}',
            '{binance_top_los_name}', '{binance_top_los_price}', '{binance_top_los_price_change}', '{binance_top_los_vol}',
            '{cb_top_los_name}', '{cb_top_los_price}', '{cb_top_los_price_change}', '{cb_top_los_vol}',
            '{okex_top_los_name}', '{okex_top_los_price}', '{okex_top_los_price_change}', '{okex_top_los_vol}',
            '{binance_drop_name}', '{binance_drop_percent_change}', '{binance_drop_cap}',
            '{cb_drop_name}', '{cb_drop_percent_change}', '{cb_drop_cap}',
            '{okex_drop_name}', '{okex_drop_percent_change}', '{okex_drop_cap}','{top_caps[0][0]}', '{round(top_caps[0][1])}','{top_caps[0][2]}','{format_number(top_caps[0][3])}',
            '{top_caps[1][0]}', '{top_caps[1][1]}','{top_caps[1][2]}','{format_number(top_caps[1][3])}','{top_caps[2][0]}', '{top_caps[2][1]}','{top_caps[2][2]}','{format_number(top_caps[2][3])}']

    for i in range(len(lst1)):
        if lst2[i] in text_all:
            text_all = text_all.replace(lst2[i], str(lst1[i]))
        if lst2[i] in title:
            title = title.replace(lst2[i], str(lst1[i]))
    print('Text created')
    push_post(title, text_all)
main()


