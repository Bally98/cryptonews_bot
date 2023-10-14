import requests
from tqdm import tqdm
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json, hmac, hashlib, time, base64
from datetime import datetime, timedelta
import datetime as DT
from functions import create_text, push_post, fetch_crypto_news
from PIL import Image, ImageDraw, ImageFont

from connectors.open_ai import GptAi


def main():
    open_ai = GptAi()

    url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url_binance = 'https://api.binance.com/api/v3/ticker/24hr'
    url_coinbase = "https://api.coinbase.com/api/v3/brokerage/products?product_type=SPOT"
    url_okex = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

    api_key_cmc = '30c6565ce-18c1-4496-8727-02b12ece3299'
    secretKey_coinbase = 'R0jPwUtqwix3h6Nr0ng9ekjHyJh53ZIJh'
    api_key_binance = 'Z0WhBTWICgxOt67WrNNrP8j4WBKSpnvUj7cwJZ5QXlc6Cs2nM3w7QWZ4PEsQw1MvJ'
    api_secret_binance = 'D0LIHRHgEnOGTYCimOj7qRaGAvj3adA8oG37dVryDcqbxsRiWql4KAPlaKPlqE4Xg'

    timestamp = str(int(time.time()))
    payload = timestamp + "GET" + "/api/v3/brokerage/products".split('?')[0] + ""
    signature = hmac.new(secretKey_coinbase.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()
    headers_binance = {
        'X-MBX-APIKEY': api_key_binance,
        'X-MBX-SECRETKEY': api_secret_binance
    }
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
    data_cmc_cap = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
    data_cmc = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
    data_binance = requests.get(url_binance, headers=headers_binance).json()
    data_coinbase = requests.get(url_coinbase, headers=headers_coinbase).json()
    data_okex = requests.get(url_okex).json()

    binance_hike_cap = [0, 0, 0]
    binance_drop_cap = [0, 0, 0]
    cb_hike_cap = [0, 0, 0]
    cb_drop_cap = [0, 0, 0]
    okex_hike_cap = [0, 0, 0]
    okex_drop_cap = [0, 0, 0]

    def get_cap_cmc(coin):
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '30c6565ce-18c1-4496-8727-02b12ece3299',
        }
        url_cmc_cap = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin}'
        data_cmc_cap = requests.get(url_cmc_cap, headers=headers).json()
        try:
            if float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap'])) > 0:
                return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['market_cap']))
            else:
                return float(round(data_cmc_cap['data'][f'{coin}']['quote']['USD']['fully_diluted_market_cap']))
        except KeyError:
            return 0

    def cut(num):
        num = round(num, 2)
        return num

    def format_number(num):
        formatted_num = "{:,.0f}".format(num).replace(',', '.')
        return formatted_num

    def name_edit(name):
        a = name[:-4]
        b = '-'
        c = name[-4:]
        name = a + b + c
        return name

    def del_zero(list):
        for i in range(3):
            while list[i][-1] == '0':
                list[i] = list[i][:-1]
        return list

    top3_filterred = [item for item in data_cmc['data']]
    top3_sorted = sorted(top3_filterred, key=lambda x: float(x['quote']['USD']['percent_change_24h']), reverse=True)
    top_names = [item["name"] for item in top3_sorted[:3]]
    top_volumes_24h = [round(float(item['quote']['USD']['percent_change_24h']), 2) for item in top3_sorted[:3]]

    # binance
    binance_filterred_gain_1 = [item for item in data_binance if
                                item["symbol"].endswith("USDC") or item["symbol"].endswith("USDT") or item[
                                    "symbol"].endswith("TUSD")]
    binance_filterred_gain_2 = [item for item in binance_filterred_gain_1 if float(item['quoteVolume']) > 0]

    binance_volume_sorted_data = sorted(binance_filterred_gain_2, key=lambda x: float(x["quoteVolume"]), reverse=True)

    binance_gain_names = [name_edit(item["symbol"]) for item in binance_volume_sorted_data[:3]]
    binance_gain_prices = [format_number(round(float(item["lastPrice"]))) for item in binance_volume_sorted_data[:3]]
    binance_gain_changes = [item["priceChangePercent"] for item in binance_volume_sorted_data[:3]]
    binance_gain_vols = [format_number(round(float(item["quoteVolume"]))) for item in binance_volume_sorted_data[:3]]

    binance_los_names = [name_edit(item["symbol"]) for item in binance_volume_sorted_data[-3:]]
    binance_los_prices = del_zero([item["lastPrice"] for item in binance_volume_sorted_data[-3:]])
    binance_los_changes = [item["priceChangePercent"] for item in binance_volume_sorted_data[-3:]]
    binance_los_vols = [format_number(round(float(item["quoteVolume"]))) for item in binance_volume_sorted_data[-3:]]
    binance_los_vols.reverse()

    # binance hike/drop
    binance_filterred_hike_1 = [item for item in data_binance if item["symbol"].endswith("USDT")]
    binance_filterred_hike_2 = [item for item in binance_filterred_hike_1 if float(item['quoteVolume']) > 0]

    change_sorted_data = sorted(binance_filterred_hike_2, key=lambda x: float(x["priceChangePercent"]), reverse=True)

    binance_hike_names = [item["symbol"][:-4] for item in change_sorted_data[:3]]
    binance_hike_price_changes = [cut(float(item["priceChangePercent"])) for item in change_sorted_data[:3]]

    binance_drop_names = [item["symbol"][:-4] for item in change_sorted_data[-3:]]
    binance_drop_price_changes = [item["priceChangePercent"] for item in change_sorted_data[-3:]]
    binance_drop_price_changes.reverse()

    # coinbase
    cb_filterred_gain_1 = [item for item in data_coinbase['products'] if
                           item["quote_currency_id"].endswith("USDC") or item["quote_currency_id"].endswith("USDT") or
                           item["quote_currency_id"].endswith("TUSD")]
    cb_filterred_gain_2 = [item for item in cb_filterred_gain_1 if item['price_percentage_change_24h'] != '']

    cb_volume_sorted_data = sorted(cb_filterred_gain_2, key=lambda x: float(float(x["volume_24h"]) * float(x["price"])),
                                   reverse=True)

    cb_gain_names = [item["product_id"] for item in cb_volume_sorted_data[:3]]
    cb_gain_prices = [format_number(float(item["price"])) for item in cb_volume_sorted_data[:3]]
    cb_gain_changes = [cut(float(item["price_percentage_change_24h"])) for item in cb_volume_sorted_data[:3]]
    cb_gain_vols = [format_number(float(item['volume_24h']) * float(item['price'])) for item in
                    cb_volume_sorted_data[:3]]
    cb_los_names = [item["product_id"] for item in cb_volume_sorted_data[-3:]]
    cb_los_prices = [item["price"] for item in cb_volume_sorted_data[-3:]]
    cb_los_changes = [cut(float(item["price_percentage_change_24h"])) for item in cb_volume_sorted_data[-3:]]
    cb_los_vols = [format_number(float(item['volume_24h']) * float(item['price'])) for item in
                   cb_volume_sorted_data[-3:]]
    cb_los_vols.reverse()
    # cb hike/drop
    cb_filterred_hike_1 = [item for item in data_coinbase['products'] if item["quote_currency_id"].endswith("USDT")]
    cb_filterred_hike_2 = [item for item in cb_filterred_hike_1 if item['price_percentage_change_24h'] != '']

    cb_change_sorted_data = sorted(cb_filterred_hike_2, key=lambda x: float(x["price_percentage_change_24h"]),
                                   reverse=True)
    cb_hike_names = [item["base_currency_id"] for item in cb_change_sorted_data[:3]]
    cb_hike_price_changes = [cut(float(item["price_percentage_change_24h"])) for item in cb_change_sorted_data[:3]]

    cb_drop_names = [item["base_currency_id"] for item in cb_change_sorted_data[-3:]]
    cb_drop_price_changes = [cut(float(item["price_percentage_change_24h"])) for item in cb_change_sorted_data[-3:]]
    cb_drop_price_changes.reverse()
    # okex
    okex_filterred_gain_1 = [item for item in data_okex['data'] if
                             item["instId"].endswith("USDC") or item["instId"].endswith("USDT") or item[
                                 "instId"].endswith("TUSD")]
    okex_filterred_gain_2 = [item for item in okex_filterred_gain_1 if float(item['last']) > 0]

    okex_volume_sorted_data = sorted(okex_filterred_gain_2, key=lambda x: float(x["volCcy24h"]), reverse=True)
    okex_gain_names = [item["instId"] for item in okex_volume_sorted_data[:3]]
    okex_gain_prices = [format_number(cut(float(item["last"]))) for item in okex_volume_sorted_data[:3]]
    okex_gain_changes = [cut((float(item['last']) / float(item['open24h']) * 100 - 100)) for item in
                         okex_volume_sorted_data[:3]]
    okex_gain_vols = [format_number(float(item['volCcy24h'])) for item in okex_volume_sorted_data[:3]]
    okex_los_names = [item["instId"] for item in okex_volume_sorted_data[-3:]]
    okex_los_prices = [float(item["last"]) for item in okex_volume_sorted_data[-3:]]
    okex_los_changes = [cut((float(item['last']) / float(item['open24h']) * 100 - 100)) for item in
                        okex_volume_sorted_data[-3:]]
    okex_los_vols = [format_number(float(item['volCcy24h'])) for item in okex_volume_sorted_data[-3:]]
    okex_los_vols.reverse()
    # okex hike/drop
    okex_filterred_hike_1 = [item for item in data_okex['data'] if item["instId"].endswith("USDT")]
    okex_filterred_hike_2 = [item for item in okex_filterred_hike_1 if float(item['last']) > 0]

    okex_change_sorted_data = sorted(okex_filterred_hike_2, key=lambda x: float(
        round((float(x['last']) / float(x['open24h']) * 100 - 100), 2)),
                                     reverse=True)
    okex_hike_names = [item["instId"][:-5] for item in okex_change_sorted_data[:3]]
    okex_hike_price_changes = [cut((float(item['last']) / float(item['open24h']) * 100 - 100)) for item in
                               okex_change_sorted_data[:3]]
    okex_drop_names = [item["instId"][:-5] for item in okex_change_sorted_data[-3:]]
    okex_drop_price_changes = [round((float(item['last']) / float(item['open24h']) * 100 - 100), 2) for item in
                               okex_change_sorted_data[-3:]]
    okex_drop_price_changes.reverse()

    for cap_value in range(3):
        binance_hike_cap[cap_value] = format_number(get_cap_cmc(binance_hike_names[cap_value]))
        binance_drop_cap[cap_value] = format_number(get_cap_cmc(binance_drop_names[cap_value]))
        cb_hike_cap[cap_value] = format_number(get_cap_cmc(cb_hike_names[cap_value]))
        cb_drop_cap[cap_value] = format_number(get_cap_cmc(cb_drop_names[cap_value]))
        okex_hike_cap[cap_value] = format_number(get_cap_cmc(okex_hike_names[cap_value]))
        okex_drop_cap[cap_value] = format_number(get_cap_cmc(okex_drop_names[cap_value]))

    top3 = ''
    temp_variable_for_tops = ''
    for top3_value in range(3):
        top3 += f"<li>{top_names[top3_value]} - {top_volumes_24h[top3_value]}%</li>"
        temp_variable_for_tops += f"{top_names[top3_value]} - {top_volumes_24h[top3_value]}%, "

    binance_gain_text = ''
    binance_los_text = ''
    cb_gain_text = ''
    cb_los_text = ''
    okex_gain_text = ''
    okex_los_text = ''

    news = ['okex', 'binance', 'coinbase']

    for names in range(3):
        news.append(binance_gain_names[names][:-5].lower())
        news.append(binance_los_names[names][:-5].lower())
        news.append(cb_gain_names[names][:-5].lower())
        news.append(cb_los_names[names][:-5].lower())
        news.append(okex_gain_names[names][:-5].lower())
        news.append(okex_los_names[names][:-5].lower())

        news.append(binance_hike_names[names].lower())
        news.append(binance_drop_names[names].lower())
        news.append(cb_hike_names[names].lower())
        news.append(cb_drop_names[names].lower())
        news.append(okex_hike_names[names].lower())
        news.append(okex_drop_names[names].lower())

    news_5 = fetch_crypto_news(news, 5)
    news_text = ''

    for news_value in range(len(news_5)):
        news_text += news_5[news_value]

    for gain_los in range(3):
        binance_gain_text += f"<li>{binance_gain_names[gain_los]} - {binance_gain_prices[gain_los]}$, {binance_gain_changes[gain_los]}%, {binance_gain_vols[gain_los]}$ </li>"
        binance_los_text += f"<li>{binance_los_names[gain_los]} - {binance_los_prices[gain_los]}$, {binance_los_changes[gain_los]}%, {binance_los_vols[gain_los]}$ </li>"
        cb_gain_text += f"<li>{cb_gain_names[gain_los]} - {cb_gain_prices[gain_los]}$, {cb_gain_changes[gain_los]}%, {cb_gain_vols[gain_los]}$ </li>"
        cb_los_text += f"<li>{cb_los_names[gain_los]} - {cb_los_prices[gain_los]}$, {cb_los_changes[gain_los]}%, {cb_los_vols[gain_los]}$ </li>"
        okex_gain_text += f"<li>{okex_gain_names[gain_los]} - {okex_gain_prices[gain_los]}$, {okex_gain_changes[gain_los]}%, {okex_gain_vols[gain_los]}$ </li>"
        okex_los_text += f"<li>{okex_los_names[gain_los]} - {okex_los_prices[gain_los]}$, {okex_los_changes[gain_los]}%, {okex_los_vols[gain_los]}$ </li>"

    binance_hike_text = ''
    binance_drop_text = ''
    cb_hike_text = ''
    cb_drop_text = ''
    okex_hike_text = ''
    okex_drop_text = ''

    for hike_drop in range(3):
        binance_hike_text += f"<li>{binance_hike_names[hike_drop]}: {binance_hike_price_changes[hike_drop]}% (Market cap for now: {binance_hike_cap[hike_drop]}$)</li>"
        binance_drop_text += f"<li>{binance_drop_names[hike_drop]}: {binance_drop_price_changes[hike_drop]}% (Market cap for now: {binance_drop_cap[hike_drop]}$)</li>"
        cb_hike_text += f"<li>{cb_hike_names[hike_drop]}: {cb_hike_price_changes[hike_drop]}% (Market cap for now: {cb_hike_cap[hike_drop]}$)</li>"
        cb_drop_text += f"<li>{cb_drop_names[hike_drop]}: {cb_drop_price_changes[hike_drop]}% (Market cap for now: {cb_drop_cap[hike_drop]}$)</li>"
        okex_hike_text += f"<li>{okex_hike_names[hike_drop]}: {okex_hike_price_changes[hike_drop]}% (Market cap for now: {okex_hike_cap[hike_drop]}$)</li>"
        okex_drop_text += f"<li>{okex_drop_names[hike_drop]}: {okex_drop_price_changes[hike_drop]}% (Market cap for now: {okex_drop_cap[hike_drop]}$)</li>"

    exchange_name = ''
    max_coin = ''

    all_hikes = []
    for hike in range(3):
        all_hikes.append(float(binance_hike_price_changes[hike]))
        all_hikes.append(float(cb_hike_price_changes[hike]))
        all_hikes.append(float(okex_hike_price_changes[hike]))
    all_hikes_names = []
    for coin_name in range(3):
        all_hikes_names.append(binance_hike_names[coin_name])
        all_hikes_names.append(cb_hike_names[coin_name])
        all_hikes_names.append(okex_hike_names[coin_name])

    max_coin = all_hikes_names[all_hikes.index(max(all_hikes))]
    if max(all_hikes) in binance_hike_price_changes:
        exchange_name = 'BINANCE'
    elif max(all_hikes) in cb_hike_price_changes:
        exchange_name = 'Coinbase'
    elif max(all_hikes) in okex_hike_price_changes:
        exchange_name = 'OKEX'
    max_hike = max(all_hikes)

    date = str(datetime.today())[:10]
    date_2 = datetime.strptime(date, '%Y-%m-%d')
    full_date = date_2.strftime('%B %d %Y')

    def create_preview():

        def get_text_dimensions(text_string, font):
            ascent, descent = font.getmetrics()

            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent

            return (text_width, text_height)

        background = Image.open("pics/Banner.jpg")
        img_width, img_height = background.size

        coin_text = max_coin
        exchange_text = exchange_name
        percent_text = f'{max_hike}%'
        date_text = full_date

        font_coin = ImageFont.truetype('fonts/Martian Fonts - Martian Grotesk UWd Md.ttf', size=50)
        font_exchange = ImageFont.truetype('fonts/Martian Fonts - Martian Grotesk XWd XBd.ttf', size=30)
        font_percent = ImageFont.truetype('fonts/Martian Fonts - Martian Grotesk Nr Th.ttf', size=110)
        font_date = ImageFont.truetype('fonts/Exo-Bold.ttf', size=25)

        coin_text_width, coin_text_height = get_text_dimensions(coin_text, font_coin)
        coordinat_coin = img_width - coin_text_width - 480
        coin = ImageDraw.Draw(background)
        coin.text((coordinat_coin, 250), coin_text, font=font_coin, fill='white')

        percent_text_width, percent_text_height = get_text_dimensions(percent_text, font_percent)
        coordinat_percent = img_width - percent_text_width - 480
        percent = ImageDraw.Draw(background)
        percent.text((coordinat_percent, 310), percent_text, font=font_percent, fill='white')

        exchange_text_width, exchange_text_height = get_text_dimensions(exchange_text, font_exchange)
        coordinat_exchange = img_width - exchange_text_width - 480
        exchange = ImageDraw.Draw(background)
        exchange.text((coordinat_exchange, 460), exchange_text, font=font_exchange, fill='white')

        date = ImageDraw.Draw(background)
        date.text((50, 730), date_text, font=font_date, fill='white', align='left')

        return background.save('pics/generated_preview.jpg')

    create_preview()

    head_static = 'Every day we look through the data from the biggest crypto exchanges to collect the most important stat about cryptos'
    head_promt = f'write a text that is similar in meaning and size: {head_static}'
    head_text = open_ai.generate_title(head_promt)

    gainers_promt = f'briefly сomment on top gainers with 24h volume {binance_gain_names[0]} {binance_gain_vols[0]}, {cb_gain_names[0]} {cb_gain_vols[0]}, {okex_gain_names[0]} {okex_gain_vols[0]}'
    gainers_text = open_ai.generate_title(gainers_promt)

    hike_promt = f'briefly сomment on top price hikes {binance_hike_names[0]} {binance_hike_price_changes[0]} {cb_hike_names[0]} {cb_hike_price_changes[0]} {okex_hike_names[0]} {okex_hike_price_changes[0]}'
    hike_text = open_ai.generate_title(hike_promt)

    losers_promt = f'briefly сomment on top losers with 24h volume {binance_los_names[0]} {binance_los_vols[0]}, {cb_los_names[0]} {cb_los_vols[0]}, {okex_los_names[0]} {okex_los_vols[0]}'
    losers_text = open_ai.generate_title(losers_promt)

    drop_promt = f'briefly сomment on top price drops {binance_drop_names[0]} {binance_drop_price_changes[0]} {cb_drop_names[0]} {cb_drop_price_changes[0]} {okex_drop_names[0]} {okex_drop_price_changes[0]}'
    drop_text = open_ai.generate_title(drop_promt)

    title_promt = f'Write a headline, without time and dates and with all coin percentages, that will indicate that trading on a crypto exchange closed with the values of such coins - {temp_variable_for_tops}.'
    title = open_ai.generate_title(title_promt)
    text_all = create_text('text')

    lst1 = [head_text, top3, gainers_text, binance_gain_text, cb_gain_text, okex_gain_text, hike_text,
            binance_hike_text, cb_hike_text, okex_hike_text, losers_text,
            binance_los_text, cb_los_text, okex_los_text, drop_text, binance_drop_text, cb_drop_text, okex_drop_text,
            news_text]

    lst2 = ['{head_text}', '{top3}', '{gainers_text}', '{binance_gain_text}', '{cb_gain_text}', '{okex_gain_text}',
            '{hike_text}', '{binance_hike_text}', '{cb_hike_text}', '{okex_hike_text}', '{losers_text}',
            '{binance_los_text}', '{cb_los_text}', '{okex_los_text}', '{drop_text}', '{binance_drop_text}',
            '{cb_drop_text}', '{okex_drop_text}', '{news_text}']

    for i in range(len(lst1)):
        if lst2[i] in text_all:
            text_all = text_all.replace(lst2[i], str(lst1[i]))

    print('Text created')
    pic = 'pics/generated_preview.jpg'
    # pic = 'https://www.colorado.edu/ecenter/sites/default/files/styles/medium/public/article-thumbnail/cryptocurrency.png?itok=HHvIzV6z'
    # btc = open('btc.jpeg', 'rb')
    # img = cv2.imread('btc.jpeg')
    # string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    # print(binance_hike_names)
    # print(cb_hike_names)
    # print(okex_hike_names)
    # print(binance_hike_price_changes)
    # print(cb_hike_price_changes)
    # print(okex_hike_price_changes)
    push_post(title, text_all, pic)


main()
