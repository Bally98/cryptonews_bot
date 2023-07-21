import requests
import json
import hashlib
import hmac
import time

api_key = 'ZWhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
api_secret = 'DLIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'
api_url = 'https://api.binance.us/api/v3'

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


    params = {
        'symbol': symbol,
        'timestamp': timestamp,
        'recvWindow': 5000,
        'signature': signature
    }

    response = requests.get(request_path, headers=headers, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        price = data['price']
        print('Binance Coin price: $', price)
    else:
        print('Error occurred:', response.text)

# get_binance_price()
#

# import requests
headers = {
        'X-MBX-APIKEY': api_key,
        'X-MBX-SECRETKEY': api_secret
    }
# key = "https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT"
key = "https://api.binance.us/api/v3/ticker/24hr?symbol=BTCUSDT"

data = requests.get(key, headers=headers)
data = data.json()
print(data)

