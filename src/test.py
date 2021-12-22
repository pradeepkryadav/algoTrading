from Utils import *
from KotakBrokerAPI import *
import json

#price=Utils.getLTPFromNSE(instrumentName='BANKNIFTY',strike=34900,optionType='CE')
#price =Utils.getInstrument()
#print(price)

#broker= KotakBrokerAPI()
#print(broker.getLTP(22821))
#print(broker.getCurrentInstrumentDetails(22821))

#data='{"instrumentToken": 22821, "lastPrice": 162.0500, "instrumentName": "BANKNIFTY"}'
#data="{'instrumentToken': '22821', 'lastPrice': '162.0500', 'instrumentName': 'BANKNIFTY'}"
data="{'success': [{'instrumentToken': '21272', 'lastPrice': '34984.7500', 'instrumentName': 'BANKNIFTY'}]}"
print(Utils.getJsonValue(data))
data_=json.loads(str(data.replace("{'success': [","").replace("]}","")).replace("'", '"'))
print(data_)
print("*******1")
#print(eval(data))
data1=str(data).replace("'", '"')
print("*******2")
print(data1)
#print(data['lastPrice'])
data2=json.loads(data1)
print("*******3",data2)
data3=json.loads(str(data2['success']).replace("'", '"'))
print("*******4",data3)
#for key in data3:
 #   print(key, ":", data3[key])
print("*******5",data3[0]['lastPrice'])
print("*******5",data_['lastPrice'])
data3=data2['success']
#print(json.loads(data3))
#data3=(json.JSONEncoder(data))
print(data2)
#data1=pd.json_normalize(data)
#print(data1)
#print(data1['lastPrice'])
#ltp=data["lastPrice"]

#print(ltp)
instrumentDetailsDF=Utils.getIntrumentsDataFrame()


#instrumentDF='instrumentDF', instrumentName='BANKNIFTY', segment='FO', instrumentType='OI',strike_price='', optionType='CE',
#.iloc[0]
instrumentDetails=Utils.getInstrumentInfo(instrumentDetailsDF,'BANKNIFTY', 'FO', 'OI', 34900, 'CE','23DEC21')
#price =Utils.getInstrument(instrumentDetails)['lastPrice']
print("instrumentDetails : token ID ",instrumentDetails)
token=Utils.getInstrument(instrumentDetailsDF,'BANKNIFTY')
print("instrumentDetails : token ID ",token)
#print(instrumentDetails['instrumentToken'])

#url='https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_19_12_2021.txt'
#fileName='TradeApiInstruments_FNO_19_12_2021.txt'
#print(Utils.getInstrumentDetailsFile(fileName))
