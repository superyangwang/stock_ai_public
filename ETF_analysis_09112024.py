#Yang update 09/11/2024. commit on github and send to do auto run
# rename file: ETF_analysis_09112024
#
# conclusion
# 1. ETF based on 2010-2024-08-16 FJPNX 50K total investment: each time invest $1000: total investment: $10000
#       when price decrease 5%, buy 1000 worth shares.
#       when price increase 7%, sell 1000 worth shares.
#       not great investment, the best I can do it 6.9% return per year. not the best
# 2. ETF same with 1 FBGRX : each time invest $3000 - considered dividends and captialGain: total $40,000
#       when price decrease 2%, buy 3000 worth shares
#       when price increase 9%, sell 3000 worth shares
#       each year is about 16-17% profit --- Great
#
# 3. ETF WAINX india index: each time invest $2800 total investment : $30000, profit 12.59%
#       when price decrease 1% buy $2600 worth shares
#       when price increase 7% sell 2600 worth shares
#       results2:
#           buy @-0.003, sell 0.07, each time BUY $3000; SELL 6000. return  15.55%
# 4. FHKCX china index: each time invest $2400. total investment =$10000. annual profit =7.07%
#       when price decrease 8% buy $2400 worth shares
#       when price increase 8% sell $2400 worth shares
# 5. FXAIX fidelity 500 index. Fidelty return rate: 13.37%
#       buy 0.3% $3000 worth
#       sell 6%  $6000 worth
# 6.
# from winreg import HKEYType
# very bad calculation on Sep 27, 2024(Friday).Wrong cal for FBGRX and FJPNX
import seaborn
import platform
import pandas as pd
import datetime
import timeit
import pandas_datareader as web # works, but yahoofinancials apps sometimes did not work for 3.12 why??
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import rcParams
import seaborn as sb
from yahoofinancials import YahooFinancials # did not work for 3.12 or my github not sure why, yahoofinance is too slow
from yahooquery import Ticker
import numpy as np
from numpy.random import randn
from pandas import Series, DataFrame
import os
import yfinance as yf
from bs4 import BeautifulSoup
import time
import requests
import smtplib
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

rcParams['figure.figsize'] = 5, 4   #5inch wide, 4 tall
sb.set_style('whitegrid')

style.use('ggplot')
def authenticate():
    if password:
        print("Password retrieved successfully!")
        # Use the password in your authentication logic
    else:
        print("No password found!")

def textGoogle(text, password):
    email = "super.yangwoods@gmail.com"
    if platform.system() == "Windows":
        sms_gateway = os.getenv('sms_gateway')
        print("The system is Windows.")
    else:
        sms_gateway = os.getenv("SMSGATEWAY")
        print("The system is not Windows.")

    # The server we use to send emails in our case it will be gmail but every email provider has a different smtp
    # and port is also provided by the email provider.
    smtp = "smtp.gmail.com"
    port = 587
    # This will start our email server
    server = smtplib.SMTP(smtp, port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email, password)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = "stockprice trigger\n"
    # Make sure you also add new lines to your body
    body = text
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(email, sms_gateway, sms)

    # lastly quit the server
    server.quit()
def download_closed(holdings):
    # yahoo_financials_mutualfunds = YahooFinancials(holdings)
    # daily_mutualfund_prices = yahoo_financials_mutualfunds.get_historical_price_data(open, close, 'daily')
    close_price={}
    for ticket_1 in holdings:
        singleHolding=yf.Ticker(ticket_1)
        # print(ticket_1)
        # print(singleHolding)
        # print(singleHolding.info['currentPrice'])
        close_price[ticket_1]=singleHolding.info['previousClose']
        # print(ticket_1 + str(close_price[ticket_1]))
    return close_price

