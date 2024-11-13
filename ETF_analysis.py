# conclusion:
# 1. ETF based on 2010-2024-08-16 FJPNX 50K total investment: each time invest $3500: total investment: $10000
#      results1: based on buy and sell the same amount
#           when price decrease 5%, buy $3500 worth shares.
#           when price increase 7%, sell $3500 worth shares.
#           not great investment, the best I can do it 6.9% return per year. not the best
#      results 2: based on buy and sell are different
#           buy when 2% decrease, buy 2000
#           sell when 9% increase, sell 2000
#           profit is 9.7% annual, while fidelity is 7.05%, Gross Expense ratio=0.87%
# 2. ETF same with 1 FBGRX : each time invest $3000 - considered dividends and captialGain: total $40,000
#       result1:
#           when price decrease 2%, buy 3000 worth shares
#           when price increase 9%, sell 3000 worth shares
#           each year is about 16-17% profit --- Great
#       results2:
#           when price decrease 0.3%, buy 5000 worth shares
#           when price increase 5%, sell 5000 worth shares
#           each year is about 22.7% return on over 10-year on average
#       fidelity shows that 17.68%
# 3. ETF WAINX india index: each time invest $2800 total investment : $30000, profit 12.59%; fidelity 12.92%
#       when price decrease 1% buy $2600 worth shares
#       when price increase 7% sell 2600 worth shares
#       results2:
#           buy @-0.003, sell 0.07, each time BUY $3000; SELL 6000. return  15.55%
# 4. FHKCX china index: each time invest $2400, total investment: 10000. profit: ??
#       when price decrease 2%, buy
#       when price increase 9%, sell
# 5. FXAIX Fidelity 500 index: each time invest $2800. buy when 3% decrease, and sell @8000 increase,annual profit=13.1%
#       (10 year return 13.37% from fidelity)
#       optimal results: buy @0.01; sell @0.08, each 6000, averge profit = 13.1%
#       Result2:
#           buy 0.3% $3000; sell 6% $6000.
#           profit = 16.2%
# 6. FMSDX fidelity multi-asset index:
#       (5 year 9.49%,  from fidelity
#       total 9yr, life 8.43% from fidelity)
#       my calculation 6.4% not worth to invest in this way- buy 0.01, sell 0.06, each 6K
#       Results2:
#           buy when decrease 0.5%
#           sell when increase 6%
#           each time buy and sell 3000 worth stock.
#           profit 9.9%
#7. FSPCX fideliy insurance portfolid
#       10 year average 13.48% from fidelity
#       optimal average 13.59%
#           each buy 0.0167, sell@0.085, each 6100
#       Results2:
#           buy decrease 0.3% ; Sell increase 5% , both 5000
#           return 29.8%
#8. FNILX fidelity zero large ca index with zero expense-update: 10-10-2024
#       6 year average return 13.91% from fidelity
#       optimal average 14.22% buy 0.04, sell 0.08, each buy 2000, sel 500
#       results2: return 16.8%
#           buy @0.005; sell@0.06, each time buy $1000, sell $500
import pandas as pd
import datetime
import timeit
#from pandas.io import data, wb # becomes
import pandas_datareader as web
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import rcParams
import seaborn as sb
# from yahoofinancials import YahooFinancials
import numpy as np
from numpy.random import randn
from pandas import Series, DataFrame
import os
import yfinance as yf
#get_ipython().magic('matplotlib inline')
rcParams['figure.figsize'] = 5, 4   #5inch wide, 4 tall
sb.set_style('whitegrid')

style.use('ggplot')

