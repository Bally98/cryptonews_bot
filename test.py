import requests
api_key_cmc = '3c6565ce-18c1-4496-8727-02b12ece3299'
url_cmc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers_cmc = {
    'X-CMC_PRO_API_KEY': api_key_cmc
}

params_cmc = {
    'convert': 'USD',
    'symbol':'BTC',
}
data_cmc = requests.get(url_cmc, params=params_cmc, headers=headers_cmc).json()
print(data_cmc)
# top1_name = ''
# top2_name = ''
# top3_name = ''
# top1_volume_24h = 0
# top2_volume_24h = 0
# top3_volume_24h = 0
#
# for cmc_value in data_cmc['data']:
#     if cmc_value['quote']['USD']['percent_change_24h'] > top1_volume_24h:
#         top3_volume_24h = top2_volume_24h
#         top2_volume_24h = top1_volume_24h
#         top1_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#         top1_name = cmc_value['name']
#     elif cmc_value['quote']['USD']['percent_change_24h'] > top2_volume_24h:
#         top3_volume_24h = top2_volume_24h
#         top2_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#         top2_name = cmc_value['name']
#     elif cmc_value['quote']['USD']['percent_change_24h'] > top3_volume_24h:
#         top3_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#         top3_name = cmc_value['name']
#
# print(f'Top 1 - {top1_name}:{top1_volume_24h}%\nTop 2 - {top2_name}:'
#              f'{top2_volume_24h}%\nTop 3 - {top3_name}:{top3_volume_24h}%\n ')


# def get_3_biggest_crypto():
#     top1_name = ''
#     top2_name = ''
#     top3_name = ''
#     top1_volume_24h = 0
#     top2_volume_24h = 0
#     top3_volume_24h = 0
#     a = 0
#     for cmc_value in data_cmc['data']:
#         a += 1
#         print(a, cmc_value['name'])
#         if cmc_value['name'] != None and cmc_value['name'] != '':
#             if cmc_value['quote']['USD']['percent_change_24h'] > top1_volume_24h:
#                 top3_volume_24h = top2_volume_24h
#                 top2_volume_24h = top1_volume_24h
#                 top1_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#                 top1_name = cmc_value['name']
#             elif cmc_value['quote']['USD']['percent_change_24h'] > top2_volume_24h:
#                 top3_volume_24h = top2_volume_24h
#                 top2_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#                 top2_name = cmc_value['name']
#             elif cmc_value['quote']['USD']['percent_change_24h'] > top3_volume_24h:
#                 top3_volume_24h = round(float(cmc_value['quote']['USD']['percent_change_24h']), 2)
#                 top3_name = cmc_value['name']
#
#     return print(f'Top 1 - {top1_name}:{top1_volume_24h}%\nTop 2 - {top2_name}:'
#                  f'{top2_volume_24h}%\nTop 3 - {top3_name}:{top3_volume_24h}%\n ')
#
# get_3_biggest_crypto()