def download_yh(start, end, ticket):
    if isinstance(ticket, str):
        yahoo_financials_mutualfunds = yf.Ticker(ticket)
        # print("start" + start)

        # print("end:"+ end)
        daily_mutualfund_prices = yahoo_financials_mutualfunds.history(start=start, end=end,interval="5m")
        df = pd.DataFrame(daily_mutualfund_prices['Close'])
        # df.to_csv(ticket + '.csv')
    else:
        df = {}
        for ticket_1 in holdings:
            # temp=yf.download(ticket_1, start='2024-08-20', period='1d', interval="1m")
            temp = yf.download(ticket_1, start=start, period='1d', interval="1m")
            df[ticket_1] = pd.DataFrame(temp)
            # i=i+1
    return df
def etf_guess(ticket_ETF, holdings, holdingP, basePrice,change, adj):
    end = datetime.date.today().__str__()
    lastBusDay = datetime.datetime.today()
    shift = datetime.timedelta(max(1, (lastBusDay.weekday() + 6) % 7 - 3))
    lastBusDay = lastBusDay - shift
    start = lastBusDay.date().__str__()
    #
    # print("start:" + start )
    # print("end:"+ end)
    df = download_yh(start, end, ticket_ETF)  # ETF history close data
    df_close = download_closed(holdings)  # download one day closed data
    dict_holdings = download_yh(start, end, holdings)  # download 1min one day data

    i = 0
    changeP = 0
    for ticketName in holdings:
        price = dict_holdings[ticketName]['Close']
        if not price.empty:
            changeP = (price[-1] - df_close[ticketName]) * holdingP[i] / df_close[ticketName] + changeP
        i = i + 1
    predict_ETF = (changeP / sum(holdingP) + 1) * df['Close'][0]
    predict_ETF_adjust = (changeP / sum(holdingP) * adj + 1) * df['Close'][0]
    printStr='previous day ' + ticket_ETF + start + ' closed price =' + str(df['Close'][0]) +'\n'
    print('previous day ' + ticket_ETF + start + ' closed price =' + str(df['Close'][0]))

    print('today' + ticket_ETF + 'price guess=' + str(predict_ETF))
    printStr = printStr + 'today' + ticket_ETF + 'price guess=' + str(predict_ETF) + '\n'
    print('today' + ticket_ETF + 'price guess(adjust)=' + str(predict_ETF_adjust))
    printStr = printStr + 'today' + ticket_ETF + 'price guess(adjust)=' + str(predict_ETF_adjust) + '\n'
    print(' guess increase= ' + str(changeP * 100) + '%')
    printStr = printStr + ' guess increase= ' + str(changeP * 100) + '%' +'\n'
    printStr = printStr +"trigger price =[" + str(basePrice*(change[0]+1)) + ',' + str(basePrice*(change[1]+1)) + '] \n'
    if predict_ETF_adjust < basePrice*(change[0]+1):  # base price is not change, unless, we buy or sell
        print('-------------------------')
        print('price today drop over' + str(change[0]*100) +'%, buy ' + ticket_ETF)
        printStr = printStr + 'price drop over' + str(change[0]*100) +'%, buy ' + ticket_ETF +'\n'
        control = 'buy'
    elif predict_ETF_adjust > basePrice*(change[1]+1):
        print('-------------------------')
        print('price today increase over' + str(change[1]*100) +'%, buy  ' + ticket_ETF)
        printStr=printStr+'price increase over' + str(change[1]*100) +'% ' + ticket_ETF +'\n'
        control = 'sell'
    else:
        print('-------------------------')
        print('  doing nothing')
        control = 'nothing'
        printStr=printStr+'doing nothing'+'\n'
    # print('================' + ticket_ETF + 'done===============')
    return printStr, control

def GetETFinfo(ticket):
    tt = Ticker(ticket)
    cc=tt.fund_sector_weightings
    dd=tt.fund_holding_info[ticket]['holdings']
    name =[]
    holdingPercent=[]
    for ticket in dd:
        # print(ticket)
        name.append(ticket['symbol'])
        holdingPercent.append(ticket['holdingPercent'])
    return name, holdingPercent
        ##==========do it tomorrow.================
    # with open('Names.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(cars)

