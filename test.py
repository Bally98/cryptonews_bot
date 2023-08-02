import requests
def get_cap_cmc(coin):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '3c6565ce-18c1-4496-8727-02b12ece3299',
    }
    url_cmc_cap = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin}'
    data_cmc_cap = requests.get(url_cmc_cap, headers=headers).json()
    # if float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap'])) == 0 or '0':
    #     return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['fully_diluted_market_cap']))
    # else:
    #     return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap']))
    return print(data_cmc_cap)
get_cap_cmc('BCC')