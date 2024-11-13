import os
import yfinance as yf
import datetime
import analysis_functions
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


'''
Goal of this file is to auto fill the csv trigger file. 
1. run once a week on github. to automatically update the csv and commit into repo.
2. update 'stock_Trigger.csv' with latest stock price(close) and average volume.
'''
password = os.getenv("YANGWOODSEMAIL_PASSWORD")
# message=os.getenv("")


analysis_functions.authenticate()
Ticketcsv = pd.read_csv('stock_Trigger' + '.csv', index_col=0)
i=0
Ticket_names=Ticketcsv['Ticket Name']

buy_price = Ticketcsv['Buy Price']
sell_price = Ticketcsv['Sell Price']
printStr = ' '
trigger = 0

# load csv file download from fidelity
Rollover = pd.read_csv('Rollover_Portfolio_Positions_Nov-07-2024.csv')
filtered_Rollover = Rollover[Rollover['Symbol'].str.endswith('*') == False | (Rollover['Symbol'] == 'nnn')]
combined_list = list(set(filtered_Rollover['Symbol'].tolist() + Ticket_names.tolist()))
combined_list =sorted(combined_list)


for ticket in combined_list:
    # Download the past 5 days of data with a 10-minute interval
    # # Download data for today with 1-minute interval
    # data = yf.download(ticket, period='1d', interval='1m')
    # # TicketTrigger=Ticketcsv.loc[i]
    # # Filter the last 1 hour of data
    # # Calculate the timestamp for 1 hour ago


    # Fetch the data
    data = yf.download(tickers=ticket, interval='1h', period='1mo')
    volume_hourly = data['Volume'].mean()
    volume_std=data['Volume'].std()
    hig_volume=2*volume_std + volume_hourly
    low_volume=max(volume_hourly -2*volume_std,volume_hourly*0.5)



    # Update CSV volume data
    Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'hourly volume ave'] = volume_hourly
    Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'hourly volume std'] = volume_std
    Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'Current Price'] = data['Close'].iloc[-1]

    if not Rollover.loc[Rollover['Symbol'] == ticket, 'Cost Basis Total'].empty:
        Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'Base Cost'] =\
            Rollover.loc[Rollover['Symbol'] == ticket, 'Cost Basis Total'].iloc[0]
        Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'Total Numbers'] =\
            Rollover.loc[Rollover['Symbol'] == ticket, 'Quantity'].iloc[0]
        Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket, 'Percent of Account'] =\
            Rollover.loc[Rollover['Symbol'] == ticket, 'Percent Of Account'].iloc[0]
        print(Ticketcsv.loc[Ticketcsv['Ticket Name'] == ticket] )
Ticketcsv.to_csv("stock_Trigger2.csv")