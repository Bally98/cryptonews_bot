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
print(data)


def get_coin_growth(api_key, api_secret):
    # Замените 'API_KEY' и 'SECRET_KEY' на свои реальные ключи доступа к API Binance
    api_key = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
    api_secret = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'

    # Формирование запроса к API для получения данных о курсах всех торговых пар
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    data = response.json()

    # Инициализация переменных для хранения информации о наибольшем росте монеты
    max_percentage_change = 0.0
    coin_with_max_change = None

    # Обработка данных о курсах всех торговых пар
    for coin_data in data:
        symbol = coin_data['symbol']
        percentage_change = float(coin_data['priceChangePercent'])

        # Проверка, является ли текущий процентный рост наибольшим
        if percentage_change > max_percentage_change:
            max_percentage_change = percentage_change
            coin_with_max_change = symbol

    return coin_with_max_change, max_percentage_change

if __name__ == "__main__":
    # Замените 'API_KEY' и 'SECRET_KEY' на свои реальные ключи доступа к API Binance
    api_key = 'API_KEY'
    secret_key = 'SECRET_KEY'

    coin, growth = get_coin_growth(api_key, secret_key)
    print(f"Монета с наибольшим ростом: {coin}")
    print(f"Рост: {growth}%")