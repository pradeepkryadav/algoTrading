from ks_api_client import ks_api
#import openapi_client
from  datetime import datetime , timedelta
import math

#Instrument token of the scrip to be traded.
#Instrument tokens can be found at the following urls (NOTE: Please replace DD_MM_YYYY with the latest date for updated instrument tokens, for example 27_05_2021 will give tokens for 27 may):
#Equity: https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_DD_MM_YYYY.txt
#Derivatives: https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_DD_MM_YYYY.txt
# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
# For using sandbox environment use host as https://sbx.kotaksecurities.com/apim
#client = ks_api.KSTradeApi(access_token="", userid="",consumer_key="", ip="127.0.0.1", app_id="", host="https://sbx.kotaksecurities.com/apim")

userData= json.load(open('config/userDetails.json'))
    #userid=data['userid']
client = ks_api.KSTradeApi(userData['access_token'], userData['userid'],userData['consumer_key'], userData['ip'], userData['app_id'],userData['host'])
    # For using sandbox environment use host as https://sbx.kotaksecurities.com/apim
    #client = ks_api.KSTradeApi(access_token="", userid="",consumer_key="", ip="127.0.0.1", app_id="", host="https://sbx.kotaksecurities.com/apim")
# Get session for user
client.login(userData['password'])
# Generated session token
client.session_2fa(userData['access_code'])

# Get Report Orders
#client.order_report()

# Get Report Orders for order id
#client.order_report(order_id="")

# Get Margin required
order_info = [
    {"instrument_token": 727, "quantity": 1, "price": 1300, "amount": 0, "trigger_price": 1190},
    {"instrument_token": 1374, "quantity": 1, "price": 1200, "amount": 0, "trigger_price": 1150}
]
#client.margin_required(transaction_type="BUY", order_info=order_info)

# Get Positions
#client.positions(position_type="TODAYS")
#client.ins
#while True :
# Get Quote details
  # if (datetime.now().second % 20 == 0) :
banknifty_fut_price = client.quote(instrument_token=21272)
banknifty_fut_price

       # client.history(50056)
        #client.history()
        # Get Quote details
       #print(client.quote(instrument_token=49947))


# Terminate user's Session
#client.logout()

import math
banknifty_price = banknifty_fut_price['success'][0]['ltp']
#price=int(float(banknifty_price))
#price
base=100
ATMStrike = base*round(float(banknifty_price)/100)
ATMStrike

import requests
import pandas as pd
from datetime import datetime,date
url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_13_12_2021.txt'
d = requests.get(url)
text = d.iter_lines()
token_df = pd.read_csv(url, sep='|')
#token_df = pd.read_csv('/Users/I320253/PycharmProjects/pythonProject/tradedInstruments.txt', sep='|')
#token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
#token_df = pd.DataFrame.from_dict(d)
#token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})
#instrumentToken|instrumentName|name|lastPrice|expiry|strike|tickSize|lotSize|instrumentType|segment|exchange|isin|multiplier|exchangeToken|optionType
#15380|BANKNIFTY||5339.65|16DEC21|31700|0.050000|25|OI|FO|NSE||1|43238|CE
#token_df_ = token_df[(token_df['instrumentName'] == 'BANKNIFTY') & (token_df['instrumentType'] == 'OI') & (token_df['expiry']=='16DEC21') ]
print(token_df)

#def getTokenInfo_ (instrumentName, segment ='FO',instrumenttype='OI',strike_price = '',optionType = 'CE',expiry_day = None):
#    return token_df[(token_df['instrumentName'] == 'BANKNIFTY') & (token_df['instrumentType'] == 'OI') & (token_df['expiry']==date(2021,12,16)) & ]

def getTokenInfo(instrumentName, segment='FO', instrumentType='OI', strike_price='', optionType='CE', expiry_day=None):
    df = token_df
    # strike_price = strike_price*100
    return df[(df['segment'] == segment) & (df['expiry'] == expiry_day) & (df['instrumentType'] == instrumentType) & (
                df['instrumentName'] == instrumentName) & (df['strike'] == strike_price) & (
                          df['optionType'] == optionType)]
expiry_day = date(2021,12,16)
expiry_day='16DEC21'
instrumentName = 'BANKNIFTY'
ce_strike_info = getTokenInfo(instrumentName,'FO','OI',ATMStrike,'CE',expiry_day).iloc[0]
ce_strike_info
pe_strike_info = getTokenInfo(instrumentName,'FO','OI',ATMStrike,'PE',expiry_day).iloc[0]
pe_strike_info

def place_order(instrumentToken,transaction_type,quantity):
    try:
    # Place a Order
       # client.place_order(order_type = order_type, instrument_token = token,transaction_type = buy_sell, quantity = qty, price = 0,disclosed_quantity = 0, trigger_price = 0,validity = "GFD", variety = "REGULAR", tag = "string")
       # client.place_order(order_type,token,buy_sell, qty,0,0,0,'REGULAR','GFD','REGULAR')
        client.place_order(order_type = "N", instrument_token = instrumentToken,  \
                   transaction_type = transaction_type, quantity = quantity, price = 0,\
                   disclosed_quantity = 0, trigger_price = 0,\
                   validity = "GFD", variety = "REGULAR", tag = "string")
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)

#place order for CE
noOfLots=1
instrumentToken = int(ce_strike_info['instrumentToken'])
place_order(int(ce_strike_info['instrumentToken']),'SELL',int(ce_strike_info['lotSize'])*noOfLots)
#place order for PE
place_order(int(pe_strike_info['instrumentToken']),'SELL',int(pe_strike_info['lotSize'])*noOfLots)
instrumentToken
