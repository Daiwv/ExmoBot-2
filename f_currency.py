# -*- coding: utf-8 -*-
import time
#import _ExmoAPI
from ted import *
from _CLASS import Tactic, Pair
import _ExmoAPI
import f_print
import f_tactic
import f_string
import g

def get_active_trade_pair(pair_nr):
    try:
       active_trade_pair = -1
       free_currency_nr = get_free_currency_nr()

       if (free_currency_nr >= 0):
           print
           print '> free currency ', f_string.get_str_currency(free_currency_nr)
           active_trade_pair = f_tactic.check_tactic(pair_nr, free_currency_nr)
           if (active_trade_pair >= 0):
              print '> active_trade_pair:',  f_string.get_str_pairs_nr(active_trade_pair)
           else:
               time.sleep(10)
       else:
           active_trade_pair =-1
           time.sleep(10)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return active_trade_pair

def get_pairs_nr(first, second):
   pair =-1
   if first==BTC and second==USD:
     pair=BTC_USD
   elif first==BTC and second==RUB:
     pair=BTC_RUB
   elif first==ETH and second==RUB:
     pair=ETH_RUB
   elif first==ETH and second==USD:
     pair=ETH_USD
   elif first==ETH and second==BTC:
     pair=ETH_BTC
   elif first==USD and second==RUB:
     pair=USD_RUB
   return pair

def get_zone(last_preis, avg, low, high):
    try:
    #                       Zone 5               #
    # xPrice[4]------------------------------high #
    #                       Zone 4               #
    # xPrice[3]-----------------------------------#
    #                       Zone 3               #
    # xPrice[2]-------------------------------avg #
    #                       Zone 2               #
    # xPrice[1]-----------------------------------#
    #                       Zone 1               #
    # xPrice[0]-------------------------------low #
    #                       Zone 0               #
       xPrice={}
       xPrice[0] = low
       xPrice[1] = low  + (avg  - low ) * 0.5
       xPrice[2] = avg
       xPrice[3] = high  - (avg  - low ) * 0.5
       xPrice[4] = high

       z = 0
       if (last_preis > xPrice[0]) and (last_preis <= xPrice[1]):
           z = 1
       elif (last_preis > xPrice[1]) and (last_preis <= xPrice[2]):
           z = 2
       elif (last_preis > xPrice[2]) and (last_preis <= xPrice[3]):
           z = 3
       elif (last_preis > xPrice[3]) and (last_preis <= xPrice[4]):
           z = 4
       elif (last_preis > xPrice[4]):
           z = 5
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return z

def get_free_currency_nr():
    try:
       free_currency_nr = -1
       free_currency = g.pair_instance.free_currency
       nr = 0  # check all
       for nxt in free_currency:
           if (free_currency[nr] >= MIN_TO_TRADE[nr]):
               free_currency_nr = nr
               break
           nr += 1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return free_currency_nr

def get_current_currency():
    pair_nr=-1
    first_currency=-1
    second_currency=-1
    try:
       pair_nr = g.pair_instance.get_pair_nr()
       first_currency = get_first_currency(pair_nr)
       second_currency = get_second_currency(pair_nr)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return pair_nr, first_currency, second_currency

def get_alternative_first_and_second_currency(pair_nr):
    pair_to_trade_T1 = get_second_pair(pair_nr)
    alt_first_curr_T1 = get_first_currency(pair_to_trade_T1)
    alt_second_curr_T1 = get_second_currency(pair_to_trade_T1)
    return alt_first_curr_T1, alt_second_curr_T1

def get_second_pair(pair_nr):
    try:
        f_currency=get_first_currency(pair_nr)
        s_currency=get_second_currency(pair_nr)
        second_pair =-1
        if (f_currency == BTC) and (s_currency == USD):
            second_pair = ETH_RUB
        elif (f_currency == ETH) and (s_currency == USD):
            second_pair = BTC_RUB
        elif (f_currency == BTC) and (s_currency == RUB):
            second_pair = ETH_USD
        elif (f_currency == ETH) and (s_currency == RUB):
            second_pair = BTC_USD
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return second_pair

def get_first_currency(pair_nr):
    first=-1
    if (pair_nr == BTC_USD) or (pair_nr == BTC_RUB):
        first=BTC
    elif (pair_nr == ETH_USD) or (pair_nr == ETH_RUB):
        first=ETH
    elif (pair_nr == USD_RUB):
        first=USD
    elif (pair_nr == ETH_BTC):
        first=ETH
    return first

def get_second_currency(pair_nr):
    second=-1
    if (pair_nr == BTC_USD) or (pair_nr == ETH_USD):
        second=USD
    elif (pair_nr == BTC_RUB) or (pair_nr == ETH_RUB) or (pair_nr == USD_RUB):
        second=RUB
    elif (pair_nr == ETH_BTC):
        second=BTC
    return second

def get_bid_and_ask():
    try:
       avg_bid_ask = g.pair_instance.get_bid_ask()[AVG_BID_ASK_NR]
       aBid = g.pair_instance.get_bid_ask()[BID_NR]
       aAsk = g.pair_instance.get_bid_ask()[ASK_NR]
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return aBid, aAsk, avg_bid_ask

def check_aAsk(aAsk, price, fist_currency):
    if (price < aAsk):
        #print price, '<', aAsk
        price = aAsk + aAsk / 10000
        print '|  price = aAsk+aAsk/10000 :', round(price, DECIMAL_PART[fist_currency])
    return price

def check_aBid(aBid, price, second_currency):
    if (price > aBid):
        price = aBid - aBid / 1000
        print '|  price = aBid-aBid/1000 :', round(price, DECIMAL_PART[second_currency])
    return price

def get_currency(pair_nr):
    first= get_first_currency(pair_nr)
    second = get_second_currency(pair_nr)
    return first, second

def refresh_and_get_free_currency( ):
    try:
       _ExmoAPI.get_status(g.exmoAPI_instance, g.pair_instance)  # refresh data
       free_currency = g.pair_instance.get_free_currency()
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return free_currency

def check_free_min(currency_free, min):
    if (currency_free > min) and (currency_free < 2 * min):
        min = currency_free
    #if (TACTIC_FIX_PRICE == 1):
        #min=currency_free
    return min