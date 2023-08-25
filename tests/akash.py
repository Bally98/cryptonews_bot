import requests
import base64

def get_data(block_number) -> int:
    url = f'https://akash-rest.publicnode.com/blocks/{block_number}'
    response = requests.get(url).json()
    txs_values = response['block']['data']['txs']
    if len(txs_values) > 0:
        for element in txs_values:
            print(base64.b64decode(element))
    else:
        print('No values')

get_data(11260637)
