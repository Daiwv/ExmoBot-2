# -*- coding: utf-8 -*-
from _CLASS import Pair
import  g
from ted import *
from _ExmoAPI import *
import f_string
import f_currency
import time



def print_info():
    try:
       #print 'print_info'
       #print_all_free_currency()
       print_pair()
       #print_zone()
    except:
        print 'Error: print_info'

def print_TED (ted):
    decimal_part = ted.get_decimal_part()
    min_value_to_trade = ted.get_minvalue()
    print '-----------------------------------------------------------------------------'
    print '                  TED (ted.py)                                               '
    print '-----------------------------------------------------------------------------'
    print '   Min value to trade   ', get_str_currency(BTC), round(min_value_to_trade[BTC], decimal_part[BTC]),
    print '  ',    get_str_currency(ETH), round(min_value_to_trade[ETH], decimal_part[ETH]),
    print '  ',    get_str_currency(USD), round(min_value_to_trade[USD], decimal_part[USD]),
    print '  ',    get_str_currency(RUB), round(min_value_to_trade[RUB], decimal_part[RUB])
    print '   Min Difference       ', ted.get_min_difference(), '[%]'
    print '-----------------------------------------------------------------------------'




def print_tactic(pair_nr):
    try:
        tactic = Tactic()  # make objekt tactic and read data
        tactic_rate = tactic.get_tactic_rate()
        #print '-----------------------------------------------------------------------------'
        print '  Tactic rate =', tactic_rate
        if (TACTIC_USE_SECOND_PAIR == 1):
            print '  TACTIC : FIRST PAIR =', f_string.get_str_pairs_nr(pair_nr), '     SECOND PAIR =',
            print f_string.get_str_pairs_nr(f_currency.get_second_pair(pair_nr))

        if (TACTIC_USE_ORDER_BOOK == 1):
            print '  TACTIC : USE ORDER BOOK (ASK AND BID) WITH NUMBER OF RECORDS', NUMBER_OF_RECORDS
            print '           QUANTITY','{:>3}'.format(BTC_MAX_ASK_QUANTITY), 'BTC', '{:>3}'.format(ETH_MAX_ASK_QUANTITY), 'ETH'
        if (TACTIC_USE_FIX_PRICE == 1):
            print '  TACTIC : USE FIXED PRICES   BTC', '{:>10}'.format(BTC_USD_FIX_1), 'USD', '{:>10}'.format(BTC_USD_FIX_2), 'USD'
            print '                              BTC', '{:>10}'.format(BTC_RUB_FIX_1), 'RUB', '{:>10}'.format(BTC_RUB_FIX_2), 'RUB'
            print '                              ETH', '{:>10}'.format(ETH_USD_FIX_1), 'USD', '{:>10}'.format(ETH_USD_FIX_2), 'USD'
            print '                              ETH', '{:>10}'.format(ETH_RUB_FIX_1), 'RUB', '{:>10}'.format(ETH_RUB_FIX_2), 'RUB'
            print '                              USD', '{:>10}'.format(USD_RUB_FIX_1), 'RUB', '{:>10}'.format(USD_RUB_FIX_2), 'RUB'

        if (TACTIC_CHECK_MIN_MAX_BTC == 1):
            print '  TACTIC : CHECK BTC MIN', MIN_BTC_USD, '[USD] TO MAX', MAX_BTC_USD, '[USD]'
        if (TACTIC_CHECK_MIN_MAX_ETH == 1):
            print '  TACTIC : CHECK ETH MIN', MIN_ETH_USD, '[USD] TO MAX', MAX_ETH_USD, '[USD]'
        if (TACTIC_USE_CORRIDOR == 1):
            print '  TACTIC : USE CORRIDOR UP', MIN_CORRIDOR, 'TO', MAX_CORRIDOR, f_string.get_str_currency(SECOND_CURRENCY)
        #if (TACTIC_FIX_PRICE == 1):
           # print '|  TACTIC 5: FIX PRICE MIN', MIN_FIX, 'AND MAX', MAX_FIX, f_string.get_str_currency(SECOND_CURRENCY)

        #print '-----------------------------------------------------------------------------'
    except:
       print   "Error: print_tactic"

