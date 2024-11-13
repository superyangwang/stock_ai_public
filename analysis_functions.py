import yfinance as yf
import pandas as pd
import os
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import numpy as np

# Define MACD calculation function
def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    # Calculate short and long EMA
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    # Calculate MACD and Signal Line
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_histogram'] = df['MACD']-df['Signal Line']
    # Identify MACD zero crossings : negative to possitive to sell
    df['MACD_zero_cross_sell'] = ((df['MACD_histogram'] <= 0) & (df['MACD_histogram'].shift(1) > 0)) & df['MACD']>0
    # Identify MACD zero crossings positive to negative to buy
    df['MACD_zero_cross_buy'] = ((df['MACD_histogram'] >= 0) & (df['MACD_histogram'].shift(1) < 0)) & df['MACD']<0
    plttt = 0
    if plttt==1:
        # plot
        plt.figure(figsize=(14, 7))

        # Plot MACD and Signal line
        plt.plot(df.index, df['MACD'], label='MACD Line', color='blue', linewidth=1.5)
        plt.plot(df.index, df['Signal Line'], label='Signal Line', color='red', linestyle='--', linewidth=1)

        # Plot Fast and Slow EMA lines
        plt.plot(df.index, df['EMA_12'], label='12-Day EMA (Fast)', color='green', linestyle='-.', linewidth=0.8)
        plt.plot(df.index, df['EMA_26'], label='26-Day EMA (Slow)', color='purple', linestyle='-.', linewidth=0.8)

        # Add a legend and labels
        plt.legend(loc='upper left')
        plt.title(f'MACD and EMA Lines for {df['Ticker'][0]}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()

        plt.show()
        # Save the plot as a PNG file
        file_name = 'macd_figure_' + df['Ticker'][0] + '.png'
        plt.savefig(file_name)
    return df
password = os.getenv("YANGWOODSEMAIL_PASSWORD")
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

def volumeTrigger(ave, std, data):
    '''
    :param ave: float , average value of volume in one min on average in the past 1month
    :param std: float,  standard dev of volume in one min on average in the past 1month
    :param data: dataframe, from yahoo finance downloading.
    :return:
    '''
    printStr =''
    # calculate volume cateria by min
    volume = [max(ave * 0.5, ave - std), ave + std, ave + 2 * std, ave + 3 * std]
    Volume_5m = data['Volume'].tail(5).mean()  # all volume per min
    Volume_10m = data['Volume'].tail(10).mean()
    Volume_1h = data['Volume'].tail(60).mean()
    Volume_today = data['Volume'].mean()
    if Volume_1h < volume[0]:
        printStr = printStr + '10min volume is small' + '\n'
    elif Volume_1h < volume[1]:
        print('volume is in the middle, no need to print')
    elif Volume_1h < volume[2]:
        printStr = printStr + 'large volume(1std)' + '\n'
    elif Volume_1h < volume[3]:
        printStr = printStr + 'very large volume(2std)' + '\n'
    else:
        printStr = printStr + 'extreme large volume(>3rd std)' + '\n'

    return printStr

def price_delta(data):
    delta = data['Close'].tail(10).iloc[-1] - data['Close'].tail(10).iloc[-10]
    delta_p = (data['Close'].tail(10).iloc[-1] - data['Close'].tail(10).iloc[-10])/data['Close'].tail(10).iloc[-10]
    if delta > 0:
        printStr ='Price Up in 10min '
    else:
        printStr = 'Price Down in 10min '
    printStr = printStr + str(delta_p*100) + '%'

    return printStr


import pandas as pd
import matplotlib.pyplot as plt


def calculate_smi(data, p1=14, p2=14, smooth_k=3, smooth_d=3):
    """
    Calculate the Stochastic Momentum Index (SMI).

    Parameters:
    - data: DataFrame containing 'high', 'low', and 'close' columns
    - p1: period for the highest high and lowest low (default is 14)
    - p2: period for the double smoothing (default is 14)
    - smooth_k: period for smoothing the K value (default is 3)
    - smooth_d: period for smoothing the D value (default is 3)

    Returns:
    - DataFrame with SMI_K and SMI_D columns
    """

    # Highest high and lowest low for period p1
    data['high_max'] = data['High'].rolling(window=p1).max()
    data['low_min'] = data['Low'].rolling(window=p1).min()

    # Calculate midpoint range
    data['mid_point'] = (data['high_max'] + data['low_min']) / 2

    # Distance of the close from the midpoint (double smoothing)
    data['d_close'] = data['Close'] - data['mid_point']
    data['d_close_smooth'] = data['d_close'].rolling(window=p2).mean()
    data['range_smooth'] = (data['high_max'] - data['low_min']).rolling(window=p2).mean()

    # K and D values
    data['K'] = 100 * (data['d_close_smooth'] / (0.5 * data['range_smooth']))
    data['K_smooth'] = data['K'].rolling(window=smooth_k).mean()  # Smoothing K value
    # data['SMI_D'] = data['K_smooth'].rolling(window=smooth_d).mean()  # D value (double smoothed K)
    d_ma_type = 'SMA'
    # Applying the selected moving average type to %D line
    if d_ma_type == 'SMA':
        data['D'] = data['K_smooth'].rolling(window=smooth_d).mean()
    elif d_ma_type == 'EMA':
        data['D'] = data['K_smooth'].ewm(span=smooth_d, adjust=False).mean()
    else:
        raise ValueError(
            "Invalid d_ma_type. Use 'SMA' for Simple Moving Average or 'EMA' for Exponential Moving Average.")

    # Drop unnecessary columns for clarity
    # Drop unnecessary columns
    data.drop(['high_max', 'low_min', 'mid_point', 'd_close', 'd_close_smooth', 'range_smooth'], axis=1, inplace=True)
    tempStr = ' '
    # return string for printing
    if data['K_smooth'].iloc[-1]<-40 or data['K_smooth'].iloc[-1]>40:
        formatted_str = "{:.1f}".format(data['K_smooth'].iloc[-1])
        if data['K_smooth'].iloc[-1]<0:
            tempStr = 'Oversold ' + formatted_str
        if data['K_smooth'].iloc[-1]>0:
            tempStr = 'Overbought ' + formatted_str
        if abs(data['K_smooth'].iloc[-1]-data['D'].iloc[-1])<5:
            temp_delta = abs(data['K_smooth'].iloc[-1]-data['D'].iloc[-1])
            tempStr = tempStr + 'D and K close to cross, 2nd order =' + "{:.1f}".format(temp_delta)
        delta1 = abs(data['K_smooth'].iloc[-1] - data['K_smooth'].iloc[-3]) /2
        delta2 = abs(data['K_smooth'].iloc[-2] - data['K_smooth'].iloc[-4]) / 2
        delta3 = abs(data['K_smooth'].iloc[-3] - data['K_smooth'].iloc[-5]) / 2
        delta4 = abs(data['K_smooth'].iloc[-4] - data['K_smooth'].iloc[-6]) / 2
        Y = [delta4, delta3, delta2, delta1]
        X = np.arange(len(Y))
        # Perform linear fit
        slope, intercept = np.polyfit(X, Y, 1)
        if abs(slope)<5:
            # tempStr =tempStr + f"slope : {slope}" + f"Intercept (Gain): {intercept}"
            tempStr = (tempStr + ' K is close to peak value, \n' + '  2nd order = ' + str(slope))  + '\n'



    return data[['K_smooth', 'D']].rename(columns={'K_smooth': 'SMI_K', 'D': 'SMI_D'}) , tempStr


def plot_smi(data, overbought_level = 40, oversold_level = -40, save_path='SMI.png'):
    """
    Plot the Stochastic Momentum Index (SMI) with overbought and oversold levels.

    Parameters:
    - data: DataFrame containing 'SMI_K' and 'SMI_D' columns
    """

    # Define overbought and oversold levels
    # overbought_level = 40
    # oversold_level = -40

    # Plot SMI_K and SMI_D
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['SMI_K'], label='%K (SMI)', color='black', linewidth=1.5)
    plt.plot(data.index, data['SMI_D'], label='%D (SMI)', color='red', linewidth=1.5)

    # Plot overbought and oversold lines
    plt.axhline(y=overbought_level, color='grey', linestyle='--', linewidth=1)
    plt.axhline(y=oversold_level, color='grey', linestyle='--', linewidth=1)

    # Fill area between overbought and oversold levels
    # plt.fill_between(data.index, overbought_level, oversold_level, color='grey', alpha=0.1)
    # Highlight grey-filled areas based on K
    plt.fill_between(
        data.index, data['SMI_K'], -40,
        where=(data['SMI_K']< -40),
        color='grey', alpha=0.9,
        interpolate=True, label='K < -40'
    )
    plt.fill_between(
        data.index, 40, data['SMI_K'],
        where=(data['SMI_K'] > 40),
        color='grey', alpha=0.9,
        interpolate=True, label='K > 40'
    )
    # Labels and legend
    plt.title('Stochastic Momentum Index (SMI)')
    plt.ylabel('SMI Value')
    plt.legend(loc='upper left')
    plt.grid(True)
    # plt.show()
    # Fill
    # Save the plot as a PNG file
    plt.savefig(save_path, format='png')
    plt.close()  # Close the plot to free up memory

# Example usage:
# Assuming `df` is a DataFrame containing 'high', 'low', and 'close' columns# df = pd.DataFrame({
# #     'high': [...],
# #     'low': [...],
# #     'close': [...]
# # })
# # smi_df = calculate_smi(df)
# # plot_smi(smi_df)
