import json, hmac, hashlib, time, base64
import requests
from datetime import datetime, timedelta
import datetime as DT

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
req_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
print(req_coinbase)
