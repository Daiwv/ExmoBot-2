# -*- coding: utf-8 -*-
from ted import *

class Tactic():
    def __init__(self):
        self.tactic_1=TACTIC_USE_SECOND_PAIR
        self.second_pair=-1
        self.tactic_2=TACTIC_CHECK_MIN_MAX_BTC
        self.min_BTC=(float)(MIN_BTC_USD)
        self.max_BTC=(float)(MAX_BTC_USD)
        self.tactic_3=TACTIC_CHECK_MIN_MAX_ETH
        self.min_ETH=(float)(MIN_ETH_USD)
        self.max_ETH=(float)(MAX_ETH_USD)
        self.tactic_4=TACTIC_USE_CORRIDOR
        self.min_corridor = MIN_CORRIDOR
        self.max_corridor = MAX_CORRIDOR
        #self.tactic_5=TACTIC_FIX_PRICE
        #self.min_fix=MIN_FIX
        #self.max_fix=MAX_FIX
        self.tactic_rate=self.tactic_1 + self.tactic_2*10+self.tactic_3*100+self.tactic_4*1000#+self.tactic_5*10000
        #0 - no tactic
        #1 - TACTIC_USE_SECOND_PAIR
        #10 - TACTIC_CHECK_MIN_MAX_BTC
        #100 - TACTIC_CHECK_MIN_MAX_ETH
        #1000 - TACTIC_USE_CORRIDOR
        #10000 - TACTIC_FIX_PRICE

    def get_second_pair(self):
        return self.second_pair

    def get_tactic_rate(self):
        return self.tactic_rate

class Order:
    def __init__(self):
        self.status ='-'
        self.id=-1
        self.pair_trade='/'
        self.type_trade=''
        self.amount=0.0
        self.rate_trade=0.0

    def set_my_order(self, id, status, pair_trade, type_trade, amount, rate_trade):
        self.id = id
        self.status = status
        self.pair_trade = pair_trade
        self.type_trade = type_trade
        self.amount = amount
        self.rate_trade = rate_trade

    def get_my_order(self):
        return self

    def print_my_order(self):
        print 'id:', self.id,
        print 'status', self.status,
        print         self.pair_trade,
        print         self.type_trade,
        print 'amount:', str(self.amount),
        print 'price:',  str(self.rate_trade)

class Order_List:
    def __init__(self):
        self.list=[]

    def set_list(self, list):
        self.list = list

    def add_order (self, order):
        self.list.append(order)

    def get_list(self):
        return self.list

class TED:
    def set_decimal_part(self):
        dp_btc=DECIMAL_PART_BTC
        dp_eth=DECIMAL_PART_ETH
        dp_usd=DECIMAL_PART_USD
        dp_rub=DECIMAL_PART_RUB
        self.decimal_part=[dp_btc, dp_eth, dp_usd, dp_rub]

    def set_minvalue(self):
        minvalue_btc=(float)(MIN_BTC_TO_TRADE)
        minvalue_eth=(float)(MIN_ETH_TO_TRADE)
        minvalue_usd=(float)(MIN_USD_TO_TRADE)
        minvalue_rub=(float)(MIN_RUB_TO_TRADE)
        self.minvalue_to_trade=[minvalue_btc, minvalue_eth, minvalue_usd, minvalue_rub]

    def __init__(self, PAIR_NR):
        self.PAIR_NR=PAIR_NR
        self.set_decimal_part()
        self.set_minvalue()
        self.min_difference=MIN_DIFFERENCE

    def get_decimal_part(self):
         return self.decimal_part

    def get_minvalue(self):
         return self.minvalue_to_trade

    def get_min_difference(self):
        return self.min_difference

class Pair:
    def __init__(self, pair_nr):
        self.pair_nr = pair_nr
        self.avg_price24=-1
        self.min_price24=-1
        self.max_price24=-1
        self.price24=[self.avg_price24, self.min_price24, self.max_price24]
        self.free_currency_BTC = 0
        self.free_currency_ETH = 0
        self.free_currency_USD = 0
        self.free_currency_RUB = 0
        free_currency = [self.free_currency_BTC, self.free_currency_ETH, self.free_currency_USD, self.free_currency_RUB]
        self.free_currency = free_currency
        self.avg_bid_ask=0
        self.bid=0
        self.ask=0
        self.bid_ask=[self.avg_bid_ask, self.bid, self.ask]
        self.min_diff_sell_buy=self.avg_bid_ask*MIN_DIFFERENCE*0.01
        self.min_price_to_sell=self.avg_bid_ask + self.min_diff_sell_buy
        self.max_price_to_buy = self.avg_bid_ask - self.min_diff_sell_buy
        self.price_to_trade = {}

    def set_avg_bid_ask(self, bid_ask):
        self.avg_bid_ask=bid_ask[AVG_BID_ASK_NR]
        self.bid=bid_ask[BID_NR]
        self.ask=bid_ask[ASK_NR]
        self.bid_ask=[self.avg_bid_ask, self.bid, self.ask]
        self.min_diff_sell_buy = self.avg_bid_ask * MIN_DIFFERENCE * 0.01
        self.min_price_to_sell = self.avg_bid_ask + self.min_diff_sell_buy
        self.max_price_to_buy = self.avg_bid_ask - self.min_diff_sell_buy
        #self.calculate_price_to_trade()

    def set_price24(self, p24):
        self.avg_price24 = p24[AVG_NR]
        self.min_price24 = p24[MIN_NR]
        self.max_price24 = p24[MAX_NR]
        self.price24 = [self.avg_price24, self.min_price24, self.max_price24]
        #self.calculate_price_to_trade()

    def set_free_currency(self, f):
        self.free_currency_BTC = f[BTC]
        self.free_currency_ETH = f[ETH]
        self.free_currency_USD = f[USD]
        self.free_currency_RUB = f[RUB]
        free_currency = [self.free_currency_BTC, self.free_currency_ETH, self.free_currency_USD, self.free_currency_RUB]
        self.free_currency = free_currency

    def get_free_currency(self):
        return self.free_currency

    def get_pair_nr(self):
        return self.pair_nr

    def get_price24(self):
        return  self.price24

    def get_bid_ask(self):
        return self.bid_ask

    def get_price_to_trade(self):
        self.calculate_price_to_trade()
        return self.price_to_trade

    def get_min_deff_sell_buy(self):
        return self.min_diff_sell_buy

    def get_min_price_to_sell(self):
        return self.min_price_to_sell

    def get_max_price_to_buy(self):
        return self.max_price_to_buy

    def calculate_price_to_trade(self):
        avg_bid_ask = self.avg_bid_ask
        bid = self.bid
        ask = self.ask
        price24 = self.price24
        low = price24[MIN_NR]
        high = price24[MAX_NR]
        avg = price24[AVG_NR]
        diff_SB = MIN_DIFFERENCE * avg_bid_ask * 0.01
        price_to_trade = {}
        # ----------------------------------------------------------------------
        price_to_trade[0] =0
        price_to_trade[1] = low - diff_SB  #
        price_to_trade[2] = low  #
        price_to_trade[3] = low + diff_SB  #
        price_to_trade[4] = low + (avg - low) * 0.5
        price_to_trade[5] = avg - diff_SB  #
        price_to_trade[6] = avg  #
        price_to_trade[7] = avg + diff_SB  #
        price_to_trade[8] = high - (avg - low) * 0.5
        price_to_trade[9] = high - diff_SB  #
        price_to_trade[10] = high  #
        price_to_trade[11] = high + diff_SB  #
        # ----------------------------------------------------------------------
        self.price_to_trade = price_to_trade

    def get_Pair(self):
        return self