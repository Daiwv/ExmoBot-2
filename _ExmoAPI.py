# -*- coding: utf-8 -*-
# Бот для Эксмо ETH&BTC
# Импорт библиотек
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
from contextlib import closing
import g # global
from _key import *
from _CLASS import *
from f_print import *
import _file

class ExmoAPI:
    def __init__(self, API_KEY, API_SECRET, API_URL='api.exmo.com', API_VERSION='v1'):
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET)

    def sha512(self, data):
        H = hmac.new(key=self.API_SECRET, digestmod=hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params={}):
        params['nonce'] = int(round(time.time() * 1000))
        params = urllib.urlencode(params)

        sign = self.sha512(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign
        }

        conn = httplib.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method, params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            f_print.print_exception(sys._getframe().f_code.co_name)
            raise sys.exit()

def read_exmoAPI():
    try:
       list = []
       pairs_nr=g.pair_instance.get_pair_nr()
       pair_currency=get_status(g.exmoAPI_instance, g.pair_instance)

       get_statistics (g.exmoAPI_instance, g.pair_instance)
       get_depth(g.exmoAPI_instance, g.pair_instance)

       list=get_my_orders(g.exmoAPI_instance)
       #f_print.print_my_order(list)
       #get_trading_hystory(g.exmoAPI_instance)

    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

# Установака соединения

# глубина стакана
# В z{} записывается весь массив данных по Asks/Bids (200 ордеров)
# Вычисляется середина стакана для актуальной пары и записывается в глобальный массив avg_AB[pairs_nr]

def get_depth(instance, pair_currency):
    #global min_price
    #global max_price
    try:
       pairs_nr = pair_currency.get_pair_nr()
       pairs_url = PAIR_STRING[pairs_nr]
       pair = PAIR_STRING[pairs_nr].upper()
       #print 'NUMBER_OF_RECORDS', NUMBER_OF_RECORDS
       count = NUMBER_OF_RECORDS
       if (count < 100):
           count = 100
       limit =  '&limit='+ str(count)
       #print limit
       y = instance.api_query('order_book/?pair=' + pairs_url.upper() + limit)   #200')
       #print y
       z = {}
       for p in y:
           p2 = p.lower()
           ask_quantity = y[p]['ask_quantity']
           bid_quantity = y[p]['bid_quantity']
           z[p2] = {'asks': [], 'bids': []}
           for q in y[p]['ask']:
               z[p2]['asks'].append([float(q[0]), float(q[1])])
           for q in y[p]['bid']:
               z[p2]['bids'].append([float(q[0]), float(q[1])])

       #avg_AB = round((z[pairs_url]['asks'][0][0] + z[pairs_url]['bids'][0][0]) * 0.5, 4)
       depth = z

       #min_price, max_price = get_max_and_min(count_min_max, depth, pairs_url, pairs_nr, instance, pair_currency)
       #print depth
       # запросить стакан c учетом объемов (заглушки)
       #vAsks = get_vAsk(depth, pairs_nr, pairs_url, am_lim)
       #vBids = get_vBids(depth, pairs_nr, pairs_url, am_lim)
       vAsks = round(find_rate(depth, pairs_url, 'asks', am_lim, pairs_nr), 4)
       vBids = round(find_rate(depth, pairs_url, 'bids', am_lim, pairs_nr), 4)

       avg_AB = (vAsks + vBids) / 2

       bid_ask = [avg_AB, vBids, vAsks]
       pair_currency.set_avg_bid_ask(bid_ask)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return z

# Запись в глобальные переменные статистических данных за последние 24 часа, полученных с помощью API
def get_statistics(instance, pair_currency):
    try:
       pairs_nr = pair_currency.get_pair_nr()
       pairs_url = PAIR_STRING[pairs_nr]
       pair = PAIR_STRING[pairs_nr].upper()
       a = instance.api_query('ticker')
       # high - максимальная цена сделки за 24 часа
       # low - минимальная цена сделки за 24 часа
       # avg - средняя цена сделки за 24 часа
       # vol - объем всех сделок за 24 часа
       # vol_curr - сумма всех сделок за 24 часа
       # last_trade - цена последней сделки
       # buy_price - текущая максимальная цена покупки
       # sell_price - текущая минимальная цена продажи
       z = {}
       z[pair] = {}
       j = 0;
       while j < 9:
           z[pair][j] = {}
           j += 1
       i = 0;
       for m in a[pair]:
           p2 = m.lower

           z[pair][i] = float(a[pair][m])
           i += 1
       avg = z[pair][8]
       high = z[pair][0]
       low = z[pair][7]
       p = {}
       p =[(float)(avg), (float)(low), (float)(high)]
       pair_currency.set_price24(p)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return z

