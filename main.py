import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json, hmac, hashlib, time, base64
from datetime import datetime, timedelta
import datetime as DT
def main():
    url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url_binance = 'https://api.binance.com/api/v3/ticker/24hr'
    url_coinbase = "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"
    url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

    api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
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
    headers_cmc = {
        'X-CMC_PRO_API_KEY': api_key_cmc
    }
    params_cmc = {
        'start': 1,
        'limit': 50,
        'convert': 'USD'
    }
    data_cmc = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
    data_binance = requests.get(url_binance).json()
    data_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
    data_okex = requests.get(url_okex).json()
    def get_cap_cmc(coin):
        for j in data_cmc['data']:
            if j['symbol'] == coin:
                return j['quote']['USD']['market_cap']
                break

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

        return print(f'Top 1 - {top1_name}:{top1_volume_24h}%\nTop 2 - {top2_name}:'
                     f'{top2_volume_24h}%\nTop 3 - {top3_name}:{top3_volume_24h}%\n ')

    def gainers_losers(command):
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
            if symbol_binance.endswith('USDT'):
                if round(float(value_binance['quoteVolume']), 2) > binance_top_gain_vol:
                    binance_top_gain_name = value_binance['symbol'][:-4]
                    binance_top_gain_price = value_binance['lastPrice']
                    binance_top_gain_price_change = float(value_binance['priceChangePercent'])
                    binance_top_gain_vol = cut(float(value_binance['quoteVolume']))
                if round(float(value_binance['quoteVolume']), 2) < binance_top_gain_vol:
                    binance_top_los_name = value_binance['symbol'][:-4]
                    binance_top_los_price = value_binance['lastPrice']
                    binance_top_los_price_change = float(value_binance['priceChangePercent'])
                    binance_top_los_vol = cut(float(value_binance['quoteVolume']))
        for value_cb in data_coinbase['products']:
            symbol_cb = str(value_cb['quote_currency_id'])
            if symbol_cb.endswith('USDT'):
                if value_cb['price_percentage_change_24h'] != '':
                    volume_cb = float(value_cb['volume_24h']) * float(value_cb['price'])
                    if volume_cb > cb_top_gain_vol:
                        cb_top_gain_name = str(value_cb['base_currency_id'])
                        cb_top_gain_price = float(value_cb['price'])
                        cb_top_gain_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top_gain_vol = volume_cb
                    if volume_cb < cb_top_gain_vol:
                        cb_top_los_name = str(value_cb['base_currency_id'])
                        cb_top_los_price = float(value_cb['price'])
                        cb_top_los_price_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_top_los_vol = volume_cb
        for value_okex in data_okex['data']:
            symbol_okex = value_okex['instId']
            if symbol_okex.endswith('USDT'):
                if float(value_okex['volCcy24h']) > okex_top_gain_vol:
                    x = value_okex['instId'].index('-')
                    okex_top_gain_name = str(value_okex['instId'][:x])
                    okex_top_gain_price = str(value_okex['last'])
                    okex_top_gain_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top_gain_vol = round(float(value_okex['volCcy24h']), 2)
                if float(value_okex['volCcy24h']) > okex_top_gain_vol:
                    x = value_okex['instId'].index('-')
                    okex_top_los_name = str(value_okex['instId'][:x])
                    okex_top_los_price = str(value_okex['last'])
                    okex_top_los_price_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_top_los_vol = round(float(value_okex['volCcy24h']), 2)
        if command == 'gainers':
            return print(f'Top gainers\n{okex_top_gain_name}:{okex_top_gain_price}$,{okex_top_gain_price_change}%\nVolume:{okex_top_gain_vol}$ Via OKEX\n\n'
                         f'{binance_top_gain_name}:{binance_top_gain_price}$,{binance_top_gain_price_change}%\nVolume:{binance_top_gain_vol}$ Via Binance\n\n'
                         f'{cb_top_gain_name}:{cb_top_gain_price}$,{cb_top_gain_price_change}%\nVolume:{cb_top_gain_vol}$ Via CoinBase')
        elif command == 'losers':
            return print(
                f'Top losers\n{okex_top_los_name}:{okex_top_los_price}$,{okex_top_los_price_change}%\nVolume:{okex_top_los_vol}$ Via OKEX\n\n'
                f'{binance_top_los_name}:{binance_top_los_price}$,{binance_top_los_price_change}%\nVolume:{binance_top_los_vol}$ Via Binance\n\n'
                f'{cb_top_los_name}:{cb_top_los_price}$,{cb_top_los_price_change}%\nVolume:{cb_top_los_vol}$ Via CoinBase')

    def price_hike_drop(command):
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
                    binance_hike_cap = get_cap_cmc(str(binance_hike_name))
                if float(value_binance['priceChangePercent']) > binance_drop_percent_change:
                    binance_drop_name = value_binance['symbol'][:-4]
                    binance_drop_percent_change = float(value_binance['priceChangePercent'])
                    binance_drop_cap = get_cap_cmc(str(binance_drop_name))
        for value_cb in data_coinbase['products']:
            symbol_cb = str(value_cb['quote_currency_id'])
            if symbol_cb.endswith('USDT'):
                x = value_cb['price_percentage_change_24h']
                if x != '':
                    if float(x) > cb_hike_percent_change:
                        cb_hike_name = str(value_cb['base_currency_id'])
                        cb_hike_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_hike_cap = get_cap_cmc(str(cb_hike_name))
                    if float(x) < cb_drop_percent_change:
                        cb_drop_name = str(value_cb['base_currency_id'])
                        cb_drop_percent_change = round(float(value_cb['price_percentage_change_24h']), 3)
                        cb_drop_cap = get_cap_cmc(str(cb_drop_name))
        for value_okex in data_okex['data']:
            symbol_okex = value_okex['instId']
            if symbol_okex.endswith('USDT'):
                if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 > okex_hike_percent_change:
                    x = value_okex['instId'].index('-')
                    okex_hike_name = str(value_okex['instId'][:x])
                    kex_hike_percent_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_hike_cap = get_cap_cmc(str(okex_hike_name))
                if float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100 < okex_drop_percent_change:
                    x = value_okex['instId'].index('-')
                    okex_drop_name = str(value_okex['instId'][:x])
                    okex_drop_percent_change = round(
                        (float(value_okex['last']) / float(value_okex['open24h']) * 100 - 100), 2)
                    okex_drop_cap = get_cap_cmc(str(okex_drop_name))
        if command == 'hike':
            return print(f'Biggest price hike today:\n'
                         f'Binance:{binance_hike_name}: +{binance_hike_percent_change}\n(Market cap for now:{binance_hike_cap})\n'
                         f'CoinBase:{cb_hike_name}: +{cb_hike_percent_change}\n(Market cap for now:{cb_hike_cap})\n'
                         f'OKEX:{okex_hike_name}: +{okex_hike_percent_change}\n(Market cap for now:{okex_hike_cap})')
        elif command == 'drop':
            return print(f'Biggest price hike today:\n'
                         f'Binance:{binance_drop_name}: +{binance_drop_percent_change}\n(Market cap for now:{binance_drop_cap})\n'
                         f'CoinBase:{cb_drop_name}: +{cb_drop_percent_change}\n(Market cap for now:{cb_drop_cap})\n'
                         f'OKEX:{okex_drop_name}: +{okex_drop_percent_change}\n(Market cap for now:{okex_drop_cap})')


    def top_5_cap():
        top_caps = [[],[],[],[],[]]
        for top5 in range(5):
            top_caps[top5].insert(0, str(data['data'][top5]['symbol']))
            top_caps[top5].insert(1, str(data['data'][top5]['quote']['USD']['price']))
            top_caps[top5].insert(2, str(data['data'][top5]['quote']['USD']['percent_change_24h']))
            top_caps[top5].insert(3, str(data['data'][top5]['quote']['USD']['volume_24h']))
        for k in range(5):
            print(f'Top volume\n*{top_caps[k][0]}: {top_caps[k][1]}$  {top_caps[k][2]}%\nVolume 24h: {top_caps[k][3]}$')

    get_3_biggest_crypto()
    gainers_losers('gainers')
    price_hike_drop('hike')
    iners_losers('losers')
    price_hike_drop('drop')
    top_5_cap()
main()