def print_pair():
    try:
        pair_nr=g.pair_instance.get_pair_nr()
        price24=g.pair_instance.get_price24()
        bid_ask=g.pair_instance.get_bid_ask()

        fist_curr=f_currency.get_first_currency(pair_nr)
        second_curr=f_currency.get_second_currency(pair_nr)


        print '                  CURRENT PRICE FROM API', f_string.get_str_currency(fist_curr),
        print '/', f_string.get_str_currency(second_curr),'                          '
        print '-----------------------------------------------------------------------------'
        print '  Price within the last 24    avg', '{:>7}'.format(round(price24[AVG_NR], DECIMAL_PART[second_curr])),
        print '  min',                               '{:>7}'.format(round(price24[MIN_NR], DECIMAL_PART[second_curr])),
        print '  max',                               '{:>7}'.format(round(price24[MAX_NR], DECIMAL_PART[second_curr]))
        print '  Last price Buy/Sell         avg', '{:>7}'.format(round(bid_ask[AVG_BID_ASK_NR], DECIMAL_PART[second_curr])),
        print '  bid',                                '{:>7}'.format(round(bid_ask[BID_NR], DECIMAL_PART[second_curr])),
        print '  ask',                                '{:>7}'.format(round(bid_ask[ASK_NR], DECIMAL_PART[second_curr]))
        print '-----------------------------------------------------------------------------'
    except:
        print "Error: print_pair"

def print_all_free_currency():
    try:
       #print 'print_all_free_currency'
       free_currency = g.pair_instance.free_currency
       #print
       print '> free_currency [BTC]=', '{:>7}'.format(round(free_currency[BTC], DECIMAL_PART[BTC])),
       print '  MIN_TO_TRADE[BTC]=', '{:>7}'.format(MIN_TO_TRADE[BTC])
       print '> free_currency [ETH]=', '{:>7}'.format(round(free_currency[ETH], DECIMAL_PART[ETH])),
       print '  MIN_TO_TRADE[ETH]=', '{:>7}'.format(MIN_TO_TRADE[ETH])
       print '> free_currency [USD]=', '{:>7}'.format(round(free_currency[USD], DECIMAL_PART[USD])),
       print '  MIN_TO_TRADE[USD]=', '{:>7}'.format(MIN_TO_TRADE[USD])
       print '> free_currency [RUB]=', '{:>7}'.format(round(free_currency[RUB], DECIMAL_PART[RUB])),
       print '  MIN_TO_TRADE[RUB]=', '{:>7}'.format(MIN_TO_TRADE[RUB])
       print
    except:
        print 'Error: print_all_free_currency'

def print_zone():
    bid_ask_price = g.pair_instance.get_bid_ask()
    last_preis = bid_ask_price[AVG_BID_ASK_NR]
    price24 = g.pair_instance.get_price24()
    low = price24[MIN_NR]
    high = price24[MAX_NR]
    avg = price24[AVG_NR]
    zone = f_currency.get_zone(last_preis, avg, low, high)
    pair_nr = g.pair_instance.get_pair_nr()
    fist_curr=f_currency.get_first_currency(pair_nr)
    second_curr=f_currency.get_second_currency(pair_nr)
    print '    _________________________'
    if (zone == 5):
        print '    |xxxxxxxxxx zone 5 xxxxxxxxx|'
    else:
        print '    |       zone 5          |'
    print 'high|-----------------------|-', round(high, DECIMAL_PART[second_curr])
    if (zone == 4):
        print '    |xxxxxxx Zone 4 xxxxxxxx|'
    else:
        print '    |       zone 4          |'
    print '    |-----------------------|-', round(high - (avg - low) * 0.5, DECIMAL_PART[second_curr])
    if (zone == 3):
        print '    |xxxxxx zone 3 xxxxxxxxx|'
    else:
        print '    |       zone 3          |'
    print 'avg-|-----------------------|-', round(avg, DECIMAL_PART[second_curr])
    if (zone == 2):
        print '    |xxxxxx zone 2 xxxxxxxxx|'
    else:
        print '    |       zone 2          |'
    print '    |-----------------------|-', round(low + (avg - low) * 0.5, DECIMAL_PART[second_curr])
    if (zone == 1):
        print '    |xxxxxx zone 1 xxxxxxxxx|'
    else:
        print '    |       zone 1          |'
    print 'low-|-----------------------|-', round(low, DECIMAL_PART[second_curr])
    if (zone == 0):
        print '    |xxxxxxx zone 0 xxxxxxxx|'
    else:
        print '    |       zone 0          |'
    print '    |_______________________|'

def print_exception(exception_name):
    print '>', time.strftime("%d.%m.%Y %H:%M:%S"), 'Error: ',  exception_name
    time.sleep(5)


def print_my_order(list):
    #print '-----------------------------------------------------------------------------'
    #print '                  OPENED ORDERS                                              '
    #print '-----------------------------------------------------------------------------'
    i = 0
    for order in list:
        print '  id:', order.id,
        print order.status,
        print '[',   order.pair_trade,
        print ']',   order.type_trade,
        print 'amount:', str(order.amount),
        print 'price:',  str(order.rate_trade)
    i += 1

def print_my_order_id(list):
    #print '-----------------------------------------------------------------------------'
    #print '                  OPENED ORDERS                                              '
    #print '-----------------------------------------------------------------------------'

    for id in list:
        print '  id:',  id