def download_all(start, end):
    df1 =web.DataReader("TSLA", "stooq", start, end)
    df2 =web.DataReader("GE","stooq", start, end)
    df3 =web.DataReader("SQ","stooq", start, end)
    df4 =web.DataReader("BIDU","stooq",start, end)
    df5 =web.DataReader("ALB","stooq", start, end)
    df6 =web.DataReader("MSFT","stooq",start, end)
    df7 =web.DataReader("TWTR","stooq", start, end)
    df8 =web.DataReader("FMC","stooq",start, end)
    df9 =web.DataReader("UAL","stooq",start, end)


    dfpd = pd.DataFrame(df1)
    # filePath="C:/Users/super/PycharmProjects/yang/code/projectsStock/final"
    # dfpd.to_csv(filePath + "/TSLA.csv")
    dfpd.to_csv("TSLA.csv")
    dfpd = pd.DataFrame(df2)
    dfpd.to_csv("GE.csv")
    dfpd = pd.DataFrame(df3)
    dfpd.to_csv("SQ.csv")
    dfpd = pd.DataFrame(df4)
    dfpd.to_csv("BIDU.csv")
    dfpd = pd.DataFrame(df5)
    dfpd.to_csv("ALB.csv")
    dfpd = pd.DataFrame(df6)
    dfpd.to_csv("MSFT.csv")
    dfpd = pd.DataFrame(df7)
    dfpd.to_csv("TWTR.csv")
    dfpd = pd.DataFrame(df8)
    dfpd.to_csv("FMC.csv")
    dfpd = pd.DataFrame(df9)
    dfpd.to_csv("UAL.csv")

    Fjpnx1=web.DataReader("SMFG","stooq",start, end)
    Fjpnx2=web.DataReader("HTHIY","stooq",start, end)
    Fjpnx3=web.DataReader("RNECY","stooq",start, end)
    Fjpnx4=web.DataReader("SONY","stooq",start, end)
    Fjpnx5=web.DataReader("IX","stooq",start, end)
    Fjpnx6=web.DataReader("SHECY","stooq",start, end)
    Fjpnx7=web.DataReader("HOCPY","stooq",start, end)
    Fjpnx8=web.DataReader("DNZOY","stooq",start, end)
    Fjpnx9=web.DataReader("FUJIY","stooq",start, end)
    Fjpnx10=web.DataReader("TKOMY","stooq",start, end)
    Fjpnx=web.DataReader("FJPNX","stooq",start, end)
    dfpd = pd.DataFrame(Fjpnx1)
    dfpd.to_csv("FGPNX_SMFG.csv")
    dfpd = pd.DataFrame(Fjpnx2)
    dfpd.to_csv("FGPNX_HTHIY.csv")
    dfpd = pd.DataFrame(Fjpnx3)
    dfpd.to_csv("FGPNX_RNECY.csv")
    dfpd = pd.DataFrame(Fjpnx4)
    dfpd.to_csv("FGPNX_SONY.csv")
    dfpd = pd.DataFrame(Fjpnx5)
    dfpd.to_csv("FGPNX_IX.csv")
    dfpd = pd.DataFrame(Fjpnx6)
    dfpd.to_csv("FGPNX_SHECY.csv")
    dfpd = pd.DataFrame(Fjpnx7)
    dfpd.to_csv("FGPNX_HOCPY.csv")
    dfpd = pd.DataFrame(Fjpnx8)
    dfpd.to_csv("FGPNX_DNZOY.csv")
    dfpd = pd.DataFrame(Fjpnx9)
    dfpd.to_csv("FGPNX_FUJIYcsv")
    dfpd = pd.DataFrame(Fjpnx10)
    dfpd.to_csv("FGPNX_TKOMY.csv")
    dfpd = pd.DataFrame(Fjpnx)
    dfpd.to_csv("FGPNX.csv")
    return
def download_yh(start, end, ticket):
    if isinstance(ticket, str):
        yahoo_financials_mutualfunds = yf.Ticker(ticket)
        daily_mutualfund_prices = yahoo_financials_mutualfunds.history(start=start, end=end,interval="1d")
        df = pd.DataFrame(daily_mutualfund_prices)
        # df = pd.DataFrame(daily_mutualfund_prices['Close'])
        df.to_csv(ticket + '.csv')
    return daily_mutualfund_prices

