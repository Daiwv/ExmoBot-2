# -*- coding: utf-8 -*-
from g import *

#TED-Data
FIRST_CURRENCY     = BTC       #Head-Currency
SECOND_CURRENCY    = USD       #Second-Currency
MIN_DIFFERENCE     = 1.0       #MIN_DIFFERENCE at sell/buy [%]

#Tactic
# Priority (if all tactic checked):
# TACTIC_USE_SECOND_PAIR = TACTIC_CHECK_MIN_MAX_BTC
# TACTIC_USE_SECOND_PAIR = TACTIC_CHECK_MIN_MAX_ETH
# TACTIC_CHECK_MIN_MAX_ETH > TACTIC_USE_CORRIDOR > TACTIC_FIX_PRICE
TACTIC_USE_SECOND_PAIR   = 1   #Use the second pair (automatic)                                  #tactic 1

TACTIC_USE_ORDER_BOOK    = 1   #Use the prices and quantity from the book
NUMBER_OF_RECORDS        = 500 #Up 100 to 1000
BTC_MAX_ASK_QUANTITY     = 5   #Max Quantity of BTC
ETH_MAX_ASK_QUANTITY     = 20  #Max Quantity of ETH

TACTIC_USE_FIX_PRICE     = 1   #Use the fix prices
BTC_USD_FIX_1 = 9888
BTC_USD_FIX_2 = 9999
BTC_RUB_FIX_1 = 600000
BTC_RUB_FIX_2 = 360000
ETH_USD_FIX_1 = 999
ETH_USD_FIX_2 = 375
ETH_RUB_FIX_1 = 40000
ETH_RUB_FIX_2 = 20000
USD_RUB_FIX_1 = 59.5
USD_RUB_FIX_2 = 59.8


TACTIC_CHECK_MIN_MAX_BTC = 0   #Use the other pair if BTC > MAX_BTC or BTC < MIN_BTC(automatic)  #tactic 2 (10)
MIN_BTC_USD = 9200
MAX_BTC_USD = 12000

TACTIC_CHECK_MIN_MAX_ETH = 0   #Use the other pair if ETH > MAX_ETH or ETH < MIN_ETH             #tactic 3 (100)
MIN_ETH_USD = 350
MAX_ETH_USD = 900

TACTIC_USE_CORRIDOR      = 0   #Use the corridor of prices  (arbitrary currency)                 #tactic 4 (1000)
MIN_CORRIDOR = 9100
MAX_CORRIDOR = 12400
CHANGE_PAIR  = 0
CHANGED_FIRST_CURRENCY  = USD

MIN_TO_TRADE = {}
MIN_TO_TRADE[BTC]   = 0.0010001
MIN_TO_TRADE[USD]   = 15
MIN_TO_TRADE[ETH]   = 0.010001
MIN_TO_TRADE[RUB]   = 600

DECIMAL_PART={}
DECIMAL_PART[BTC]   = 5         #Decimal Part
DECIMAL_PART[USD]   = 2         #Decimal Part
DECIMAL_PART[ETH]   = 4         #Decimal Part
DECIMAL_PART[RUB]   = 2         #Decimal Part

# коэффициент для расчета начальной цены покупки или продажи
# используется для подгона начальный цены под "заглушки"
# 0.001 здесь - это суммированный минимальный объем продажи (или покупки) от середины стакана
# TODO для разных валют это величина разная. Надо сделать для каждой отдельно или совсем убрать.
# Поэтому сделаю пока минимум, ca. 0
AM_LIM= 0.001