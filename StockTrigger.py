import os
from fileinput import filename

import yfinance as yf
import datetime
import analysis_functions
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import platform
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

# Define the file path for the HTML output
html_file = "Stock_plot.html"
trig_ticket = []
trig_text = []
# Write the initial HTML structure
with open(html_file, "w") as file:
    file.write("<html>\n<head>\n<title>Image Plot</title>\n</head>\n<body>\n")
    file.write("<h1>Image Plot with Filenames</h1>\n")
    for ticket in Ticket_names:
        # Download the past 5 days of data with a 10-minute interval
        # # Download data for today with 1-minute interval
        # data = yf.download(ticket, period='1d', interval='1m')
        # # TicketTrigger=Ticketcsv.loc[i]
        # # Filter the last 1 hour of data
        # # Calculate the timestamp for 1 hour ago


        # Fetch the data
        data = yf.download(tickers=ticket, interval='1m', period='1d')
        # one_hour_ago = datetime.now(tz=data.index.tz) - timedelta(hours=1)
        # stock_data = yf.download(tickers=ticket, interval='1m', period='15m')
        try:
            # stock_data = data[data.index >= one_hour_ago]
            # Check if there's any data in the last hour
            stock_data = data.tail(15)
            if stock_data.empty:
                raise ValueError("No data available within the past hour.")
            max_price = stock_data['High'].max()
            min_price = stock_data['Low'].min()
            # print(ticket)
            ave = Ticketcsv.loc[i]['hourly volume ave']/60
            std = Ticketcsv.loc[i]['hourly volume std']/60
            if min_price < Ticketcsv.loc[i]['Buy Price']:
                printStr = printStr + '\n' + ticket + '\n'
                printStr = printStr + ticket+ ' current price below ' + str(min_price) +'\n'
                printStr = printStr + 'Buy ' + ticket +'\n'
                trigger=trigger+1
                # trig_ticket.append(ticket)
                printStr = printStr + "\n"
                tempStr = analysis_functions.price_delta(data)
                printStr = printStr + tempStr + "\n"

                tempStr = analysis_functions.volumeTrigger(ave, std, data)
                printStr = printStr + tempStr + "\n"
                printStr = printStr + '----------\n'

                smi_df , tempStr = analysis_functions.calculate_smi(data)
                filename = 'smi_' + ticket + '.png'
                analysis_functions.plot_smi(smi_df, 40, -40,filename)
                printStr = printStr + tempStr
                img_filename = f"smi_{ticket}.png"
                # 'smi_' + ticket + '.png'

                # Add the filename as a caption and image in the HTML
                file.write(f'<p>{img_filename}</p>\n')
                file.write(f'<p>{printStr}</p>\n')
                file.write(f'<img src="{img_filename}" alt="Image {ticket}">\n')
            elif max_price > Ticketcsv.loc[i]['Sell Price']:
                trig_ticket.append(ticket)
                printStr = printStr + '\n' + ticket + '\n'
                printStr = printStr + ticket + ' current price above ' + str(max_price) + '\n'
                printStr = printStr + 'Sell ' + ticket +'\n'
                trigger = trigger + 1
                printStr = printStr + "\n"
                tempStr = analysis_functions.price_delta(data)
                printStr = printStr + tempStr + "\n"

                tempStr = analysis_functions.volumeTrigger(ave, std, data)
                printStr = printStr + tempStr + "\n"
                printStr = printStr + '----------\n'

                smi_df, tempStr = analysis_functions.calculate_smi(data)
                filename = 'smi_' + ticket + '.png'
                analysis_functions.plot_smi(smi_df, 40, -40, filename)
                printStr = printStr + tempStr
                file.write(f'<p>{filename}</p>\n')
                file.write(f'<p>{printStr}</p>\n')
                file.write(f'<img src="{filename}" alt="Image {ticket}">\n')
            else:
                print('doing nothing, no printStr')
            # data = yf.download(ticket, period='6mo', interval='1d')
            # analysis_functions.calculate_macd(data, short_window=12, long_window=26, signal_window=9)
            # print('pause here')

            # print(printStr)

        except ValueError as ve:
            # Handle the case where no data is available in the last hour
            print(ve)
        i=i+1
    # Close the HTML tags
    file.write("</body>\n</html>")

print(f"HTML file '{html_file}' created successfully.")


# Open the HTML file for writing
'''
with open(html_file, "w") as file:
    # Write the initial HTML structure
    file.write("<html>\n<head>\n<title>Image Plot</title>\n</head>\n<body>\n")
    file.write("<h1>Image Plot with Filenames</h1>\n")

    # Loop through temp1.png to temp10.png
    for ticket in trig_ticket:
        img_filename = f"smi_{ticket}.png"
        # 'smi_' + ticket + '.png'

        # Add the filename as a caption and image in the HTML
        file.write(f'<p>{img_filename}</p>\n')
        file.write(f'<img src="{img_filename}" alt="Image {ticket}">\n')

        # Print the filename to the console
        print(img_filename)

    # Close the HTML tags
    file.write("</body>\n</html>")

print(f"HTML file '{html_file}' created successfully.")
'''

print(printStr)
print('trigger=')
print(trigger)
if trigger > 0:
    system = platform.system().lower()

    # Check if the system name contains 'windows'
    if 'windows' in system:
        print("You are using Windows.")
    else:
        analysis_functions.textGoogle(printStr, password)