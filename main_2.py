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

    binance_gain_names = ['', '', '']
    binance_gain_price_changes = [0, 0, 0]
    binance_gain_prices = [0, 0, 0]
    binance_gain_vols = [0, 0, 0]

    binance_los_names = ['', '', '']
    binance_los_price_changes = [0, 0, 0]
    binance_los_prices = [0, 0, 0]
    binance_los_vols = [100000000000, 100000000000, 100000000000]

    cb_gain_names = ['', '', '']
    cb_gain_price_changes = [0, 0, 0]
    cb_gain_prices = [0, 0, 0]
    cb_gain_vols = [0, 0, 0]

    cb_los_names = ['', '', '']
    cb_los_price_changes = [0, 0, 0]
    cb_los_prices = [0, 0, 0]
    cb_los_vols = [100000000000, 100000000000, 100000000000]

    okex_gain_names = ['', '', '']
    okex_gain_price_changes = [0, 0, 0]
    okex_gain_prices = [0, 0, 0]
    okex_gain_vols = [0, 0, 0]

    okex_los_names = ['', '', '']
    okex_los_price_changes = [0, 0, 0]
    okex_los_prices = [0, 0, 0]
    okex_los_vols = [100000000000, 100000000000, 100000000000]




    binance_hike_names = ['', '', '']
    binance_hike_price_changes = [0, 0, 0]
    binance_hike_cap = [0, 0, 0]

    binance_drop_names = ['', '', '']
    binance_drop_price_changes = [0, 0, 0]
    binance_drop_cap = [0, 0, 0]

    cb_hike_names = ['', '', '']
    cb_hike_price_changes = [0, 0, 0]
    cb_hike_cap = [0, 0, 0]

    cb_drop_names = ['', '', '']
    cb_drop_price_changes = [0, 0, 0]
    cb_drop_cap = [0, 0, 0]

    okex_hike_names = ['', '', '']
    okex_hike_price_changes = [0, 0, 0]
    okex_hike_cap = [0, 0, 0]

    okex_drop_names = ['', '', '']
    okex_drop_price_changes = [0, 0, 0]
    okex_drop_cap = [0, 0, 0]

    top_names = ['', '', '']
    top_volumes_24h = [0, 0, 0]
    top3 = ''



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


    #gain\los
    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT') or symbol_binance.endswith('USDC') or symbol_binance.endswith('TUSD'):
            binance_value = round(float(value_binance['quoteVolume']), 2)
            if float(value_binance['quoteVolume']) > 0:
                if binance_value > float(binance_gain_vols[0]):
                    binance_gain_vols[2] = binance_gain_vols[1]
                    binance_gain_vols[1] = binance_gain_vols[0]
                    binance_gain_vols[0] = round(float(value_binance['quoteVolume']))
                    binance_gain_names[0] = value_binance['symbol'][:-4]
                    binance_gain_prices[0] = cut(float(value_binance['lastPrice']))
                    binance_gain_price_changes[0] = float(value_binance['priceChangePercent'])
                elif binance_value > float(binance_gain_vols[1]):
                    binance_gain_vols[2] = binance_gain_vols[1]
                    binance_gain_vols[1] = round(float(value_binance['quoteVolume']))
                    binance_gain_names[1] = value_binance['symbol'][:-4]
                    binance_gain_prices[1] = cut(float(value_binance['lastPrice']))
                    binance_gain_price_changes[1] = float(value_binance['priceChangePercent'])
                elif binance_value> float(binance_gain_vols[2]):
                    binance_gain_vols[2] = round(float(value_binance['quoteVolume']))
                    binance_gain_names[2] = value_binance['symbol'][:-4]
                    binance_gain_prices[2] = cut(float(value_binance['lastPrice']))
                    binance_gain_price_changes[2] = float(value_binance['priceChangePercent'])

                elif binance_value < float(binance_los_vols[0]):
                    binance_los_vols[2] = binance_los_vols[1]
                    binance_los_vols[1] = binance_los_vols[0]
                    binance_los_vols[0] = round(float(value_binance['quoteVolume']))
                    binance_los_names[0] = value_binance['symbol'][:-4]
                    binance_los_prices[0] = float(value_binance['lastPrice'])
                    binance_los_price_changes[0] = float(value_binance['priceChangePercent'])
                elif binance_value < float(binance_los_vols[1]):
                    binance_los_vols[2] = binance_los_vols[1]
                    binance_los_vols[1] = round(float(value_binance['quoteVolume']))
                    binance_los_names[1] = value_binance['symbol'][:-4]
                    binance_los_prices[1] = float(value_binance['lastPrice'])
                    binance_los_price_changes[1] = float(value_binance['priceChangePercent'])
                elif binance_value < float(binance_los_vols[2]):
                    binance_los_vols[2] = round(float(value_binance['quoteVolume']))
                    binance_los_names[2] = value_binance['symbol'][:-4]
                    binance_los_prices[2] = float(value_binance['lastPrice'])
                    binance_los_price_changes[2] = float(value_binance['priceChangePercent'])



    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT') or symbol_binance.endswith('USDC') or symbol_binance.endswith('TUSD'):
            if value_cb['price_percentage_change_24h'] != '':
                volume_cb = float(value_cb['volume_24h']) * float(value_cb['price'])
                if volume_cb > float(cb_gain_vols[0]):
                    cb_gain_vols[2] = cb_gain_vols[1]
                    cb_gain_vols[1] = cb_gain_vols[0]
                    cb_gain_names[0] = str(value_cb['base_currency_id'])
                    cb_gain_prices[0] =  float(value_cb['price'])
                    cb_gain_price_changes[0] = round(float(value_cb['price_percentage_change_24h']), 3)
                    cb_gain_vols[0] =  round(volume_cb)
                elif volume_cb > float(cb_gain_vols[1]):
                    cb_gain_vols[2] = cb_gain_vols[1]
                    cb_gain_names[1] =  str(value_cb['base_currency_id'])
                    cb_gain_prices[1] = float(value_cb['price'])
                    cb_gain_price_changes[1] =round(float(value_cb['price_percentage_change_24h']), 3)
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


    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_binance.endswith('USDC') or symbol_binance.endswith('TUSD'):
            if float(value_okex['last']) > 0 :
                x = value_okex['instId'].index('-')
                if float(value_okex['volCcy24h']) > okex_gain_vols[0]:
                    okex_gain_vols[2] = okex_gain_vols[1]
                    okex_gain_vols[1] = okex_gain_vols[0]
                    okex_gain_names[0] = str(value_okex['instId'][:x])
                    okex_gain_prices[0] =  cut(float(value_okex['last']))
                    okex_gain_price_changes[0] =  round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_gain_vols[0] =  round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) > okex_gain_vols[1]:
                    okex_gain_vols[2] = okex_gain_vols[1]
                    okex_gain_names[1] =  str(value_okex['instId'][:x])
                    okex_gain_prices[1] =  cut(float(value_okex['last']))
                    okex_gain_price_changes[1] = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_gain_vols[1] = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) > okex_gain_vols[2]:
                    okex_gain_names[2] = str(value_okex['instId'][:x])
                    okex_gain_prices[2] =  cut(float(value_okex['last']))
                    okex_gain_price_changes[2] =  round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_gain_vols[2] =  round(float(value_okex['volCcy24h']))

                elif float(value_okex['volCcy24h']) < okex_los_vols[0]:
                    okex_los_vols[2] = okex_los_vols[1]
                    okex_los_vols[1] = okex_los_vols[0]
                    okex_los_names[0] = str(value_okex['instId'][:x])
                    okex_los_prices[0] =  cut(float(value_okex['last']))
                    okex_los_price_changes[0] =  round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_los_vols[0] = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) < okex_los_vols[1]:
                    okex_los_vols[2] = okex_los_vols[1]
                    okex_los_names[1] =  str(value_okex['instId'][:x])
                    okex_los_prices[1] = cut(float(value_okex['last']))
                    okex_los_price_changes[1] = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_los_vols[1] = round(float(value_okex['volCcy24h']))
                elif float(value_okex['volCcy24h']) < okex_los_vols[2]:
                    okex_los_names[2] = str(value_okex['instId'][:x])
                    okex_los_prices[2] = cut(float(value_okex['last']))
                    okex_los_price_changes[2] =  round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_los_vols[2] = round(float(value_okex['volCcy24h']))
    #hike\drop
    for value_binance in data_binance:
        symbol_binance = str(value_binance['symbol'])
        if symbol_binance.endswith('USDT'):
            if float(value_binance['priceChangePercent']) > binance_hike_price_changes[0]:
                binance_hike_price_changes[2] = binance_hike_price_changes[1]
                binance_hike_price_changes[1] = binance_hike_price_changes[0]
                binance_hike_names[0] = value_binance['symbol'][:-4]
                binance_hike_price_changes[0] = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) > binance_hike_price_changes[1]:
                binance_hike_price_changes[2] = binance_hike_price_changes[1]
                binance_hike_names[1] = value_binance['symbol'][:-4]
                binance_hike_price_changes[1] = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) > binance_hike_price_changes[2]:
                binance_hike_names[2] = value_binance['symbol'][:-4]
                binance_hike_price_changes[2] = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance_drop_price_changes[0]:
                binance_drop_price_changes[2] = binance_drop_price_changes[1]
                binance_drop_price_changes[1] = binance_drop_price_changes[0]
                binance_drop_names[0] = value_binance['symbol'][:-4]
                binance_drop_price_changes[0] = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance_drop_price_changes[1]:
                binance_drop_price_changes[2] = binance_drop_price_changes[1]
                binance_drop_names[1] = value_binance['symbol'][:-4]
                binance_drop_price_changes[1] = float(value_binance['priceChangePercent'])
            elif float(value_binance['priceChangePercent']) < binance_drop_price_changes[2]:
                binance_drop_names[2] = value_binance['symbol'][:-4]
                binance_drop_price_changes[2] = float(value_binance['priceChangePercent'])

    for value_cb in data_coinbase['products']:
        symbol_cb = str(value_cb['quote_currency_id'])
        if symbol_cb.endswith('USDT') or symbol_cb.endswith('USDC') or symbol_cb.endswith('TUSD'):
            if value_cb['price_percentage_change_24h'] != '':
                percent = float(value_cb['price_percentage_change_24h'])
                if percent > cb_hike_price_changes[0]:
                    cb_hike_price_changes[2] = cb_hike_price_changes[1]
                    cb_hike_price_changes[1] = cb_hike_price_changes[0]
                    cb_hike_names[0] = str(value_cb['base_currency_id'])
                    cb_hike_price_changes[0] = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent > cb_hike_price_changes[1]:
                    cb_hike_price_changes[2] = cb_hike_price_changes[1]
                    cb_hike_names[1] = str(value_cb['base_currency_id'])
                    cb_hike_price_changes[1] = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent > cb_hike_price_changes[2]:
                    cb_hike_names[2] = str(value_cb['base_currency_id'])
                    cb_hike_price_changes[2] = round(float(value_cb['price_percentage_change_24h']), 3)
                    a = value_cb
                elif percent < cb_drop_price_changes[0]:
                    cb_drop_price_changes[2] = cb_drop_price_changes[1]
                    cb_drop_price_changes[1] = cb_drop_price_changes[0]
                    cb_drop_names[0] = str(value_cb['base_currency_id'])
                    cb_drop_price_changes[0] = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent < cb_drop_price_changes[1]:
                    cb_drop_price_changes[2] = cb_drop_price_changes[1]
                    cb_drop_names[1] = str(value_cb['base_currency_id'])
                    cb_drop_price_changes[1] = round(float(value_cb['price_percentage_change_24h']), 3)
                elif percent < cb_drop_price_changes[2]:
                    cb_drop_names[2] = str(value_cb['base_currency_id'])
                    cb_drop_price_changes[2] = round(float(value_cb['price_percentage_change_24h']), 3)

    for value_okex in data_okex['data']:
        symbol_okex = value_okex['instId']
        if symbol_okex.endswith('USDT') or symbol_okex.endswith('USDC') or symbol_okex.endswith('TUSD'):
            x_index = value_okex['instId'].index('-')
            if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[0]:
                okex_hike_price_changes[2] = okex_hike_price_changes[1]
                okex_hike_price_changes[1] = okex_hike_price_changes[0]
                okex_hike_names[0] = str(value_okex['instId'][:x_index])
                okex_hike_price_changes[0] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[1]:
                okex_hike_price_changes[2] = okex_hike_price_changes[1]
                okex_hike_names[1] = str(value_okex['instId'][:x_index])
                okex_hike_price_changes[1] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_price_changes[2]:
                okex_hike_names[2] = str(value_okex['instId'][:x_index])
                okex_hike_price_changes[2] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[0]:
                okex_drop_price_changes[2] = okex_drop_price_changes[1]
                okex_drop_price_changes[1] = okex_drop_price_changes[0]
                okex_drop_names[0] = str(value_okex['instId'][:x_index])
                okex_drop_price_changes[0] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[1]:
                okex_drop_price_changes[2] = okex_drop_price_changes[1]
                okex_drop_names[1] = str(value_okex['instId'][:x_index])
                okex_drop_price_changes[1] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
            elif float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_price_changes[2]:
                okex_drop_names[2] = str(value_okex['instId'][:x_index])
                okex_drop_price_changes[2] = round(
                    (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)

    for cap_value in range(3):
        binance_hike_cap.insert(cap_value, format_number(get_cap_cmc(binance_hike_names[cap_value])))
        binance_drop_cap.insert(cap_value, format_number(get_cap_cmc(binance_drop_names[cap_value])))
        cb_hike_cap.insert(cap_value, format_number(get_cap_cmc(cb_hike_names[cap_value])))
        cb_drop_cap.insert(cap_value, format_number(get_cap_cmc(cb_drop_names[cap_value])))
        okex_hike_cap.insert(cap_value, format_number(get_cap_cmc(okex_hike_names[cap_value])))
        okex_drop_cap.insert(cap_value, format_number(get_cap_cmc(okex_drop_names[cap_value])))

    for top3_value in range(3):
        top3 += f"<li>{top_names[top3_value]} - {top_volumes_24h[top3_value]}%</li>"

    for vols in range(3):
        binance_gain_vols[vols] = format_number(binance_gain_vols[vols])
        binance_los_vols[vols] = format_number(binance_los_vols[vols])
        cb_gain_vols[vols] = format_number(cb_gain_vols[vols])
        cb_los_vols[vols] = format_number(cb_los_vols[vols])
        okex_gain_vols[vols] = format_number(okex_gain_vols[vols])
        okex_los_vols[vols] = format_number(okex_los_vols[vols])


    binance_gain_text = ''
    binance_los_text = ''
    cb_gain_text = ''
    cb_los_text = ''
    okex_gain_text = ''
    okex_los_text = ''

    for gain_los in range(3):
        binance_gain_text += f"<li>{binance_gain_names[gain_los]} - {binance_gain_prices[gain_los]}$, {binance_gain_price_changes[gain_los]}%, {binance_gain_vols[gain_los]}$ </li>"
        binance_los_text += f"<li>{binance_los_names[gain_los]} - {binance_los_prices[gain_los]}$, {binance_los_price_changes[gain_los]}%, {binance_los_vols[gain_los]}$ </li>"
        cb_gain_text += f"<li>{cb_gain_names[gain_los]} - {cb_gain_prices[gain_los]}$, {cb_gain_price_changes[gain_los]}%, {cb_gain_vols[gain_los]}$ </li>"
        cb_los_text += f"<li>{cb_los_names[gain_los]} - {cb_los_prices[gain_los]}$, {cb_los_price_changes[gain_los]}%, {cb_los_vols[gain_los]}$ </li>"
        okex_gain_text += f"<li>{okex_gain_names[gain_los]} - {okex_gain_prices[gain_los]}$, {okex_gain_price_changes[gain_los]}%, {okex_gain_vols[gain_los]}$ </li>"
        okex_los_text += f"<li>{okex_los_names[gain_los]} - {okex_los_prices[gain_los]}$, {okex_los_price_changes[gain_los]}%, {okex_los_vols[gain_los]}$ </li>"

    binance_hike_text = ''
    binance_drop_text = ''
    cb_hike_text = ''
    cb_drop_text = ''
    okex_hike_text = ''
    okex_drop_text = ''

    for hike_drop in range(3):
        binance_hike_text += f"<li>{binance_hike_names[hike_drop]}: {binance_hike_price_changes[hike_drop]}% (Market cap for now: {binance_gain_price_changes[hike_drop]})$</li>"
        binance_drop_text += f"<li>{binance_drop_names[hike_drop]}: {binance_drop_price_changes[hike_drop]}% (Market cap for now: {binance_drop_cap[hike_drop]})$</li>"
        cb_hike_text += f"<li>{cb_hike_names[hike_drop]}: {cb_hike_price_changes[hike_drop]}% (Market cap for now: {cb_hike_cap[hike_drop]})$</li>"
        cb_drop_text += f"<li>{cb_drop_names[hike_drop]}: {cb_drop_price_changes[hike_drop]}% (Market cap for now: {cb_drop_cap[hike_drop]})$</li>"
        okex_hike_text += f"<li>{okex_hike_names[hike_drop]}: {okex_hike_price_changes[hike_drop]}% (Market cap for now: {okex_hike_cap[hike_drop]})$</li>"
        okex_drop_text += f"<li>{okex_drop_names[hike_drop]}: {okex_drop_price_changes[hike_drop]}% (Market cap for now: {okex_drop_cap[hike_drop]})$</li>"

    title = create_text('title')
    text_all = create_text('text')

    lst1 = [top3, binance_gain_text, cb_gain_text, okex_gain_text, binance_hike_text, cb_hike_text, okex_hike_text,
            binance_los_text, cb_los_text, okex_los_text, binance_drop_text, cb_drop_text, okex_drop_text]

    lst2 = ['{top3}', '{binance_gain_text}', '{cb_gain_text}', '{okex_gain_text}', '{binance_hike_text}', '{cb_hike_text}', '{okex_hike_text}',
            '{binance_los_text}', '{cb_los_text}', '{okex_los_text}', '{binance_drop_text}', '{cb_drop_text}', '{okex_drop_text}']

    for i in range(len(lst1)):
        if lst2[i] in text_all:
            text_all = text_all.replace(lst2[i], str(lst1[i]))
        if lst2[i] in title:
            title = title.replace(lst2[i], str(lst1[i]))
    print('Text created')
    push_post(title, text_all)
main()


