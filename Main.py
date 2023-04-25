import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.dates as mdates


def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data['Adj Close']


def least_squares_polynomial(x, y, degree):
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
    degree = int(input("Enter the degree of least squares polynomial: "))
    periods = int(input("Enter the number of periods: "))

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')

    stock_data = get_stock_data(stock_symbol, start_date, end_date)

    x = np.linspace(0, len(stock_data)-1, len(stock_data))
    y = stock_data

    poly = least_squares_polynomial(x, y, degree)
    trend, strength = evaluate_trend(poly, x)

    # Find the equation of the tangent line at the current date
    current_date_index = len(stock_data) - 1
    current_date_x = x[current_date_index]
    tangent_slope = poly.deriv(1)(current_date_x)
    tangent_intercept = y[current_date_index] - tangent_slope * current_date_x
    tangent_y = tangent_slope * current_date_x + tangent_intercept

    # Plot the least squares polynomial and the trend line
    future_dates = pd.date_range(start=stock_data.index[0], periods=len(stock_data) + periods // 5, freq='D')
    x_future = np.linspace(current_date_x, current_date_x + periods // 5, len(future_dates))
    y_trend = poly(x)
    y_trend_line = tangent_slope * x_future + tangent_intercept

    print(f"Tangent line y value: {tangent_y:.2f}")
    print(f"Polynomial y value: {poly(current_date_x):.2f}")

    fig, ax = plt.subplots()
    ax.plot(stock_data.index, stock_data, label="Actual Prices")
    ax.plot(stock_data.index, y_trend, label="Least Squares Polynomial")
    ax.plot(future_dates, y_trend_line, label="Trend Line")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"{stock_symbol} Stock Price Trend")
    ax.legend()
    fig.autofmt_xdate()
    plt.show()



main()
