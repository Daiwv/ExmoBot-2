# -*- coding: utf-8 -*-
import math
import httplib
import urllib
import urllib2
import json
import hashlib
import hmac
import time
import copy
import string
import random
import socket
import sys
from _CLASS import *
from _ExmoAPI import *
from _key import *
import _file
import g  # global
import ted
import f_main
import f_print
import f_string
import f_trade
import f_tactic
import f_currency


def main():
    try:
        g.exmoAPI_instance = ExmoAPI(MY_API_KEY, MY_API_SECRET)  # EXMO-API-Connection
    except:
        f_print.print_exception(sys._getframe().f_code.co_name + ' ExmoAPI()')

    try:
        # make pair-number from first and second currency (ted.py)
        pair_nr = f_currency.get_pairs_nr(FIRST_CURRENCY, SECOND_CURRENCY)
        f_main.ini(pair_nr)
        f_print.print_pair()
        f_print.print_tactic(pair_nr)
        # active_trade_pair = pair_nr
    except:
        f_print.print_exception(sys._getframe().f_code.co_name + 'ini() + print()')

    print '> Bot: I am ready . . .',

    while (True):
        pair_nr = f_currency.get_pairs_nr(FIRST_CURRENCY, SECOND_CURRENCY)
        f_main.ini(pair_nr)
        # my_func.__name__
        try:
            # active_trade_pair depending on the chosen tactics and depending on the free currency
            active_trade_pair = f_currency.get_active_trade_pair(pair_nr)
            if (active_trade_pair < 0):
                f_main.do_wait()
            else:
                try:
                   f_main.do_trade(active_trade_pair)
                except:
                    f_print.print_exception(sys._getframe().f_code.co_name + ' f_main.do_trade')
        except:
            f_print.print_exception(sys._getframe().f_code.co_name + ' while-loop')
            # raise sys.exit()
            # sys.exit("Exit")
            main()


main()
