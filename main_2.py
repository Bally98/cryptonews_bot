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
        if cmc_value['quote']['USD']['percent_change_24h'] > top1_volume_24h:
            top3_volume_24h = top2_volume_24h
            top2_volume_24h = top1_volume_24h
            top1_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
            top1_name = cmc_value['name']
        elif cmc_value['quote']['USD']['percent_change_24h'] > top2_volume_24h:
            top3_volume_24h = top2_volume_24h
            top2_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
            top2_name = cmc_value['name']
        elif cmc_value['quote']['USD']['percent_change_24h'] > top3_volume_24h:
            top3_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
            top3_name = cmc_value['name']

        binance_top_gain_name = ''
        binance_top_gain_price_change = 0
        binance_top_gain_price = 0
        binance_top_gain_vol = 0
        binance_top_los_name = ''
        binance_top_los_price_change = 0
        binance_top_los_price = 0
        binance_top_los_vol = 999999999

        cb_top_gain_name = ''
        cb_top_gain_price_change = 0
        cb_top_gain_price = 0
        cb_top_gain_vol = 0
        cb_top_los_name = ''
        cb_top_los_price_change = 0
        cb_top_los_price = 0
        cb_top_los_vol = 999999999

        okex_top_gain_name = ''
        okex_top_gain_price = 0
        okex_top_gain_price_change = 0
        okex_top_gain_vol = 0
        okex_top_los_name = ''
        okex_top_los_price = 0
        okex_top_los_price_change = 0
        okex_top_los_vol = 999999999

    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT') or symbol_binance.endswith('USD') or symbol_binance.endswith('USDC'):
            if round(float(value_binance['quoteVolume']), 2) > float(binance_top_gain_vol):
                binance_top_gain_name = value_binance['symbol'][:-4]
                binance_top_gain_price = cut(float(value_binance['lastPrice']))
                binance_top_gain_price_change = float(value_binance['priceChangePercent'])
                binance_top_gain_vol = round(float(value_binance['quoteVolume']))
            if round(float(value_binance['quoteVolume']), 2) < float(binance_top_los_vol):
                if float(value_binance['lastPrice']) > 0:
                    binance_top_los_name = value_binance['symbol'][:-4]
                    binance_top_los_price = round(float(value_binance['lastPrice']), 4)
                    binance_top_los_price_change = float(value_binance['priceChangePercent'])
                    binance_top_los_vol = cut(float(value_binance['quoteVolume']))
    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT') or symbol_binance.endswith('USD') or symbol_binance.endswith('USDC'):
            if value_cb['price_percentage_change_24h'] != '':
                volume_cb = float(value_cb['volume_24h']) * float(value_cb['price'])
                if volume_cb > cb_top_gain_vol:
                    cb_top_gain_name = str(value_cb['base_currency_id'])
                    cb_top_gain_price = cut(float(value_cb['price']))
                    cb_top_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                    cb_top_gain_vol = round(volume_cb)
                if volume_cb < cb_top_gain_vol:
                    cb_top_los_name = str(value_cb['base_currency_id'])
                    cb_top_los_price = round(float(value_cb['price']), 4)
                    cb_top_los_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                    cb_top_los_vol = cut(volume_cb)
    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_binance.endswith('USD') or symbol_binance.endswith('USDC'):
            if float(value_okex['volCcy24h']) > okex_top_gain_vol:
                x = value_okex['instId'].index('-')
                okex_top_gain_name = str(value_okex['instId'][:x])
                okex_top_gain_price = cut(float(value_okex['last']))
                okex_top_gain_price_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                okex_top_gain_vol = round(float(value_okex['volCcy24h']))
            if float(value_okex['volCcy24h']) < okex_top_los_vol:
                x = value_okex['instId'].index('-')
                okex_top_los_name = str(value_okex['instId'][:x])
                okex_top_los_price = round(float(value_okex['last']), 4)
                okex_top_los_price_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                okex_top_los_vol = cut(float(value_okex['volCcy24h']))

    binance_hike_name = ''
    binance_hike_percent_change = 0
    binance_hike_cap = 0
    binance_drop_name = ''
    binance_drop_percent_change = 999
    binance_drop_cap = 0

    cb_hike_name = ''
    cb_hike_percent_change = 0
    cb_hike_cap = 0
    cb_drop_name = ''
    cb_drop_percent_change = 999
    cb_drop_cap = 0

    okex_hike_name = ''
    okex_hike_percent_change = 0
    okex_hike_cap = 0
    okex_drop_name = ''
    okex_drop_percent_change = 999
    okex_drop_cap = 0

    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT'):
            if float(value_binance['priceChangePercent']) > binance_hike_percent_change:
                binance_hike_name = value_binance['symbol'][:-4]
                binance_hike_percent_change = float(value_binance['priceChangePercent'])
            if float(value_binance['priceChangePercent']) < binance_drop_percent_change:
                binance_drop_name = value_binance['symbol'][:-4]
                binance_drop_percent_change = float(value_binance['priceChangePercent'])
    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT'):
            x = value_cb['price_percentage_change_24h']
            if x != '':
                if float(x) > cb_hike_percent_change:
                    cb_hike_name = str(value_cb['base_currency_id'])
                    cb_hike_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                if float(x) < cb_drop_percent_change:
                    cb_drop_name = str(value_cb['base_currency_id'])
                    cb_drop_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_okex.endswith('USDC'):
            if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_percent_change:
                x = value_okex['instId'].index('-')
                okex_hike_name = str(value_okex['instId'][:x])
                okex_hike_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_percent_change:
                x = value_okex['instId'].index('-')
                okex_drop_name = str(value_okex['instId'][:x])
                okex_drop_percent_change = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
    binance_hike_cap = format_number(get_cap_cmc(binance_hike_name))
    binance_drop_cap = format_number(get_cap_cmc(binance_drop_name))
    cb_hike_cap = format_number(get_cap_cmc(cb_hike_name))
    cb_drop_cap = format_number(get_cap_cmc(cb_drop_name))
    okex_hike_cap = format_number(get_cap_cmc(okex_hike_name))
    okex_drop_cap = format_number(get_cap_cmc(okex_drop_name))
    binance_top_gain_vol = format_number(binance_top_gain_vol)
    cb_top_gain_vol = format_number(cb_top_gain_vol)
    okex_top_gain_vol = format_number(okex_top_gain_vol)
    binance_top_los_vol = format_number(binance_top_los_vol)
    cb_top_los_vol = format_number(cb_top_los_vol)
    okex_top_los_vol = format_number(okex_top_los_vol)


    top_caps = [[],[],[]]
    for top5 in range(3):
        top_caps[top5].insert(0, str(data_cmc['data'][top5]['symbol']))
        top_caps[top5].insert(1, round(float(data_cmc['data'][top5]['quote']['USD']['price']), 2))
        top_caps[top5].insert(2, round(float(data_cmc['data'][top5]['quote']['USD']['percent_change_24h']), 2))
        top_caps[top5].insert(3, round(float(data_cmc['data'][top5]['quote']['USD']['volume_24h'])))
    top_caps[0][1] = round(top_caps[0][1])
    top_caps[1][1] = round(top_caps[1][1])
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


