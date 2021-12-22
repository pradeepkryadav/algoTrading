import Order
from ks_api_client import ks_api
from time import sleep
import urllib.parse as urlparse
import pandas as pd
import requests
import re
import datetime
import numpy as np
from bs4 import BeautifulSoup
import pandas_ta as ta
# from utills import *
from pynse import *
from KotakBrokerAPI import *

nse = Nse()
broker = KotakBrokerAPI()
instrumentDetails = Utils.getIntrumentsDataFrame();
stoplossPct = 30
stoplossPctDelta = 5
symbol = 'BANKNIFTY'
base = 100
tradeList=[]
while True:
    weekday_today = datetime.now().weekday()
    print(weekday_today)
    if (weekday_today != 5) & (weekday_today != 6):
        print(weekday_today)
        sleep(5)
        print(symbol)
        expiry_day = '23DEC21'
        instrumentName = 'BANKNIFTY'
        instrumentToken=Utils.getInstrument(instrumentDetails,instrumentName=instrumentName)
        # while datetime.datetime.now().time() < datetime.time(9,24,55):
        #    sleep(1)
        #quote = nse.get_quote(instrumentName, segment=Segment.FUT)['lastPrice']
        #quote = Utils.getInstrument(instrumentDetails)['lastPrice']
        print(instrumentToken)
        quote=broker.getQuoteDetail(instrumentToken)
        #{'success': [{'instrumentToken': '21272', 'lastPrice': '34984.7500', 'instrumentName': 'BANKNIFTY'}]}
        print("quote  ",quote)
        futPrice=Utils.getValueFromJson(quote,'ltp')
        ATMStrike = base * round(float(futPrice)/ base)
        print(datetime.now())
        print(ATMStrike)
        # expiry_day = datetime.date(2021, 12, 16)
        ce_strike_info = Utils.getInstrumentInfo(instrumentDetails, instrumentName, 'FO', 'OI', ATMStrike - 100, 'CE',
                                    expiry_day)
        print("ce_strike_info  ",ce_strike_info)
        pe_strike_info =Utils.getInstrumentInfo(instrumentDetails, instrumentName, 'FO', 'OI', ATMStrike - 100, 'PE',
                                    expiry_day)
        print("pe_strike_info : ",pe_strike_info)
        #ce_strike_info=broker.getQuoteDetail(instrumentTokenCE)
        #pe_strike_info=broker.getQuoteDetail(instrumentTokenPE)
        orderCE = Order.prepareOrder(ce_strike_info)
        orderPE = Order.prepareOrder(pe_strike_info)
        #brokerResponse=broker.placeOrder(orderPE)
        #orderPE=Order.updateOrderDetails(orderPE,brokerResponse)
        #brokerResponse=broker.placeOrder(orderCE)
        #orderCE = Order.updateOrderDetails(orderCE, brokerResponse)
        tradeList.append(orderCE)
        tradeList.append(orderPE)

        while True:
            sleep(10)
            for order in tradeList:
                #trailStoploss(tradeList[i])
                initialPrice = order.initialPrice
                stopLoss = order.stopLoss
                #currentPrice = Utils.getLTPFromNSE(order.tradingSymbol, order.strike, order.optionType)
                currentPrice = broker.getLTP(int(order.instrumentToken))
                newStoploss = currentPrice + (currentPrice * float(stoplossPct)/100)
                stoplossDeta = currentPrice * float(stoplossPctDelta)/100
                if stopLoss >= newStoploss + stoplossDeta:
                        # modify the order , call modify order API
                    order.stopLoss = newStoploss
                       # broker.modifyOrder(order)
                    print('*** Stoploss updated  **** original price :',order.initialPrice," current Price : ",currentPrice)
                else:
                    print('*** Stoploss update not required **** :',order.initialPrice," current Price : ",currentPrice," strike : ",order.instrumentName,order.strike,order.optionType)
                # Get current price of PE and CE
                # check initial stoploss
                #def updateOrderAndTrailSL():
                print(broker.getTodaysPositions())
