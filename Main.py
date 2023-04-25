import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.dates as mdates


def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data['Adj Close']


def interpolating_polynomial(x, y, degree):
    mask = np.where(~np.isnan(y))[0]
    return np.poly1d(np.polyfit(x[mask], y[mask], degree))


def evaluate_trend(poly, x):
    first_derivative = poly.deriv(1)
    avg_derivative = np.mean([first_derivative(x_i) for x_i in x[-10:]])
    trend = "up" if avg_derivative > 0 else "down"
    strength = abs(avg_derivative)
    return trend, strength


def main():
    stock_symbol = input("Enter the stock symbol: ").upper()
    days_range = int(input("Enter the range of days to look back: "))
    degree = int(input("Enter the degree of interpolating polynomial: "))

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')

    stock_data = get_stock_data(stock_symbol, start_date, end_date)

    x = np.linspace(0, len(stock_data)-1, len(stock_data))
    y = stock_data

    poly = interpolating_polynomial(x, y, degree)
    trend, strength = evaluate_trend(poly, x)

    y_trend = poly(x)
    y_future = poly(x[-1] + 1) + strength * np.sign(poly.deriv(1)(x[-1]))

    # Calculate the trend line points based on the derivative
    slope = poly.deriv(1)(x[-1])
    y_trend_line = slope * (x - x[-1]) + y_trend[-1]

    fig, ax = plt.subplots()
    ax.plot(stock_data.index, stock_data, label="Actual Prices")
    ax.plot(stock_data.index, y_trend, label="Interpolating Polynomial")
    ax.plot(stock_data.index, y_trend_line, label="Trend Line")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"{stock_symbol} Stock Price Trend")
    ax.legend()
    fig.autofmt_xdate()
    plt.show()


main()