if __name__=="__main__":
    # load csv from file

    password = os.getenv("YANGWOODSEMAIL_PASSWORD")
    # message=os.getenv("")
    authenticate()
    printStr=" "
    RollOverIRAtotal=20000 # as 09-10,2024 it did not make much money, return rate is low, so reduce the investment


    ticket_ETF = 'WAINX'
    holdings, holdingP = GetETFinfo(ticket_ETF)
    Ticket = pd.read_csv('ETF_' + ticket_ETF + '.csv', index_col=0)
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    STR2, action=etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.003, 0.07], 1)
    if action == 'buy':
        print(STR2)
        printStr=printStr+STR2 +' buy $3000 worth ETF \n'
    elif action == 'sell':
        print(' sell $6000')
        print(STR2)
        printStr = printStr + STR2 + ' sell $6000 \n'
    else:
        print(STR2)
        print(' nonthing done ')
        printStr = printStr + STR2

    if action != 'nothing':

        totalCost=Ticket['total'].iloc[-1]
        print('current share% =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        printStr = printStr + 'current share% =' + str(totalCost / RollOverIRAtotal * 100) + '%' + '\n'
        if totalCost / RollOverIRAtotal > 0.049:
            printStr = printStr+'be careful close to 5% target, recalculate the investment' +'\n'
            print('be careful close to 5% target, recalculate the investment')
        else:
            print('not reach 2% target investment yet')
            printStr = printStr +'not reach 5% target investment yet' +'\n'
        # print('======WAINX Indian ETF is done======')
        printStr = printStr + '===WAINX Indian is done=====' + '\n'
        printStr = printStr + '\n'

    #=======================================================================

    ticket_ETF = 'FBGRX'

    Ticket = pd.read_csv('ETF_FBGRX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1] # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    str3, action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.003, 0.05], 1)

    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy 5000 worth FBGRX ETF \n'
    elif action == 'sell':
        print(' sell $6000')
        print(str3)
        printStr = printStr + str3 + ' sell 5000 worth FBGRX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    if action != 'nothing':
        ROTHIRA=28943 # as 09-10-2024, when it is full buy from Rollover IRA account
        print('current share % =' + str(totalCost / ROTHIRA * 100) + '%')
        if totalCost / ROTHIRA > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 100% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' +'\n'
        print('====FBGRX blue chip ETF is done======')
        printStr = printStr + '===FBGRX blue chip is done===' + '\n'
    printStr = printStr + '\n'



    # =======================================================================
    ticket_ETF = 'FSPCX'
    Ticket = pd.read_csv('ETF_FSPCX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    str3 , action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.003, 0.05], 1)

    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy 5000 worth FSPCX ETF \n'
    elif action == 'sell':
        print(' sell $6000')
        print(str3)
        printStr = printStr + str3 + ' sell 5000 worth FSPCX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    if action != 'nothing':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 100% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' + '\n'
        print('====FSPCX is done======')
        printStr = printStr + '===FSPCX FIDELITY INSURANCE is done===' + '\n'
        # textGoogle(printStr, password)
    printStr = printStr + '\n'

    #=======================================================================
    ticket_ETF = 'FHKCX'
    Ticket = pd.read_csv('ETF_FHKCX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1] # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    print(holdings)
    i=0
    for component in holdings:
        if component == '00939':
            print("correct")
            holdings[i] ='0939.HK'
        if component == "02899":
            holdings[i]='2899.HK'
        i = i + 1

    str3, action  = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.02, 0.09], 1)
    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy $2400 worth FHKCX ETF \n'
    elif action == 'sell':
        print(' sell 2400')
        print(str3)
        printStr = printStr + str3 + ' sell $2400 worth FHKCX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    if action != 'nothing':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        totalCost = Ticket['total'].iloc[-1]
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 2% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' +'\n'
        print('=====FHKCX blue chip ETF is done======')
        printStr = printStr + '===FHKCX blue chip is done===' + '\n'
        # textGoogle(printStr,password)
    printStr = printStr + '\n'


    # =======================================================================
    ticket_ETF = 'FNILX'
    Ticket = pd.read_csv('ETF_FNILX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    # print(holdings)
    str3, action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.005, 0.06], 1)
    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy $1000 worth FNILX ETF \n'
    elif action == 'sell':
        print(' sell $500')
        print(str3)
        printStr = printStr + str3 + ' sell $2400 worth FNILX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    if action != 'nothing':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 2% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' + '\n'
        print('=====FNILX blue chip ETF is done======')
        printStr = printStr + '===FNILX blue chip is done===' + '\n'
    printStr = printStr + '\n'

    # =======================================================================
    ticket_ETF = 'FJPNX'
    Ticket = pd.read_csv('ETF_FJPNX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    print(holdings)

    str3, action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.02, 0.09], 1)
    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy $2000 worth FJPNX ETF \n'
    elif action == 'sell':
        print(' sell $500')
        print(str3)
        printStr = printStr + str3 + ' sell $2000 worth FJPNX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    if action != 'nothing':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 2% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' + '\n'
        print('=====FJPNX ETF is done======')
        printStr = printStr + '===FJPNX is done===' + '\n'
        # textGoogle(printStr, password)
    printStr = printStr + '\n'

    # =======================================================================
    ticket_ETF = 'FXAIX'
    Ticket = pd.read_csv('ETF_FXAIX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    print(holdings)

    str3, action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.003, 0.06], 1)
    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy $3000 worth FXAIX ETF \n'
    elif action == 'sell':
        print(' sell $6000')
        print(str3)
        printStr = printStr + str3 + ' sell $6000 worth FXAIX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3
    # print("buy 3000 worth FXAIX ETF; sell $6000 worth FXAIX")
    # printStr = printStr + str3 + 'buy 3000 worth FXAIX ETF; sell $6000 worth FXAIX \n'
    if action != 'nothng':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 2% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' + '\n'
        print('=====FXAIX ETF is done======')
        printStr = printStr + '===FXAIX is done===' + '\n'
    printStr = printStr + '\n'

    # =======================================================================
    ticket_ETF = 'FMSDX'
    Ticket = pd.read_csv('ETF_FMSDX.csv', index_col=0)
    totalCost = Ticket['total'].iloc[-1]
    baseCost = Ticket['price'].iloc[-1]  # basecost is the last purchase or sell point
    holdings, holdingP = GetETFinfo(ticket_ETF)
    print(holdings)

    str3 , action = etf_guess(ticket_ETF, holdings, holdingP, baseCost, [-0.005, 0.06], 1)
    if action == 'buy':
        print(str3)
        printStr=printStr+str3 +' buy $3000 worth FMSDX ETF \n'
    elif action == 'sell':
        print(' sell $3000')
        print(str3)
        printStr = printStr + str3 + ' sell $6000 worth FMSDX \n'
    else:
        print(str3)
        print(' nonthing done ')
        printStr = printStr + str3

    # print("buy 3000 worth FMSDX ETF; sell $3000 worth FMSDX")
    # printStr = printStr + str3 + 'buy 3000 worth FMSDX ETF; sell $3000 worth FMSDX\n'
    if action != 'nothing':
        print('current share % =' + str(totalCost / RollOverIRAtotal * 100) + '%')
        if totalCost / RollOverIRAtotal > 1:
            print('be careful close to 100% target, recalculate the investment')
            printStr = printStr + 'be careful close to 100% target, recalculate the investment' + '\n'
        else:
            print('not reach 2% target investment yet')
            printStr = printStr + 'not reach 5% target investment yet' + '\n'
        print('=====FMSDX ETF is done======')
        printStr = printStr + '===FMSDX is done===' + '\n'
    printStr = printStr + '\n'
    textGoogle(printStr, password)
        # printStr = printStr + '\n'