if __name__=="__main__":
    start = datetime.datetime(2018, 7, 3)
    end2 = datetime.datetime.now()
    # end = datetime.datetime(end2.year, end2.month, end2.day) - datetime.timedelta(days=2)
    end = datetime.datetime(end2.year, end2.month, end2.day)

    ticket = 'FMSDX'
    start='2015-09-28'
    end='2024-09-28'
    df = download_yh(start, end, ticket)
    #   df = pd.read_csv('FNILX.csv')
    # to answer the first question, at what % increase and decrease it is the best to buy or sell
    TotalMoney=18560.0
    # variables are ETF1 =0.05, investment_each=2000

    ETFb = 0.02
    ETFs = 0.09

    totalETF=ETFb*TotalMoney
    investment_each=1000.0

    #   df['close'].plot(); plt.legend(loc='best') # this only plot index

    df2 = df["Close"]

    plt.figure()
    df2.plot()
    plt.legend(loc='best')
    plt.plot(df2)
    # plt.show()
    # analysis : start from start date, purchased initial $2000,
    # each time price increase 5%, sell $2000 stock,
    # each time decrease every 5%, buy $2000
    basePrice=df['Close'].values[0]  #calculate base price
    num=0
    investmentETF=investment_each
    investmentCash=TotalMoney-investmentETF
    targetPrice_sell = (1 + ETFs) * basePrice
    targetPrice_buy = (1 - ETFb) * basePrice
    shares = investmentETF / df['Close'].values[0]
    results_ETF=[]
    results_share=[]
    results_cash=[]
    results_equity=[]
    results_control=[]
    results_basePrice=[]
    results_dividends_CapGain=[]
    profit=[]
    # sell=[0.02,0.025, 0.03, 0.035, 0.04, 0.05, 0.06, 0.07,0.075, 0.08,0.085, 0.09, 0.1]
    # buy =[ 0.01, 0.0133, 0.0167, 0.02,0.233, 0.267,0.03, 0.04, 0.05, 0.06]
    sell=[ 0.05,0.055, 0.06, 0.065,0.07]
    buy =[0.003, 0.005, 0.007, 0.01, 0.02,0.03]
    # sell = [1.1]
    # buy = [0.08, 0.07]
    # each_buy = [5000]
    # each_buy=[1000, 2000,3000, 4000,5000]
    # each_sell = [500,1000,2000,3000, 4000, 5000, 6000]

    each_buy = [2000, 2500,3000,3500, 4000]
    each_sell = [ 1000, 2000,2500, 3000,3500, 4000]
    sell_list=[]
    buy_list=[]
    each_list=[]
    each_list_sell=[]
    Profit2_list2=[]
    shares_list=[]
    for i in range(len(sell)):
        for j in range(len(buy)):
            for k in range(len(each_buy)):
                for l in range(len(each_sell)):
                    num = 0
                    # print("i=" + str(i)+ " j=" + str(j) + " k=" +str(k) +" l=" +str(l))
                    results_ETF = []
                    results_share = []
                    results_cash = []
                    results_equity = []
                    results_control = []
                    results_basePrice = []
                    results_dividends_CapGain = []
                    profit = []
                    ETFs = sell[i]
                    ETFb = buy[j]
                    basePrice = df['Close'].values[0]  # calculate base price
                    investment_each = each_buy[k]
                    # investmentETF ETF cash value
                    investmentETF = investment_each
                    # investmentETF_sell = each_sell[l]
                    investmentCash = TotalMoney - investmentETF
                    targetPrice_sell = (1 + ETFs) * basePrice
                    targetPrice_buy = (1 - ETFb) * basePrice
                    shares = investmentETF / df['Close'].values[0]
                    # shares_sell = investmentETF_sell/df['Close'].values[0]
                    while num<df.index.__len__():
                        targetPrice_sell = (1 + ETFs) * basePrice
                        targetPrice_buy = (1 - ETFb) * basePrice
                        # basePrice = df['Close'].values[num]+df['Dividends'][num]+df['Capital Gains'][num]
                        df['adjustPrice'] = df['Close'] + df['Dividends'] + df['Capital Gains'] # not consider the tax since it is in tax deduction account
                        if df['Close'].values[num]>targetPrice_sell and (shares-each_sell[l]/df['Close'].values[num])>0:
                            # sell ? worth shares
                            investmentCash=investmentCash+each_sell[l]
                            shares = shares-each_sell[l]/df['Close'].values[num]

                            # shares_Div_CP =  (df['Dividends'].values[num] + df['Capital Gains'].values[num])*shares/investment_each/df['Close'].values[num]
                            shares_Div_CP = (df['Dividends'].values[num] + df['Capital Gains'].values[
                                num]) * shares / df['Close'].values[num]

                            shares =shares + shares_Div_CP
                            basePrice = df['Close'].values[num]
                            targetPrice_sell = (1 + ETFs) * basePrice
                            targetPrice_buy = (1 - ETFb) * basePrice
                            investmentETF=df['Close'].values[num]*shares
                            results_equity.append(investmentETF + investmentCash)
                            results_cash.append(investmentCash)
                            results_share.append(shares)
                            results_ETF.append(investmentETF)
                            results_control.append(-1)
                            results_basePrice.append(basePrice)
                        elif df['Close'].values[num] < targetPrice_buy and investmentCash > investment_each:
                            # to buy
                            investmentCash = investmentCash - investment_each
                            shares = shares + investment_each/df['Close'].values[num]
                            shares_Div_CP = (df['Dividends'].values[num] + df['Capital Gains'].values[num]) * shares / \
                                            df['Close'].values[num]
                            shares = shares + shares_Div_CP
                            basePrice = df['Close'].values[num]
                            targetPrice_sell = (1 + ETFs) * basePrice
                            targetPrice_buy = (1 - ETFb) * basePrice
                            investmentETF = shares * df['Close'].values[num]
                            results_equity.append(investmentETF + investmentCash)
                            results_cash.append(investmentCash)
                            results_share.append(shares)
                            results_ETF.append(investmentETF)
                            results_control.append(1)
                            adjustPrice = df['Close'].values[num] + df['Dividends'][num] + df['Capital Gains'][num]
                            results_basePrice.append(basePrice)
                        else:
                            # investmentETF = shares * df['Close'].values[num]
                            shares_Div_CP = (df['Dividends'].values[num] + df['Capital Gains'].values[num]) * shares / \
                                            df['Close'].values[num]
                            shares = shares + shares_Div_CP
                            investmentETF = shares * df['Close'].values[num]
                            results_equity.append(investmentETF + investmentCash)
                            results_cash.append(investmentCash)
                            results_share.append(shares)
                            results_ETF.append(investmentETF)
                            results_control.append(0)
                            # basePrice = df['Close'].values[num]
                            results_basePrice.append(basePrice)
                            results_dividends_CapGain.append(df['Dividends'].values[num] + df['Capital Gains'].values[num])
                        # do nonthing
                        num = num + 1
                    Profit2_list2.append((results_equity[-1]/TotalMoney))
                    sell_list.append(sell[i])
                    buy_list.append(buy[j])
                    each_list.append(each_buy[k])
                    each_list_sell.append(each_sell[l])
                    shares_list.append(shares)
    Dict_Opt={'buy ': buy_list,
              'sell': sell_list,
              'each_buy': each_list,
              'each_sell': each_list_sell,
              'profit':Profit2_list2 }
    # print("length of sell_list =" + str(len(sell_list)))
    # print("length of buy_list =" + str(len(buy_list)))
    # print("length of each_list =" + str(len(each_list)))
    # print("length of Profit2_list2 =" + str(len(Profit2_list2)))
    df4=DataFrame(Dict_Opt)
    df4.to_csv('opt_' + ticket)
    print('Profit2_list2='  +  str(max(Profit2_list2)))
    max_index = Profit2_list2.index(max(Profit2_list2))
    print("max@ buy=" + str(buy_list[max_index]))
    print("max@ sell=" + str(sell_list[max_index]))
    print("max@ each_=" + str(each_list[max_index]))
    print("max@ each_sell=" + str(each_list_sell[max_index]))
    print("final shares =" + str(shares_list[max_index]))
    print("final Cash = " +str(investmentCash))
    Dict={'total_Equity': results_equity, 'total_cash': results_cash,'total_share': results_share, 'event':results_control ,'ETF_price': df['Close'].values, 'ETF_CapGain_Div': df['Dividends'].values + df['Capital Gains'].values}
    df3=DataFrame(Dict,index=df.index)
    df3.to_csv('summary_ETF_step1_2000_5p')
    plt.figure()
    plt.plot(df3['total_Equity'])
    # for ticket in tickets:
    #     TicketName = ticket + ".csv"
    #     Ticket = pd.read_csv(TicketName, parse_dates=True, index_col=0)
    #     Ticket['Ave'] = (Ticket['Open'] + Ticket['Close']) / 2  # before is df
    #     current_price=buy_pricef = Ticket[Ticket.index == start]
    # Fjpnx1=web.DataReader("SMFG","stooq",start, end)
    # Fjpnx2=web.DataReader("HTHIY","stooq",start, end)
    # Fjpnx3=web.DataReader("RNECY","stooq",start, end)
    # Fjpnx4=web.DataReader("SONY","stooq",start, end)
    # Fjpnx5=web.DataReader("IX","stooq",start, end)
    # Fjpnx6=web.DataReader("SHECY","stooq",start, end)
    # Fjpnx7=web.DataReader("HOCPY","stooq",start, end)
    # Fjpnx8=web.DataReader("DNZOY","stooq",start, end)
    # Fjpnx9=web.DataReader("FUJIY","stooq",start, end)
    # Fjpnx10=web.DataReader("TKOMY","stooq",start, end)
    # Fjpnx=web.DataReader("FJPNX","stooq",start, end)
    # Ticket = pd.read_csv(TicketName, parse_dates=True, index_col=0)
    # print('final results')
    # print('-----------------------------------')
    # print('total shares of ' + ticket + ' = ' + str(results_share[-1]))
    # print('cash '+' = ' + str(results_cash[-1]))
    # print('ETF price per share =' + str(df['Close'].values[-1]))
    # print('total equality =' + str(results_equity[-1]))
    # print('profit = ' + str((results_equity[-1]/TotalMoney-1)*100) +'%')
