import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json, hmac, hashlib, time, base64
from datetime import datetime, timedelta
import datetime as DT

# all coins coinbase
def get_value_coinbase():
    secretKey = 'RjPwUtqwix3h6Nr0ng9ekjHyJh53ZIJh'
    timestamp = str(int(time.time()))
    payload = timestamp + "GET" + "/api/v3/brokerage/products".split('?')[0]+""
    signature = hmac.new(secretKey.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()

    url_coinbase= "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"

    headers_coinbase = {
      'Content-Type': 'application/json',
      'CB-ACCESS-KEY':'3uvoymeXCMUqcfo2',
      'CB-ACCESS-SIGN':f'{signature.hex()}',
      'CB-ACCESS-TIMESTAMP':f'{timestamp}'
    }
    data = requests.get(url_coinbase, headers=headers_coinbase).json()
    top_gain_name = None
    top_gain_price = 0
    top_gain_price_change = 0
    top_gain_vol = 0

    top_los_name = None
    top_los_price = 0
    top_los_price_change = 0
    top_los_vol = 999999999999999
    return print(data['products'][:10])
    # for i in data['products']:
    #     symbol = str(i['quote_currency_id'])
    #     if symbol.endswith('USD'):
    #         x = i['price_percentage_change_24h']
    #         if x != '':
    #             volume_dol = float(i['volume_24h']) * float(i['price'])
    #             if volume_dol > top_gain_vol:
    #                 top_gain_name = str(i['base_currency_id'])
    #                 top_gain_price = str(i['price'])
    #                 top_gain_price_change = round(float(i['price_percentage_change_24h']), 3)
    #                 top_gain_vol = round(volume_dol, 2)
    #
    #             if volume_dol < top_los_vol and volume_dol != 0:
    #                 top_los_name = str(i['base_currency_id'])
    #                 top_los_price = str(i['price'])
    #                 top_los_price_change = round(float(i['price_percentage_change_24h']), 3)
    #                 top_los_vol = round(volume_dol, 2)
    # return print(f'Top gainer:\n{top_gain_name}\nPrice {top_gain_price}$\nPrice change '
    #              f'{top_gain_price_change}%\nVolume 24h {top_gain_vol}$\n\nTop loser\n{top_los_name}\nPrice '
    #              f'{top_los_price}$\nPrice change {top_los_price_change}%\nVolume 24h {top_los_vol}$')

get_value_coinbase()






















# ca = certifi.where()
#
# api_key = 'WxNE4DGEA9YUSpu3'
# api_secret = 'JknbKVFxvOCfFCsFKseVA88ltcHUwMtt'
# api_url = 'https://api.coinbase.com/v2/'
#
# def create_coinbase_signature(timestamp, method, request_path, body=''):
#     message = str(timestamp) + method + request_path + body
#     signature = hmac.new(api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
#     return signature










# def get_coinbase_price(cur):
#     endpoint_eth = 'prices/ETH-USD/spot'
#     endpoint_btc = 'prices/BTC-USD/spot'
#     endpoint_ada = 'prices/ADA-USD/spot'
#     requst_path = ''
#     if cur == 'eth':
#         request_path = api_url + endpoint_eth
#     if cur == 'btc':
#         request_path = api_url + endpoint_btc
#     if cur == 'ada':
#         request_path = api_url + endpoint_ada
#
#     timestamp = int(time.time())
#     headers = {
#         'CB-ACCESS-KEY': api_key,
#         'CB-ACCESS-SIGN': create_coinbase_signature(timestamp, 'GET', request_path),
#         'CB-ACCESS-TIMESTAMP': str(timestamp),
#         'CB-ACCESS-PASSPHRASE': '',
#         'Content-Type': 'application/json'
#     }
#
#     response = requests.get(request_path, headers=headers)
#     if response.status_code == 200:
#         data = json.loads(response.text)
#         price = data
        # price = round(float(price),2)
        # if cur == 'eth':
        #     print(f'Ethereum price now:{price}$')
        # if cur == 'btc':
        #     print(f'Bitcoin price now:{price}$')
        # if cur == 'ada':
        #     print(f'Cardano price now:{price}$')
    # else:
    #     print('Error occurred:', response.text)
    # print(price)
# def get_price():
#     get_coinbase_price('btc')
#     get_coinbase_price('eth')
#     get_coinbase_price('ada')
# # get_price()
# def get_price_by_date(cur, date):
#     url = requests.get(f'https://api.coinbase.com/v2/prices/{cur}-USD/spot?date={date}')
#     data = url.json()['data']['amount']
#     print(f'{cur} price at {date}: {data}$')


# get_price_by_date('BTC', '2022-01-06')
# get_price_by_date('ETH', '2023-05-09')
# get_price_by_date('ADA', '2021-09-12')
# get_price_by_date('XRP', '2022-12-28')
# get_price_by_date('BCH', '2022-01-09')
# get_price_by_date('SOL', '2020-02-15')

# date_now2 = str(datetime.now())[:13]
#
# a = {
#     '_id':'3',
#     'one':'111111111',
#     'two':'2222222222',
#     'three':'33333333'
# }
# client = MongoClient("mongodb+srv://useruser2023:colibri23@cluster0.dt046rn.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
# db = client['crypto_base']
# coll = db['bot_bot']
# coll.insert_one(a)
# print(coll.find_())
# for x in coll.find():
#     print(x)
