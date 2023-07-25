import requests
import datetime
import time

def okex(btc, eth, bnb):

    url_btc = f"https://www.okex.com/api/v5/market/ticker?instId={btc}-USDT"
    url_eth = f"https://www.okex.com/api/v5/market/ticker?instId={eth}-USDT"
    url_bnb = f"https://www.okex.com/api/v5/market/ticker?instId={bnb}-USDT"
    def round_number(num):
        num = round(float(num))
        return num
    btc_res = requests.get(url_btc)
    data_btc = btc_res.json()
    btc_last_price = data_btc['data'][0]['last']
    btc_high = data_btc['data'][0]['high24h']
    btc_low = data_btc['data'][0]['low24h']
    btc_vol_dollar = data_btc['data'][0]['volCcy24h']
    btc_vol = data_btc['data'][0]['vol24h']
    btc_vol_dollar = round_number(btc_vol_dollar)
    btc_vol = round_number(btc_vol)

    eth_res = requests.get(url_eth)
    data_eth = eth_res.json()
    eth_last_price = data_eth['data'][0]['last']
    eth_high = data_eth['data'][0]['high24h']
    eth_low = data_eth['data'][0]['low24h']
    eth_vol_dollar = data_eth['data'][0]['volCcy24h']
    eth_vol = data_eth['data'][0]['vol24h']
    eth_vol_dollar = round_number(eth_vol_dollar)
    eth_vol = round_number(eth_vol)

    bnb_res = requests.get(url_bnb)
    data_bnb = bnb_res.json()
    bnb_last_price = data_bnb['data'][0]['last']
    bnb_high = data_bnb['data'][0]['high24h']
    bnb_low = data_bnb['data'][0]['low24h']
    bnb_vol_dollar = data_bnb['data'][0]['volCcy24h']
    bnb_vol = data_bnb['data'][0]['vol24h']
    bnb_vol_dollar = round_number(bnb_vol_dollar)
    bnb_vol = round_number(bnb_vol)
    return print(
            f'Okex:\nThe last price of Bitcoin is {btc_last_price}$\nThe highest price today {btc_high}$'
            f'\nThe lowest {btc_low}$\nVolume at the last 24 hours {btc_vol} BTC = {btc_vol_dollar}$'
            f'\n'
            f'\nThe last price of Ethereum is {eth_last_price}$\nThe highest price today {eth_high}$'
            f'\nThe lowest {eth_low}$\nVolume at the last 24 hours {eth_vol} ETH = {eth_vol_dollar}$'
            f'\n'
            f'\nThe last price of Binance coin is {bnb_last_price}$\nThe highest price today {bnb_high}$'
            f'\nThe lowest {bnb_low}$\nVolume at the last 24 hours {bnb_vol} BNB = {bnb_vol_dollar}$'
         )
okex('BTC','ETH', 'BNB')

# all coins from okex
url_all= "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

