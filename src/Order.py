import logging

from src.Utils import Utils


class Order:

    def __init__(self, tradingSymbol=None):
        self.exchange = "NSE"
        self.orderID = ""  # OrderID
        self.instrumentName = "BANKNIFTY"
        self.instrumentToken = ""
        self.exchangeToken = ""
        self.instrumentType = 'OI'
        self.optionType = 'PE'
        self.orderType = 'SELL'
        self.strike = 0
        self.expiry = "23DEC21"
        self.initialPrice = 0
        self.initialIntrumentPrice = 0
        self.strategy = ""
        self.qty = 0  # Requested quantity
        self.filledQty = 0  # In case partial fill qty is not equal to filled quantity
        self.initialStopLoss = 0  # Initial stop loss
        self.stopLoss = 0  # This is the current stop loss. In case of trailing SL the current stopLoss and initialStopLoss will be different after some time
        self.target = 0  # Target price if applicable
        self.cmp = 0  # Last traded price
        self.pnl = 0

    def __str__(self):
        return "ID=" + str(self.orderID) + ", state=" + self.tradeState + ", symbol=" + self.tradingSymbol \
               + ", strategy=" + self.strategy \
               + ", instrumentToken=" + self.instrumentToken + ", reqEntry=" + str(self.initialIntrumentPrice) \
               + ", stopLoss=" + str(self.stopLoss) + ", target=" + str(self.target) \
               + ", profitLoss" + str(self.pnl)

    def updateOrderDetails(self, order, jsonObj):
        # parse json object and convert into Order Object
        #{'success': [{'wtoken': '146124', 'ltp': '178.0000', 'lv_net_chg': '0.902', 'lv_net_chg_perc': '0.3098',
        #              'open_price': '150.0000', 'closing_price': '84.8000', 'high_price': '222.0000',
        #              'low_price': '64.8500', 'average_trade_price': '119.6300', 'last_trade_qty': '25',
        #              'BD_last_traded_time': '22/12/2021 15:29:57', 'OI': '660750', 'BD_TTQ': '34042750',
        #              'market_exchange': 'NSE', 'stk_name': 'BANKNIFTY', 'display_segment': 'DERIVATIVE',
        #              'display_fno_eq': 'OPT'}]}
        if jsonObj is None:
            order.orderID = "New Order"
        return order

    def prepareOrder(instrumentInfo, order=None):
        # {'success': [{'wtoken': '21272', 'ltp': '35155.0000', 'lv_net_chg': '4.8235', 'lv_net_chg_perc': '0.0176',
        #             'open_price': '34849.7000', 'closing_price': '34676.9500', 'high_price': '35169.5000',
        #            'low_price': '34746.0000', 'average_trade_price': '34954.1400', 'last_trade_qty': '25',
        #           'BD_last_traded_time': '22/12/2021 15:29:57', 'OI': '2406700', 'BD_TTQ': '3312075',
        #          'market_exchange': 'NSE', 'stk_name': 'BANKNIFTY', 'display_segment': 'DERIVATIVE',
        #         'display_fno_eq': 'FUT'}]}
        if order == None:
            order = Order()
        print("Instrument Info : ", instrumentInfo)
        # instrumentToken|instrumentName|name|lastPrice|expiry|strike|tickSize|lotSize|instrumentType|segment|exchange|isin|multiplier|exchangeToken|optionType
        # 15380|BANKNIFTY||5339.65|16DEC21|31700|0.050000|25|OI|FO|NSE||1|43238|CE
        # 21272|BANKNIFTY||37246.3|30DEC21|0|0.050000|25|FI|FO|NSE||1|71319|XX
        order.instrumentToken = instrumentInfo['instrumentToken']
        order.instrumentName = instrumentInfo['instrumentName']
        order.cmp = instrumentInfo['lastPrice']
        order.instrumentType = instrumentInfo['instrumentType']
        order.exchangeToken = instrumentInfo['exchangeToken']
        order.optionType = instrumentInfo['optionType']
        order.strike = instrumentInfo['strike']
        order.expiry = instrumentInfo['expiry']
        order.initialPrice=instrumentInfo['lastPrice']
        return order

