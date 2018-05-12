# -*- coding: utf-8 -*-
import time
from g import *
from ted import *
from _CLASS import Tactic
import f_print
import f_currency
import f_main
import f_string

# 0 - no tactic
# 1 - TACTIC_USE_SECOND_PAIR
# 10 - TACTIC_CHECK_MIN_MAX_BTC
# 100 - TACTIC_CHECK_MIN_MAX_ETH
# 1000 - TACTIC_USE_CORRIDOR
# 10000 - TACTIC_FIX_PRICE
def check_tactic(pair_nr, free_currency_nr):
    try:
       active_trade_pair=-1
       tactic = Tactic()  # make objekt tactic and read data
       tactic_rate = tactic.get_tactic_rate()

       if (tactic_rate==1):
           #TACTIC_USE_SECOND_PAIR
           pair_nr = check_1_tactic(pair_nr, free_currency_nr)

       if (tactic_rate > 1):
           # check min and max
           pair_nr = check_tactic_min_max(pair_nr, tactic_rate)

           if (tactic_rate==0) or (tactic_rate==10) or (tactic_rate==100) or (tactic_rate==1000) or (tactic_rate==10000):
               #Do something
               print '!'
       #No tactic-check for last choice
       #Checking the free currency and pair-currency (e.g. USD -> BTC/USD)
       if (tactic_rate==0) or (pair_nr>=0):
          active_trade_pair = check_free_currency_and_pair(pair_nr, free_currency_nr)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return active_trade_pair


# 0 - no tactic
# 1 - TACTIC_USE_SECOND_PAIR
# 10 - TACTIC_CHECK_MIN_MAX_BTC
# 100 - TACTIC_CHECK_MIN_MAX_ETH
# 1000 - TACTIC_USE_CORRIDOR
# 10000 - TACTIC_FIX_PRICE
def check_tactic_min_max (pair_nr, tactic_rate):
    try:
       active_trade_pair=-1
       result=1
       if (TACTIC_CHECK_MIN_MAX_BTC==1) and (tactic_rate==10):
          f_main.ini(BTC_USD)  # refresh for new pair
          result_min_max_btc = check_2_tactic(tactic_rate)
          if (result_min_max_btc > 0):
              print '> min/max BTC-price checked: OK'
              active_trade_pair = pair_nr
          elif (result_min_max_btc == 0):
              print 'min/max BTC-price checked: NO',
              time.sleep(100)
              active_trade_pair=-1

       if (TACTIC_CHECK_MIN_MAX_ETH==1)and (tactic_rate==100):
          f_main.ini(ETH_USD)  # refresh for new pair
          result_min_max_eth = check_3_tactic(tactic_rate)
          if (result_min_max_eth > 0):
              print '> min/max ETH-price checked: OK'
              active_trade_pair = pair_nr
          elif (result_min_max_eth == 0):
              print 'min/max ETH-price checked: NO',
              time.sleep(100)
              active_trade_pair = -1

       if (TACTIC_USE_CORRIDOR==1) and ((tactic_rate==1000) or (tactic_rate==1001)):
          f_main.ini(pair_nr)  # refresh for new pair
          result_inside_the_corridor= check_4_tactic(tactic_rate, pair_nr)
          if (result_inside_the_corridor > 0):
              print '> inside the corridor [ up', MIN_CORRIDOR ,'to', MAX_CORRIDOR,
              print f_string.get_str_pairs_nr(pair_nr),'] checked: OK'
              active_trade_pair = pair_nr
          elif (result_inside_the_corridor == 0):
              print '> inside the corridor [ up', MIN_CORRIDOR ,'to', MAX_CORRIDOR,
              print  f_string.get_str_pairs_nr(pair_nr),'] checked: NO',
              #time.sleep(100)
              if (CHANGE_PAIR==1):# Use the another pair
                  try:
                     new_pair_nr=f_currency.get_pairs_nr(CHANGED_FIRST_CURRENCY, CHANGED_SECOND_CURRENCY)
                    #f_main.ini(new_pair_nr)  # refresh for new pair
                     active_trade_pair=new_pair_nr
                  except:
                      f_print.print_exception(sys._getframe().f_code.co_name +  'CHANGED CURRENCY')
              else:
                  active_trade_pair = -1

       #if (TACTIC_FIX_PRICE==1) and (tactic_rate==10000):
       #   f_main.ini(pair_nr)  # refresh for new pair
       #   result_fix_price = check_5_tactic(tactic_rate, pair_nr)
       #   if (result_fix_price > 0):
       #       print '> inside the fixed prices [ min', MIN_FIX ,'- max', MAX_FIX,
       #       print f_string.get_str_pairs_nr(pair_nr),'] checked: OK'
       #       active_trade_pair = pair_nr
       #   elif (result_inside_the_corridor == 0):
       #       print '> inside the fixed prices [ min', MIN_FIX ,'max', MAX_FIX,
       #       print  f_string.get_str_pairs_nr(pair_nr),'] checked: NO',
       #       time.sleep(100)
       #       active_trade_pair=-1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return active_trade_pair

