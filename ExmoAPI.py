# -*- coding: utf-8 -*-
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
            print('Error while parsing response:', response)
            raise sys.exit()



def get_status(instance, pairs_nr):
    global nonce_last
    global currency_A_Free
    global min_currency_A
    global currency_B_Free
    global min_currency_B

    global btcFree
    global usdFree
    global ethFree
    global rubFree

    global btcTotal
    global usdTotal
    global ethTotal
    global rubTotal

    try:
        a = instance.api_query('user_info')
        # print a
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

        btcReserved = z['return']['res']['btc']
        usdReserved = z['return']['res']['usd']
        ethReserved = z['return']['res']['eth']
        rubReserved = z['return']['res']['rub']

        btcTotal = btcFree + btcReserved
        usdTotal = usdFree + usdReserved
        ethTotal = ethFree + ethReserved
        rubTotal = rubFree + rubReserved

        # print 'btcTotal =', round(btcTotal,6)
        # print 'usdTotal =', round (usdTotal,2)
        # print 'ethTotal =', round(ethTotal,6)
        # print 'rubTotal =', round (rubTotal,2)

        if (pairs_nr == nBTC_USD or pairs_nr == nBTC_RUB):
            currency_A_Free = btcFree
            min_currency_A = am_min_BTC
            # print 'BTC/',
        elif (pairs_nr == nETH_USD or pairs_nr == nETH_RUB):
            currency_A_Free = ethFree
            min_currency_A = am_min_ETH
            # print 'ETC/',
        if (pairs_nr == nBTC_USD or pairs_nr == nETH_USD):
            currency_B_Free = usdFree
            min_currency_B = am_min_USD
            # print 'USD'
        elif (pairs_nr == nBTC_RUB or pairs_nr == nETH_RUB):
            currency_B_Free = rubFree
            min_currency_B = am_min_RUB
            # print 'RUB'

        if (pairs_nr == nETH_BTC):
            currency_A_Free = ethFree
            min_currency_A = am_min_ETH
            currency_B_Free = btcFree
            min_currency_B = am_min_BTC
            # print 'ETH/BTC'

        # print 'currency_B_Free ', currency_B_Free
        # print 'min_currency_B', min_currency_B
        # print 'currency_A_Free ', currency_A_Free
        # print 'min_currency_A', min_currency_A

        # print 'btcReserved =', round (btcReserved,4)
        # print 'usdReserved =', round (usdReserved,4)
        # print 'ethReserved =', round (ethReserved,4)

    except:
        print 'Fehler get_status',
        time.sleep(2)
        reset_con()
        return 0

    return z


