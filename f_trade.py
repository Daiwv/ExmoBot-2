# -*- coding: utf-8 -*-
import time
import g
import f_print
import f_currency
import f_string
from ted import *
import _ExmoAPI
from _CLASS import Order
import _file

def start_trade():
    try:
      pair_nr, first_currency, second_currency = f_currency.get_current_currency()
      free_currency = g.pair_instance.get_free_currency()

      print '>', time.strftime("%d.%m.%Y %H:%M:%S"), #, 'start Trade', get_str_pairs_nr(pair_nr)

      if (free_currency[second_currency] >= MIN_TO_TRADE[second_currency]):
              type_trade = 'buy'
              print ' start buy',  f_string.get_str_pairs_nr(pair_nr)
              buy_currency(type_trade)

      if (free_currency[first_currency] >= MIN_TO_TRADE[first_currency]):
              type_trade = 'sell'
              print ' start sell', f_string.get_str_pairs_nr(pair_nr)
              sell_currency(type_trade)

      print ' start', type_trade
      #start_sell_buy(type_trade)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)


def start_sell_buy(type_trade):
    try:
       pair_nr, first_currency, second_currency = f_currency.get_current_currency()

       if (type_trade=='sell'):
           currency = first_currency
       else: # 'buy'
           currency = second_currency

       free_currency = g.pair_instance.get_free_currency()
       aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
       pair = PAIR_STRING[pair_nr]

       price_to_trade = {}
       price_to_trade = g.pair_instance.get_price_to_trade()
       price_to_trade[0] = g.pair_instance.get_min_price_to_sell()

       if (TACTIC_USE_ORDER_BOOK == 1):
            price_to_trade = add_ask_and_bid(pair_nr, price_to_trade)

       if (TACTIC_USE_FIX_PRICE == 1):
            price_to_trade = add_fix_prices(pair_nr, price_to_trade)

       len_price = len(price_to_trade)

       if (free_currency[currency] >=  MIN_TO_TRADE[currency]):
           for i in range(100):
               if (i >= len_price):
                   i = i - len_price

               if (price_to_trade[i]>=price_to_trade[0]):
                   price = f_currency.check_aAsk(aAsk, price_to_trade[i], currency)

                   min_currency = f_currency.check_free_min(free_currency[currency] , MIN_TO_TRADE[currency])

                   if (type_trade=='sell'):
                       quantity = min_currency

                   else: # buy
                       quantity = 0.999999 * min_currency / price

                   sell_buy(avg_bid_ask, min_currency, pair, price)

                   free_currency = f_currency.refresh_and_get_free_currency()
                   if (free_currency[currency] < MIN_TO_TRADE[currency]):
                       break

       print '> sale-order added successfully'
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return



def sell_currency(type_trade):
    try:
       pair_nr, first_currency, second_currency = f_currency.get_current_currency()
       free_currency = g.pair_instance.get_free_currency()
       aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
       pair = PAIR_STRING[pair_nr]

       price_to_trade = {}
       price_to_trade = g.pair_instance.get_price_to_trade()
       price_to_trade[0] = g.pair_instance.get_min_price_to_sell()

       if (TACTIC_USE_ORDER_BOOK == 1):
            price_to_trade=add_ask_and_bid(pair_nr, price_to_trade)

       if (TACTIC_USE_FIX_PRICE == 1):
            price_to_trade = add_fix_prices(pair_nr, price_to_trade)

       len_price = len(price_to_trade)

       if (free_currency[first_currency] >=  MIN_TO_TRADE[first_currency]):
           for i in range(100):
               if (i >= len_price):
                   i = i - len_price

               if (price_to_trade[i]>=price_to_trade[0]):
                   price = f_currency.check_aAsk(aAsk, price_to_trade[i], first_currency)
                   #
                   min_currency = f_currency.check_free_min(free_currency[first_currency] , MIN_TO_TRADE[first_currency])
                   sell(avg_bid_ask, min_currency, pair, price)
                   #
                   free_currency = f_currency.refresh_and_get_free_currency()
                   if (free_currency[first_currency] < MIN_TO_TRADE[first_currency]):
                       break

       print '> sale-order added successfully'
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return


def sell(avg_bid_ask,  min_currency, pair, price):
    try:
       type_trade = 'sell'
       pair_nr, first_currency, second_currency = f_currency.get_current_currency()
       params = {"pair": pair.upper(), 'quantity': min_currency, 'price': price, 'type': type_trade}
       id = _ExmoAPI.trade(g.exmoAPI_instance, params)

       list_open_new = _ExmoAPI.get_my_orders_id (g.exmoAPI_instance )
       diff_list = list(set(g.list_open_old) - set(list_open_new))

       f_print.print_my_order_id(diff_list)
       g.list_open_old = list_open_new

       _ExmoAPI.get_trading_hystory(g.exmoAPI_instance, diff_list)
       f_string.write_str_trade(avg_bid_ask, first_currency, id, min_currency, pair_nr, price, second_currency, type_trade)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)