def check_free_currency_and_pair(pair_nr, free_currency_nr):
    try:
       first_currency, second_currency = f_currency.get_currency(pair_nr)
       if (first_currency == free_currency_nr) or (second_currency == free_currency_nr):
           active_trade_pair = pair_nr
       else:
           print '> for the pair', f_string.get_str_pairs_nr(pair_nr), 'currency not found'
           active_trade_pair=-1
           time.sleep(1)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return active_trade_pair

def check_1_tactic(pair_nr, free_currency_nr):
    # only 1. TACTIC_USE_SECOND_PAIR
    try:
       active_trade_pair=check_free_currency_and_pair(pair_nr, free_currency_nr)
       if (active_trade_pair < 0):
          alt_first_curr_T1, alt_second_curr_T1 = f_currency.get_alternative_first_and_second_currency(pair_nr)
          if (alt_first_curr_T1 == free_currency_nr) or (alt_second_curr_T1 == free_currency_nr):
             active_trade_pair = f_currency.get_pairs_nr(alt_first_curr_T1, alt_second_curr_T1)
          else:
              active_trade_pair=-1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return active_trade_pair

def check_2_tactic(tactic_rate):
    try:
       result=-1
       # only 2. TACTIC_CHECK_MIN_MAX_BTC
       if (TACTIC_CHECK_MIN_MAX_BTC==1) and (tactic_rate == 10):  # only tactic_2 selected
           aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
           btc_price = avg_bid_ask
           print '> BTC-price:', round(btc_price, DECIMAL_PART[USD]), 'USD'
           result = 0
           if (btc_price >= MIN_BTC_USD) and (btc_price <= MAX_BTC_USD):
                result = 1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return result

def check_3_tactic(tactic_rate):
    try:
       result=-1
       # only 3. TACTIC_CHECK_MIN_MAX_ETH
       if (TACTIC_CHECK_MIN_MAX_ETH==1) and (tactic_rate == 100):  # only tactic_3 selected
           aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
           eth_price = avg_bid_ask
           print '> ETH-price:', round (eth_price, DECIMAL_PART[USD]), 'USD'
           result = 0
           if (eth_price >= MIN_ETH_USD) and (eth_price <= MAX_ETH_USD):
               result = 1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return result

def check_4_tactic(tactic_rate, pair_nr):
    try:
       result=-1
       # only 4. TACTIC_USE_CORRIDOR
       if (TACTIC_USE_CORRIDOR==1) and ((tactic_rate == 1000) or (tactic_rate == 1001)) :  # only tactic_4 selected
           aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
           print '> Price:',
           print round (avg_bid_ask, DECIMAL_PART[f_currency.get_second_currency(pair_nr)]),
           print f_string.get_str_pairs_nr(pair_nr)
           result = 0
           if (avg_bid_ask >= MIN_CORRIDOR) and (avg_bid_ask <= MAX_CORRIDOR):
               result = 1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return result

def check_5_tactic(tactic_rate, pair_nr):
    try:
       result=-1
       # only 4. TACTIC_FIX_PRICE
       if (TACTIC_FIX_PRICE==1) and (tactic_rate == 10000):  # only tactic_5 selected
           aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
           print '> Price:',
           print round (avg_bid_ask, DECIMAL_PART[f_currency.get_second_currency(pair_nr)]),
           print f_string.get_str_pairs_nr(pair_nr)
           result = 0
           if (avg_bid_ask >= MIN_FIX) and (avg_bid_ask <= MAX_FIX):
               result = 1
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return result