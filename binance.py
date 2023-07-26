import requests
import json
import hashlib
import hmac
import time

api_key = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
api_secret = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'
api_url = 'https://api.binance.com/api/v3'

def create_binance_signature(query_string):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_binance_price():
    endpoint = '/ticker/price'
    symbol = 'BNBUSDT'
    request_path = api_url + endpoint

    query_string = 'symbol=' + symbol
    timestamp = int(time.time() * 1000)
    query_string += '&timestamp=' + str(timestamp)

    signature = create_binance_signature(query_string)
    headers = {
            'X-MBX-APIKEY': api_key,
            'X-MBX-SECRETKEY': api_secret
        }

    params = {
        'symbol': symbol,
    }

    response = requests.get(request_path, headers=headers, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        price = data['price']
        print('Binance Coin price: $', price)
    else:
        print('Error occurred:', response.text)
#
# get_binance_price()
# #

# # import requests
# headers = {
#         'X-MBX-APIKEY': api_key,
#         'X-MBX-SECRETKEY': api_secret
#     }
# # key = "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT"
key = "https://api.binance.com/api/v3/ticker/24hr"

data = requests.get(key)
data = data.json()
# print(data)


def get_coin_growth():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    data = response.json()

    binance_top_gain_name = ''
    binance_top_gain_price = 0
    binance_top_gain_price_change = 0
    binance_top_gain_vol = 0

    binance_top_los_name = ''
    binance_top_los_price = 0
    binance_top_los_price_change = 0
    binance_top_los_vol = 0

    for i in data:
        symbol = str(i['symbol'])
        if symbol.endswith('USDT'):
            if float(i['priceChangePercent']) > binance_top_gain_price_change:
                binance_top_gain_name = i['symbol'][:-4]
                binance_top_gain_price = i['lastPrice']
                binance_top_gain_price_change = float(i['priceChangePercent'])
                binance_top_gain_vol = round(float(i['quoteVolume']), 2)

            if float(i['priceChangePercent']) < binance_top_los_price_change:
                binance_top_los_name = i['symbol'][:-4]
                binance_top_los_price = i['lastPrice']
                binance_top_los_price_change = float(i['priceChangePercent'])
                binance_top_los_vol = round(float(i['quoteVolume']), 2)

    return print(f'Name gain - {binance_top_gain_name}\nPrice:{binance_top_gain_price}$\nChange 24h:{binance_top_gain_price_change}%\n'
                 f'Volume 24h:{binance_top_gain_vol}\n\n'
                 f'Name los - {binance_top_los_name}\nPrice:{binance_top_los_price}$\nChange 24h:{binance_top_los_price_change}%\n'
                 f'Volume 24h:{binance_top_los_vol}')
get_coin_growth()

# if __name__ == "__main__":
    # Замените 'API_KEY' и 'SECRET_KEY' на свои реальные ключи доступа к API Binance
    # api_key = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
    # secret_key = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'

    # coin, growth = get_coin_growth()
    # print(f"Монета с наибольшим ростом: {coin}")
    # print(f"Рост: {growth}%")



