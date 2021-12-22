import json
from ks_api_client import ks_api
from Order import *

from Utils import *


class KotakBrokerAPI:

    def __init__(self):
        super(KotakBrokerAPI, self).__init__()
        self.client = self.brokerLogin
       # self.instrumentDF = self.getInstrumentList

    @property
    def brokerLogin(self):
        userData = json.load(open('../config/userDetails.json'))
        # userid=data['userid']
        client = ks_api.KSTradeApi(userData['access_token'], userData['userid'], userData['consumer_key'],
                                   userData['ip'],
                                   userData['app_id'], userData['host'])
        # For using sandbox environment use host as https://sbx.kotaksecurities.com/apim
        # client = ks_api.KSTradeApi(access_token="", userid="",consumer_key="", ip="127.0.0.1", app_id="", host="https://sbx.kotaksecurities.com/apim")
        # Get session for user
        client.login(userData['password'])
        # Generated session token
        client.session_2fa(userData['access_code'])
        return client

    def place_order(self, instrumentToken, transaction_type, quantity, stoploss):
        try:
            # Place a Order
            # https://github.com/osparamatrix/ks-orderapi-python/blob/master/docs/OrderApi.md#place_order
            # client.place_order(order_type = order_type, instrument_token = token,transaction_type = buy_sell, quantity = qty, price = 0,disclosed_quantity = 0, trigger_price = 0,validity = "GFD", variety = "REGULAR", tag = "string")
            # client.place_order(order_type,token,buy_sell, qty,0,0,0,'REGULAR','GFD','REGULAR')
            self.client.place_order(order_type="N", instrument_token=instrumentToken,
                                    transaction_type=transaction_type, quantity=quantity, price=0,
                                    disclosed_quantity=0, trigger_price=stoploss,
                                    validity="GFD", variety="REGULAR", tag="string")
        except Exception as e:
            print("Exception when calling OrderApi->place_order: %s\n" % e)

    def placeOrder(self, order):
        # Modify an existing order
        if order is None:
            order = Order()
        instrumentToken = order.instrumentToken
        stoploss = order.stopLoss
        quantity = order.qty
        transaction_type = order.orderType
        return self.place_order(instrumentToken, transaction_type, quantity, stoploss)

    def modify_order(self, order_id, quantity, stoploass):
        try:
            # Modify an existing order
            return self.client.modify_order(order_id=order_id, quantity=quantity, price=0,
                                            disclosed_quantity=0, trigger_price=stoploass, validity="GFD")

        except Exception as e:
            print("Exception when calling OrderApi->modify_order: %s\n" % e)

    def modifyOrder(self, order):
        try:
            # Modify an existing order
            if order is None:
                order = Order()
            order_id = order.orderID
            stoploss = order.stopLoss
            quantity = order.qty
            self.client.modify_order(order_id=order_id, quantity=quantity, price=0,
                                     disclosed_quantity=0, trigger_price=stoploss, validity="GFD")
        except Exception as e:
            print("Exception when calling OrderApi->modify_order: %s\n" % e)

    def cancel_order(self, order_id):
        try:
            # Cancel an order
            self.client.cancel_order(order_id=order_id)
        except Exception as e:
            print("Exception when calling OrderApi->cancel_order: %s\n" % e)

    @property
    def getInstrumentList(self):
        import requests
        import pandas as pd
        from datetime import datetime, date
        filename = 'TradeApiInstruments_FNO_' + datetime.today().strftime("%d_%m_%Y") + ".txt"
        # print(fileDateName)
        # url = 'https://preferred.kotaksecurities.com/security/production/' + filename
        # url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_13_12_2021.txt'
        filename = Utils.getInstrumentDetailsFile(filename)
        token_df = pd.read_csv(filename, sep='|')
        token_df = token_df.astype({'strike': float})
        # instrumentToken|instrumentName|name|lastPrice|expiry|strike|tickSize|lotSize|instrumentType|segment|exchange|isin|multiplier|exchangeToken|optionType
        # 15380|BANKNIFTY||5339.65|16DEC21|31700|0.050000|25|OI|FO|NSE||1|43238|CE
        # 21272|BANKNIFTY||37246.3|30DEC21|0|0.050000|25|FI|FO|NSE||1|71319|XX
        # token_df_ = token_df[(token_df['instrumentName'] == 'BANKNIFTY') & (token_df['instrumentType'] == 'OI') & (token_df['expiry']=='16DEC21') ]
        # print(token_df)
        # def getTokenInfo_ (instrumentName, segment ='FO',instrumenttype='OI',strike_price = '',optionType = 'CE',expiry_day = None):
        # return token_df[(token_df['instrumentName'] == 'BANKNIFTY') & (token_df['instrumentType'] == 'OI') & (token_df['expiry']==date(2021,12,16)) & ]
        return token_df

    def getInstrumentInfo(self, instrumentName, segment='FO', instrumentType='OI', strike_price='', optionType='CE',
                          expiry_day='23DEC21'):
        df = self.instrumentDF
        print('******* getInstrumentInfo')
        # print(df)
        # strike_price = strike_price*100
        instrumentInfo = df[
            (df['segment'] == segment) & (df['expiry'] == expiry_day) & (df['instrumentType'] == instrumentType) & (
                    df['instrumentName'] == instrumentName) & (df['strike'] == strike_price) & (
                    df['optionType'] == optionType)]
        print('getInstrumentInfo' + instrumentInfo)
        return instrumentInfo

    ## 21272|BANKNIFTY||37246.3|30DEC21|0|0.050000|25|FI|FO|NSE||1|71319|XX
    def getInstrument(self, instrumentName='BANKNIFTY', segment='FO', instrumentType='FI', strike_price='0',
                      optionType='XX',
                      expiry_day='30DEC21'):
        df = self.instrumentDF
        instrumentInfo = df[
            (df['segment'] == segment) & (df['expiry'] == expiry_day) & (df['instrumentType'] == instrumentType) & (
                    df['instrumentName'] == instrumentName)]
        print('getInstrument' + instrumentInfo)
        return instrumentInfo

    def getLTP(self, instrument_token):
        # get instrumentToken from list
        # call API for getting LTP price
        currentLTP = (self.client.quote(instrument_token, quote_type='LTP'))
        #print("inside getLTP ",currentLTP['success'][0]['lastPrice'])
#        currentLTP = Utils.getJsonValue(currentLTP)
        currentLTP = currentLTP['success'][0]['lastPrice']
        # currentLTP
        return float(currentLTP)

    def getQuoteDetail(self, instrument_token):
        # get instrumentToken from list
        # call API for getting LTP price
        quoteDetail = (self.client.quote(instrument_token))
        print(quoteDetail)
        return quoteDetail

    def getCurrentInstrumentDetails(self, instrument_token):
        # get instrumentToken from list
        # call API for getting LTP price
        quote_details = (self.client.quote(instrument_token))
        # currentLTP
        return quote_details;
    def getTodaysPositions(self):
        try:
            # Get's position by position_type.
            self.client.positions(position_type="TODAYS")
        except Exception as e:
            print("Exception when calling PositionsApi->positions: %s\n" % e)