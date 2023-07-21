import requests

def get_top_10_currencies(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': 1,
        'limit': 30,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            top_10_currencies = data['data']
            return top_10_currencies
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return None
if __name__ == "__main__":
    api_key = '3c6565ce-18c1-4496-8727-02b12ece3299'
    top_currencies = get_top_10_currencies(api_key)
    if top_currencies:
        print("Топ-30 валют по капитализации на CoinMarketCap:")
        for currency in top_currencies:
            currency['quote']['USD']['market_cap'] = currency['quote']['USD']['market_cap'] / 1e9
            currency['quote']['USD']['market_cap'] = round(currency['quote']['USD']['market_cap'], 2)
            print(f"{currency['symbol']} Капитализация: {currency['quote']['USD']['market_cap']} Миллиард $")
    else:
        print("Не удалось получить данные о топ-10 валютах.")

