import json
import math
import uuid
import time
import logging
import calendar
from datetime import datetime, timedelta
from src.Config import getHolidays
from pynse import *

nse = Nse()


class Utils:
    dateFormat = "%Y-%m-%d"
    timeFormat = "%H:%M:%S"
    dateTimeFormat = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def roundOff(price):  # Round off to 2 decimal places
        return round(price, 2)

    @staticmethod
    def roundToNSEPrice(price):
        x = round(price, 2) * 20
        y = math.ceil(x)
        return y / 20

    @staticmethod
    def isMarketOpen():
        if Utils.isTodayHoliday():
            return False
        now = datetime.now()
        marketStartTime = Utils.getMarketStartTime()
        marketEndTime = Utils.getMarketEndTime()
        return now >= marketStartTime and now <= marketEndTime

    @staticmethod
    def isMarketClosedForTheDay():
        # This method returns true if the current time is > marketEndTime
        # Please note this will not return true if current time is < marketStartTime on a trading day
        if Utils.isTodayHoliday():
            return True
        now = datetime.now()
        marketEndTime = Utils.getMarketEndTime()
        return now > marketEndTime

    @staticmethod
    def waitTillMarketOpens(context):
        nowEpoch = Utils.getEpoch(datetime.now())
        marketStartTimeEpoch = Utils.getEpoch(Utils.getMarketStartTime())
        waitSeconds = marketStartTimeEpoch - nowEpoch
        if waitSeconds > 0:
            logging.info("%s: Waiting for %d seconds till market opens...", context, waitSeconds)
            time.sleep(waitSeconds)

    @staticmethod
    def getEpoch(datetimeObj=None):
        # This method converts given datetimeObj to epoch seconds
        if datetimeObj == None:
            datetimeObj = datetime.now()
        epochSeconds = datetime.timestamp(datetimeObj)
        return int(epochSeconds)  # converting double to long

    @staticmethod
    def getMarketStartTime(dateTimeObj=None):
        return Utils.getTimeOfDay(9, 15, 0, dateTimeObj)

    @staticmethod
    def getMarketEndTime(dateTimeObj=None):
        return Utils.getTimeOfDay(15, 30, 0, dateTimeObj)

    @staticmethod
    def getTimeOfDay(hours, minutes, seconds, dateTimeObj=None):
        if dateTimeObj == None:
            dateTimeObj = datetime.now()
        dateTimeObj = dateTimeObj.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
        return dateTimeObj

    @staticmethod
    def getTimeOfToDay(hours, minutes, seconds):
        return Utils.getTimeOfDay(hours, minutes, seconds, datetime.now())

    @staticmethod
    def getTodayDateStr():
        return Utils.convertToDateStr(datetime.now())

    @staticmethod
    def convertToDateStr(datetimeObj):
        return datetimeObj.strftime(Utils.dateFormat)

    @staticmethod
    def isHoliday(datetimeObj):
        dayOfWeek = calendar.day_name[datetimeObj.weekday()]
        if dayOfWeek == 'Saturday' or dayOfWeek == 'Sunday':
            return True

        dateStr = Utils.convertToDateStr(datetimeObj)
        holidays = getHolidays()
        if (dateStr in holidays):
            return True
        else:
            return False

    @staticmethod
    def isTodayHoliday():
        return Utils.isHoliday(datetime.now())

    @staticmethod
    def generateTradeID():
        return str(uuid.uuid4())

    @staticmethod
    def prepareMonthlyExpiryFuturesSymbol(inputSymbol):
        expiryDateTime = Utils.getMonthlyExpiryDayDate()
        expiryDateMarketEndTime = Utils.getMarketEndTime(expiryDateTime)
        now = datetime.now()
        if now > expiryDateMarketEndTime:
            # increasing today date by 20 days to get some day in next month passing to getMonthlyExpiryDayDate()
            expiryDateTime = Utils.getMonthlyExpiryDayDate(now + timedelta(days=20))
        year2Digits = str(expiryDateTime.year)[2:]
        monthShort = calendar.month_name[expiryDateTime.month].upper()[0:3]
        futureSymbol = inputSymbol + year2Digits + monthShort + 'FUT'
        logging.info('prepareMonthlyExpiryFuturesSymbol[%s] = %s', inputSymbol, futureSymbol)
        return futureSymbol

    @staticmethod
    def prepareWeeklyOptionsSymbol(inputSymbol, strike, optionType, numWeeksPlus=0):
        expiryDateTime = Utils.getWeeklyExpiryDayDate()
        todayMarketStartTime = Utils.getMarketStartTime()
        expiryDayMarketEndTime = Utils.getMarketEndTime(expiryDateTime)
        if numWeeksPlus > 0:
            expiryDateTime = expiryDateTime + timedelta(days=numWeeksPlus * 7)
            expiryDateTime = Utils.getWeeklyExpiryDayDate(expiryDateTime)
        if todayMarketStartTime > expiryDayMarketEndTime:
            expiryDateTime = expiryDateTime + timedelta(days=6)
            expiryDateTime = Utils.getWeeklyExpiryDayDate(expiryDateTime)
        # Check if monthly and weekly expiry same
        expiryDateTimeMonthly = Utils.getMonthlyExpiryDayDate()
        weekAndMonthExpriySame = False
        if expiryDateTime == expiryDateTimeMonthly:
            weekAndMonthExpriySame = True
            logging.info('Weekly and Monthly expiry is same for %s', expiryDateTime)
        year2Digits = str(expiryDateTime.year)[2:]
        optionSymbol = None
        if weekAndMonthExpriySame == True:
            monthShort = calendar.month_name[expiryDateTime.month].upper()[0:3]
            optionSymbol = inputSymbol + str(year2Digits) + monthShort + str(strike) + optionType.upper()
        else:
            m = expiryDateTime.month
            d = expiryDateTime.day
            mStr = str(m)
            if m == 10:
                mStr = "O"
            elif m == 11:
                mStr = "N"
            elif m == 12:
                mStr = "D"
            dStr = ("0" + str(d)) if d < 10 else str(d)
            optionSymbol = inputSymbol + str(year2Digits) + mStr + dStr + str(strike) + optionType.upper()
        logging.info('prepareWeeklyOptionsSymbol[%s, %d, %s, %d] = %s', inputSymbol, strike, optionType, numWeeksPlus,
                     optionSymbol)
        return optionSymbol

    @staticmethod
    def getMonthlyExpiryDayDate(datetimeObj=None):
        if datetimeObj == None:
            datetimeObj = datetime.now()
        year = datetimeObj.year
        month = datetimeObj.month
        lastDay = calendar.monthrange(year, month)[1]  # 2nd entry is the last day of the month
        datetimeExpiryDay = datetime(year, month, lastDay)
        while calendar.day_name[datetimeExpiryDay.weekday()] != 'Thursday':
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)
        while Utils.isHoliday(datetimeExpiryDay) == True:
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)

        datetimeExpiryDay = Utils.getTimeOfDay(0, 0, 0, datetimeExpiryDay)
        return datetimeExpiryDay

    @staticmethod
    def getWeeklyExpiryDayDate(dateTimeObj=None):
        if dateTimeObj == None:
            dateTimeObj = datetime.now()
        daysToAdd = 0
        if dateTimeObj.weekday() >= 3:
            daysToAdd = -1 * (dateTimeObj.weekday() - 3)
        else:
            daysToAdd = 3 - dateTimeObj.weekday()
        datetimeExpiryDay = dateTimeObj + timedelta(days=daysToAdd)
        while Utils.isHoliday(datetimeExpiryDay) == True:
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)

        datetimeExpiryDay = Utils.getTimeOfDay(0, 0, 0, datetimeExpiryDay)
        return datetimeExpiryDay

    @staticmethod
    def isTodayWeeklyExpiryDay():
        expiryDate = Utils.getWeeklyExpiryDayDate()
        todayDate = Utils.getTimeOfToDay(0, 0, 0)
        if expiryDate == todayDate:
            return True
        return False

    @staticmethod
    def isTodayOneDayBeforeWeeklyExpiryDay():
        expiryDate = Utils.getWeeklyExpiryDayDate()
        todayDate = Utils.getTimeOfToDay(0, 0, 0)
        if expiryDate - timedelta(days=1) == todayDate:
            return True
        return False

    @staticmethod
    def getNearestStrikePrice(price, nearestMultiple=50):
        inputPrice = int(price)
        remainder = int(inputPrice % nearestMultiple)
        if remainder < int(nearestMultiple / 2):
            return inputPrice - remainder
        else:
            return inputPrice + (nearestMultiple - remainder)

    def trailStopLoss(self, instrumentName='BANKNIFTY', strike='34000', optionType='PE'):
        # Get the current price of both strike
        # if current price and SL having difference more than 5%
        # update the order for new stop loss
        ltp = nse.get_quote(instrumentName, segment=Segment.OPT, optionType=optionType, strike=strike)['closePrice']
        # ltpCE = nse.get_quote(instrumentName, segment=Segment.OPT, optionType=OptionType.CE, strike=strike)['closePrice']
        return ltp

    def getLTPFromNSE(instrumentName='BANKNIFTY', strike='34000', optionType='PE'):
        # Get the current price of both strike
        # if current price and SL having difference more than 5%
        # update the order for new stop loss
        if optionType == 'PE':
            optionType = OptionType.PE
        else:
            optionType = OptionType.CE
        ltp = nse.get_quote(instrumentName, segment=Segment.OPT, optionType=optionType, strike=strike)['closePrice']
        print(ltp)
        # ltpCE = nse.get_quote(instrumentName, segment=Segment.OPT, optionType=OptionType.CE, strike=strike)['closePrice']
        return ltp

    def getOptionChainNSE(self):
        nse.get

    @staticmethod
    def downloadfile(url):
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        return local_filename

    def getInstrumentDetailsFile(fileName):
        if os.path.isfile(fileName):
            print('Utils : file already downloaded ' + fileName)
            return fileName
        else:
            url = 'https://preferred.kotaksecurities.com/security/production/' + fileName
            Utils.downloadfile(url)
            print('Utils : file downloading with url : ' + url)
            return fileName

    def getInstrumentInfo(instrumentDF='instrumentDF', instrumentName='BANKNIFTY', segment='FO', instrumentType='OI',
                          strike_price='', optionType='CE',
                          expiry_day='23DEC21'):
        df = instrumentDF
        # print('******* getInstrumentInfo')
        # print(df)
        # strike_price = strike_price*100
        instrumentInfo = df[
            (df['segment'] == segment) & (df['expiry'] == expiry_day) & (df['instrumentType'] == instrumentType) & (
                    df['instrumentName'] == instrumentName) & (df['strike'] == strike_price) & (
                    df['optionType'] == optionType)].iloc[0]
        #.iloc[0].iloc[0]

        instrumentInfo1 = df[
            (df['segment'] == 'FO') & (df['instrumentType'] == 'OI') & (
                    df['instrumentName'] == 'BANKNIFTY') & (df['strike'] == '34900') & (
                    df['optionType'] == 'PE') & (df['expiry'] == '23DEC21')]
        print("instrumentName : ", instrumentName, " , instrumentType : ", instrumentType, " , instrumentToken : ",
              instrumentInfo)
        return instrumentInfo

    ## 21272|BANKNIFTY||37246.3|30DEC21|0|0.050000|25|FI|FO|NSE||1|71319|XX
    def getInstrument(instrumentDF, instrumentName='BANKNIFTY', segment='FO', instrumentType='FI',
                      expiry_day='30DEC21'):
        df = instrumentDF
        instrumentInfo = df[
            (df['segment'] == segment) & (df['expiry'] == expiry_day) & (df['instrumentType'] == instrumentType) & (
                    df['instrumentName'] == instrumentName)].iloc[0].iloc[0]
        print("instrumentName : ", instrumentName, " ,instrumentType : ", instrumentType, " ,instrumentToken : ",
              instrumentInfo)
        return int(instrumentInfo)

    @staticmethod
    def getIntrumentsDataFrame():
        import pandas as pd
        from datetime import datetime, date
        filename = 'TradeApiInstruments_FNO_' + datetime.today().strftime("%d_%m_%Y") + ".txt"
        filename = Utils.getInstrumentDetailsFile(filename)
        token_df = pd.read_csv(filename, sep='|')
        token_df = token_df.astype({'strike': float})
        token_df = token_df.astype({'lastPrice': float})
        # token_df = token_df.astype({'instrumentToken': int})
        return token_df

    def getJsonValue(jsonObj, keyName='lastPrice'):
        data = json.loads(str(jsonObj.replace("{'success': [", "").replace("]}", "")).replace("'", '"'))
        return data[keyName]

    def getValueFromJson(jsonObj, keyName='lastPrice'):
        return jsonObj['success'][0][keyName]
