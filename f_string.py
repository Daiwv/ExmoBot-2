# -*- coding: utf-8 -*-
import time
from g import *

from ted import *
import f_currency
import f_trade
import f_tactic
import f_print
import _file


def get_str_pairs_nr(nr):
    str = 'None'
    if (nr == 0):
        str = 'BTC/USD'
    elif (nr == 1):
        str = 'ETH/USD'
    elif (nr == 2):
        str = 'BTC/RUB'
    elif (nr == 3):
        str = 'ETH/RUB'
    elif (nr == 4):
        str = 'ETH/BTC'
    elif (nr == 5):
        str = 'USD/RUB'
    return str

def get_str_currency(nr):
    str_currency = ''
    if (nr == BTC):
        str_currency = 'BTC'
    elif (nr == ETH):
        str_currency = 'ETH'
    elif (nr == USD):
        str_currency = 'USD'
    elif (nr == RUB):
        str_currency = 'RUB'
    return str_currency



def write_str_trade(avg_bid_ask, first_currency, id, min_currency, pair_nr, price, second_currency, type_trade):
    str_second_curruncy = get_str_currency(second_currency)
    if (type_trade == 'buy'):
       quantity = round((0.999999 * min_currency / price), 6)
       sign = ' - '
    else:
        quantity = round((0.999999 * min_currency), 6)
        sign = ' + '

    my_trading_history = ' {:>10}'.format(get_str_pairs_nr(pair_nr)) \
                         + ' {:>15}'.format(str(id)) \
                         + '{:>7}'.format(type_trade) \
                         + '{:>10}'.format(str(round(price, DECIMAL_PART[second_currency]))) \
                         + '{:>4}'.format(str_second_curruncy) \
                         + ' {:>10}'.format(str(quantity)) \
                         + ' {:>20}'.format('(calculated: last price ' \
                                            + str(round(avg_bid_ask, DECIMAL_PART[first_currency])) + ' ' \
                                            + str_second_curruncy
                                            + sign + str(round((abs(avg_bid_ask - price) / avg_bid_ask) * 100, 1)) \
                                            + ' %) ')
    print '>', my_trading_history
    _file.write_to_file('my_open_order', my_trading_history)






