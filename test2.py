from datetime import datetime

date = str(datetime.today())[:10]
date_2 = datetime.strptime(date, '%Y-%m-%d')
full_date = date_2.strftime('%B %d %Y')

# binance_hike_names = ['b1', 'b2', 'b3']
# cb_hike_names = ['c1', 'c2', 'c3']
# okex_hike_names = ['o1', 'o2', 'o3']
#
# binance_hike_price_changes = [5.6, 98.2, 10.2]
# cb_hike_price_changes = [1.2, 988, 125.9]
# okex_hike_price_changes = [6.5, 5555.9, 22.2]
#
# exchange_name = ''
# coin = ''
#
# all_hikes = []
# for i in range(3):
#     all_hikes.append(binance_hike_price_changes[i])
#     all_hikes.append(cb_hike_price_changes[i])
#     all_hikes.append(okex_hike_price_changes[i])
# all_hikes_names = []
# for j in range(3):
#     all_hikes_names.append(binance_hike_names[j])
#     all_hikes_names.append(cb_hike_names[j])
#     all_hikes_names.append(okex_hike_names[j])
#
# coin = all_hikes_names[all_hikes.index(max(all_hikes))]
# if max(all_hikes) in binance_hike_price_changes:
#     exchange_name = 'BINANCE'
# elif max(all_hikes) in cb_hike_price_changes:
#     exchange_name = 'Coinbase'
# elif max(all_hikes) in okex_hike_price_changes:
#     exchange_name = 'OKEX'
# print(coin)
# print(max(all_hikes))
# print(exchange_name)







