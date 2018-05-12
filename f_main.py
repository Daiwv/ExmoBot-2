# -*- coding: utf-8 -*-
import time
import sys
from _CLASS import *
import _ExmoAPI #import read_exmoAPI
from _key import *
import _file
from ted import *
import f_string
import f_trade
import f_tactic
import f_currency
import f_print
import g #global


def do_trade(active_trade_pair ):
    try:
       ini(active_trade_pair)  # refresh for new pair
       #f_print.print_info()
       f_trade.start_trade()
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

def ini(pair_nr):
    try:
       g.pair_instance = Pair(pair_nr)  # make objekt from class Pair (price-data)
       _ExmoAPI.read_exmoAPI()  # read API-Daten EXMO, push in pair_currency
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

def do_wait():
    try:
       print '.',
       time.sleep(2)
       f_currency.refresh_and_get_free_currency()
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)