# Статус аккаунта. Определение свободной и зарезервированной валюты
# Актуальная валютная пара записывается в currency_A_Free, currency_B_Free
# TODO две переменных для одного значения... потом подправить
def get_status(instance, pair_currency):
    pairs_nr = pair_currency.get_pair_nr()
    try:
        a = instance.api_query('user_info')
        # print 'a', a
        z = {}
        z['return'] = {}
        z['return']['funds'] = {}
        z['return']['res'] = {}

        for m in a['balances']:
            p2 = m.lower()
            z['return']['funds'][p2] = float(a['balances'][m])

        for m in a['reserved']:
            p2 = m.lower()
            z['return']['res'][p2] = float(a['reserved'][m])

        btcFree = z['return']['funds']['btc']
        usdFree = z['return']['funds']['usd']
        ethFree = z['return']['funds']['eth']
        rubFree = z['return']['funds']['rub']

        currency_free = [ (float)(btcFree), (float)(ethFree), (float)(usdFree), (float)(rubFree)]
        pair_currency.set_free_currency (currency_free)
        return pair_currency

    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

    return pair_currency


def get_my_orders_id(instance):
    try:
        list = get_my_orders(instance)
        list_id = []

        for order in list:
            list_id.append(order.id)

    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return list_id



# Статус ордеров передаются в массив z={}
def get_my_orders(instance, ind_ak=0):
    #global order_list
    #order_list = Order_List()
    list = []
    try:
        a = instance.api_query('user_open_orders')  # , params, headers)
        z = {}
        z['success'] = 0
        z['error'] = 'all ok'
        z['return'] = {}
        for p in a:
            for j in range(len(a[p])):
                z['success'] = 1
                oid = a[p][j]["order_id"]
                pair_trade = a[p][j]["pair"].lower()
                type_trade =  a[p][j]["type"]
                amount =float(a[p][j]["quantity"])
                rate_trade = float(a[p][j]["price"])
                z['return'][oid] = {"pair": pair_trade, "type": type_trade,
                                    "amount": amount, "rate": rate_trade}
                p3= z['return'][oid]

                order=Order()
                order.set_my_order(oid, 'open', pair_trade, type_trade, amount, rate_trade)
                #print print_my_order(order)
                list.append(order)
                #print list

        if z['success'] == 0:
            z['error'] = 'no orders'

    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
        return 0
    return list

# Отмена ордера. Не используется
def cancel_order(instance, ord, ind_ak=0):
    try:
        a = instance.api_query('order_cancel', ord)
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return a


# Массив с данными стакана (200 ордеров) обрабатывется для каждой пары
# В глобальные переменные Верхняя и Нижняя граница стаканов (продажа и покупка)
# записываются актульные значения
# В массив rate записываются значения границ стакана с учетом объемов (для определения заглушек)
def find_rate(depth, pair, typ, am_lim, pairs_nr):
    try:
      #print depth, pair, typ, am_lim, pairs_nr
      rate = depth[pair][typ][0][0]

      if typ == 'asks':
          aAsks[pairs_nr] = depth[pair][typ][0][0]
      if typ == 'bids':
          aBids[pairs_nr] = depth[pair][typ][0][0]
      am_sum = 0.0
      counter = 0
      #print aAsks
      for orders in depth[pair][typ]:
          #print orders
          am = orders[1]
          rate = orders[0]
          #am_sum += am
          am_sum = am
          counter += 1
          if am_sum >= am_lim:
              break
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return rate

def trade(instance, params, ind_ak=0):
    count = 0
    try:
        a = instance.api_query('order_create', params)
        #print '| order_id =', a['order_id'], params
        if a['error'] != '':
            print 'Trade: ', a['error']
        aa = a['order_id']
        return aa
    except:
        f_print.print_exception(sys._getframe().f_code.co_name)

def get_trading_hystory(instance, list_id):
    try:
        currency =''
        type_trade = '-'
        in_currency = '-'
        in_amount = '-'
        out_currency = '-'
        out_amount = '0'
        trades = '-'

        date_ex = '-'
        type = '-'
        pair = '-'
        order_id = '0'
        quantity = '0'
        price = '0'
        amount = '0'
        my_trading_history = '-'

        if not list_id:
            print "List is empty"
        else:
           for id in list_id:
               params = {"order_id": id}
               a = instance.api_query("order_trades", params)

               type_trade = a["type"]
               in_currency = a["in_currency"]
               in_amount = a["in_amount"]
               out_currency = a["out_currency"]
               out_amount = a["out_amount"]
               trades = a["trades"]

               for t in trades:
                  date_ex=t["date"]
                  type=t["type"]
                  pair=t["pair"]
                  order_id=t["order_id"]
                  quantity=t["quantity"]
                  price=t["price"]
                  amount=t["amount"]

                  if type=='sell':
                      currency = in_currency
                  else:
                      currency=out_currency

                  my_trading_history = ' {:>10}'.format(pair) \
                                  + ' {:>15}'.format(str(order_id)) \
                                  + '{:>6}'.format(type_trade) + ' ' \
                                  + '{:>10}'.format(str(quantity))\
                                  + '{:>4}'.format(currency) + ' ' \
                                  +'{:>10}'.format(amount)#\


                                 #+ ' h '


        print '>' , my_trading_history
        _file.write_to_file ('my_trading_history', (my_trading_history))


    except:
        f_print.print_exception(sys._getframe().f_code.co_name)
    return 0







#get_my_orders(ExmoAPI_instance)
#ord = '414864705'
#params = {"order_id":ord}
#cancel_order(ExmoAPI_instance, params)
