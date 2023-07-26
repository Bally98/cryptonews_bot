import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json, hmac, hashlib, time, base64
from datetime import datetime, timedelta
import datetime as DT
def main():
    def cut(num):
        num = round(num, 2)
        return num
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
            'limit': 50,
            'convert': 'USD'
        }
        headers = {
            'X-CMC_PRO_API_KEY': api_key
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        for i in data['data']:

            if i['quote']['USD']['percent_change_24h'] > top1_volume_24h:
                top3_volume_24h = top2_volume_24h
                top2_volume_24h = top1_volume_24h
                top1_volume_24h = round(float(i['quote']['USD']['percent_change_24h']), 2)
                top1_name = i['name']
            elif i['quote']['USD']['percent_change_24h'] > top2_volume_24h:
                top3_volume_24h = top2_volume_24h
                top2_volume_24h = round(float(i['quote']['USD']['percent_change_24h']), 2)
                top2_name = i['name']
            elif i['quote']['USD']['percent_change_24h'] > top3_volume_24h:
                top3_volume_24h = round(float(i['quote']['USD']['percent_change_24h']), 2)
                top3_name = i['name']

        return print(f'Top 1 - {top1_name}:{top1_volume_24h}%\nTop 2 - {top2_name}:'
                     f'{top2_volume_24h}%\nTop 3 - {top3_name}:{top3_volume_24h}%\n ')


    def top_gainers():
        url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
        url_binance = 'https://api.binance.com/api/v3/ticker/24hr'
        url_coinbase = "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"
        secretKey_coinbase = 'RjPwUtqwix3h6Nr0ng9ekjHyJh53ZIJh'
        timestamp = str(int(time.time()))
        payload = timestamp + "GET" + "/api/v3/brokerage/products".split('?')[0] + ""
        signature = hmac.new(secretKey_coinbase.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()

        headers_coinbase = {
            'Content-Type': 'application/json',
            'CB-ACCESS-KEY': '3uvoymeXCMUqcfo2',
            'CB-ACCESS-SIGN': f'{signature.hex()}',
            'CB-ACCESS-TIMESTAMP': f'{timestamp}'
        }

        cb_top_gain_name = ''
        cb_top_gain_price = 0
        cb_top_gain_price_change = 0
        cb_top_gain_vol = 0

        data_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
        data_okex = requests.get(url_okex).json()
        data_binance = requests.get(url_binance).json()

        binance_top_gain_name = ''
        binance_top_gain_price = 0
        binance_top_gain_price_change = 0
        binance_top_gain_vol = 0

        okex_top_gain_name = ''
        okex_top_gain_price = 0
        okex_top_gain_price_change = 0
        okex_top_gain_vol = 0
        for value_okex in data_okex['data']:
            symbol_okex = value_okex['instId']
            if symbol_okex.endswith('USDT') or symbol_okex.endswith('USD'):
                if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_top_gain_price_change:
                    x = value_okex['instId'].index('-')
                    okex_top_gain_name = str(value_okex['instId'][:x])
                    okex_top_gain_price = str(value_okex['last'])
                    okex_top_gain_price_change = round((float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top_gain_vol = round(float(value_okex['vol24h']), 2)
        for value_binance in data_binance:
            symbol_binance = str(value_binance['symbol'])
            if symbol_binance.endswith('USDT') or symbol_binance.endswith('USD'):
                if float(value_binance['priceChangePercent']) > binance_top_gain_price_change:
                    binance_top_gain_name = value_binance['symbol'][:-4]
                    binance_top_gain_price = value_binance['lastPrice']
                    binance_top_gain_price_change = float(value_binance['priceChangePercent'])
                    binance_top_gain_vol = cut(float(value_binance['quoteVolume']))
        for value_cb in data_coinbase['products']:
            symbol_cb = str(value_cb['quote_currency_id'])
            if symbol_cb.endswith('USDT') or symbol_cb.endswith('USD'):
                x = value_cb['price_percentage_change_24h']
                if x != '':
                    x = float(x)
                    if x > cb_top_gain_price_change:
                        cb_top_gain_name = str(value_cb['base_currency_id'])
                        cb_top_gain_price = str(value_cb['price'])
                        cb_top_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top_gain_vol = cut(float(value_cb['volume_24h']))
        return print(f'Top gainers\n{okex_top_gain_name}:{okex_top_gain_price}$,{okex_top_gain_price_change}%\nVolume:{okex_top_gain_vol}$ Via OKEX\n\n'
                     f'{binance_top_gain_name}:{binance_top_gain_price}$,{binance_top_gain_price_change}%\nVolume:{binance_top_gain_vol}$ Via Binance\n\n'
                     f'{cb_top_gain_name}:{cb_top_gain_price}$,{cb_top_gain_price_change}%\nVolume:{cb_top_gain_vol}$ Via CoinBase')
    return get_3_biggest_crypto(), top_gainers()
main()