def buy_currency(type_trade):
    try:
        pair_nr, first_currency, second_currency = f_currency.get_current_currency()
        free_currency = g.pair_instance.get_free_currency()
        aBid, aAsk, avg_bid_ask = f_currency.get_bid_and_ask()
        pair = PAIR_STRING[pair_nr]

        price_to_trade={}
        price_to_trade = g.pair_instance.get_price_to_trade()
        price_to_trade[0] = g.pair_instance.get_max_price_to_buy()

        if (TACTIC_USE_ORDER_BOOK == 1):
            price_to_trade = add_ask_and_bid(pair_nr, price_to_trade)

        if (TACTIC_USE_FIX_PRICE == 1):
            price_to_trade = add_fix_prices(pair_nr, price_to_trade)

        len_price = len(price_to_trade)
        if (free_currency[second_currency] >= MIN_TO_TRADE[second_currency]):
            for i in range(100):
                if (i >= len_price):
                    i = i - len_price
                if (price_to_trade[i] <= price_to_trade[0]):
                    price = f_currency.check_aBid(aBid, price_to_trade[i], second_currency)
                    min_currency = f_currency.check_free_min(free_currency[second_currency], MIN_TO_TRADE[second_currency])
                    buy(avg_bid_ask,  min_currency, pair, price)
                    free_currency = f_currency.refresh_and_get_free_currency()
                    if (free_currency[second_currency] < MIN_TO_TRADE[second_currency]):
                        break
        print '> buy-order added successfully'
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return 0


def buy(avg_bid_ask,  min_currency, pair, price):
    try:
       type_trade = 'buy'
       pair_nr, first_currency, second_currency = f_currency.get_current_currency()
       params = {"pair": pair.upper(), 'quantity': 0.999999 * min_currency / price, 'price': price,
                 'type': type_trade}
       id = _ExmoAPI.trade(g.exmoAPI_instance, params)

       list_open_new = _ExmoAPI.get_my_orders_id (g.exmoAPI_instance )
       diff_list = list(set(g.list_open_old) - set(list_open_new))
       f_print.print_my_order_id(diff_list)
       g.list_open_old = list_open_new

       _ExmoAPI.get_trading_hystory(g.exmoAPI_instance, diff_list)

       f_string.write_str_trade(avg_bid_ask, first_currency, id, min_currency, pair_nr, price, second_currency, type_trade)

    except:
        f_print.print_exception(sys._getframe().f_code.co_name)


def get_vBids(am_lim):
    pairs_nr = g.pair_instance.get_pair_nr()
    pairs_url = PAIR_STRING[pairs_nr]
    depth = _ExmoAPI.get_depth(g.exmoAPI_instance, g.pair_instance)
    vBids = round(_ExmoAPI.find_rate(depth, pairs_url, 'bids', am_lim, pairs_nr), 4)
    return vBids


def get_vAsks(am_lim):
    pairs_nr = g.pair_instance.get_pair_nr()
    pairs_url = PAIR_STRING[pairs_nr]
    depth = _ExmoAPI.get_depth(g.exmoAPI_instance, g.pair_instance)
    vAsks = round(_ExmoAPI.find_rate(depth, pairs_url, 'asks', am_lim, pairs_nr), 4)
    return vAsks

def get_max_and_min( pair_currency):
    try:
       depth = _ExmoAPI.get_depth(g.exmoAPI_instance, pair_currency)
       pairs_nr = pair_currency.get_pair_nr()
       pairs_url = PAIR_STRING[pairs_nr]
       pair = PAIR_STRING[pairs_nr]#.upper()
       typ = 'asks'
       rate = depth[pair][typ][0][0]
       aAsks[pairs_nr] = depth[pair][typ][0][0]
       typ = 'bids'
       rate = depth[pair][typ][0][0]
       aBids[pairs_nr] = depth[pair][typ][0][0]
       min = (aAsks[pairs_nr] + aBids[pairs_nr])*0.5
       max = (aAsks[pairs_nr] + aBids[pairs_nr])*0.5
       counter = 0
       for orders in depth[pair][typ]:
           rate = orders[0]
           print rate
           if (rate > max):
               max = rate
           if (rate < min ):
               min=rate
       print min, max
       return min, max
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)


def add_ask_and_bid(pair_nr, price_to_trade):
    try:
       if (f_currency.get_first_currency(pair_nr) == BTC):
           lim_quantity = BTC_MAX_ASK_QUANTITY
       elif (f_currency.get_first_currency(pair_nr) == ETH):
           lim_quantity = ETH_MAX_ASK_QUANTITY
       else:
           lim_quantity = am_lim
       bid_price = get_vBids(lim_quantity)
       ask_price = get_vAsks(lim_quantity)
       price_to_trade[len(price_to_trade)] = bid_price
       price_to_trade[len(price_to_trade)] = ask_price
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return price_to_trade


def add_fix_prices(pair_nr, price_to_trade):
    try:
       if (f_currency.get_first_currency(pair_nr) == BTC) and (f_currency.get_second_currency(pair_nr) == USD):
           price_to_trade[len(price_to_trade)] = BTC_USD_FIX_1
           price_to_trade[len(price_to_trade)] = BTC_USD_FIX_2
       elif (f_currency.get_first_currency(pair_nr) == BTC) and (f_currency.get_second_currency(pair_nr) == RUB):
           price_to_trade[len(price_to_trade)] = BTC_RUB_FIX_1
           price_to_trade[len(price_to_trade)] = BTC_RUB_FIX_2
       elif (f_currency.get_first_currency(pair_nr) == ETH) and (f_currency.get_second_currency(pair_nr) == USD):
           price_to_trade[len(price_to_trade)] = ETH_USD_FIX_1
           price_to_trade[len(price_to_trade)] = ETH_USD_FIX_2
       elif (f_currency.get_first_currency(pair_nr) == ETH) and (f_currency.get_second_currency(pair_nr) == RUB):
           price_to_trade[len(price_to_trade)] = ETH_RUB_FIX_1
           price_to_trade[len(price_to_trade)] = ETH_RUB_FIX_2
       elif(f_currency.get_first_currency(pair_nr) == USD) and (f_currency.get_second_currency(pair_nr) == RUB):
           price_to_trade[len(price_to_trade)] = USD_RUB_FIX_1
           price_to_trade[len(price_to_trade)] = USD_RUB_FIX_2
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return price_to_trade

