# -*- coding: utf-8 -*-

exmoAPI_instance = None
pair_instance = None
min_price=0
max_price=0
list_open_old = []
BTC   = 0
ETH   = 1
USD   = 2
RUB   = 3

BTC_USD=0
ETH_USD=1
BTC_RUB=2
ETH_RUB=3
ETH_BTC=4
USD_RUB=5

PAIR_STRING=['btc_usd', 'eth_usd', 'btc_rub', 'eth_rub', 'eth_btc', 'usd_rub']

AVG_NR=0
MIN_NR=1
MAX_NR=2

AVG_BID_ASK_NR = 0
BID_NR = 1
ASK_NR = 2

am_lim = 0.0001

#pairs = ['btc_usd', 'eth_usd', 'btc_rub', 'eth_rub', 'eth_btc', 'usd_rub']
# статистические данные, собранные с помощью API за последне 24 часа
# [0]-BTC/USD... [5]-USD/RUB.
vBids = [0, 0, 0, 0, 0, 0]  # предложения покупки в стакане с учетом коэффициента по объемам (учет заглушек)
vAsks = [0, 0, 0, 0, 0, 0]  # предложения продажи в стакане с учетом коэффициента по объемам (учет заглушек)
aBids = [0, 0, 0, 0, 0, 0]  # актульные предложения покупки в стакане
aAsks = [0, 0, 0, 0, 0, 0]  # актуальные предложения продажи в стакане



