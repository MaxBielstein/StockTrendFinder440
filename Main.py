import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.dates as mdates


def get_degree(days_range):
    if days_range <= 20:
        return 1
    elif days_range <= 99:
        return 2
    elif days_range <= 200:
        return 3
    else:
        return 4


def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data.fillna(method='ffill', inplace=True)
    return stock_data['Adj Close']

def least_squares_polynomial(x, y, degree):
    mask = np.where(~np.isnan(y))[0]
    return np.poly1d(np.polyfit(x[mask], y[mask], degree))


def tangent_line(strength, x, y_intercept):
    return strength * x + y_intercept


def evaluate_trend(poly, x):
    dy_dx = np.gradient(poly(x))
    average_derivative = np.mean(dy_dx)
    strength = average_derivative
    trend = ""
    if average_derivative > 0:
        trend = f"Up"
    else:
        trend = f"Down"
    return trend, strength


def main():
    stock_symbol = input("Enter the stock symbol: ").upper()
    days_range = int(input("Enter the range of days to look back (10-1000): "))
    degree = get_degree(days_range)

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')

    stock_data = get_stock_data(stock_symbol, start_date, end_date)

    x = np.linspace(0, len(stock_data) - 1, len(stock_data))
    y = stock_data

    poly = least_squares_polynomial(x, y, degree)
    trend, strength = evaluate_trend(poly, x)

    current_date_index = len(stock_data) - 1
    current_date_x = x[current_date_index]
    slope = strength
    y_intercept = poly(current_date_x) - slope * current_date_x
    y_trend = poly(x)
    y_tangent = tangent_line(slope, x, y_intercept)

    fig, ax = plt.subplots()
    ax.plot(stock_data.index, stock_data, label="Actual Prices")
    ax.plot(stock_data.index, y_trend, label="Least Squares Polynomial")
    ax.plot(stock_data.index[(days_range // 3) + 1:], y_tangent[(days_range // 3) + 1:], label="Trend Line",
            linestyle="--")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    correct_trend_rate = back_test(stock_symbol, days_range)
    ax.set_title(f"{stock_symbol} Stock Price Trend\nTrend: {trend}, Strength: {np.abs(strength):.2f}, Accuracy: {correct_trend_rate}")


    ax.legend()
    fig.autofmt_xdate()
    plt.show()

def back_test(stock_symbol, days_range):
    correct_trend = 0
    incorrect_trend = 0

    for i in range(10):
        end_date = (datetime.today() - timedelta(days=i * days_range)).strftime('%Y-%m-%d')
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')
        #print(end_date)
        #print(start_date)
        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        end_date2 = (datetime.today() - timedelta(days=i * days_range)).strftime('%Y-%m-%d')
        start_date2 = (datetime.strptime(end_date2,'%Y-%m-%d') - timedelta(days= days_range)).strftime('%Y-%m-%d')
        end_date2 = (datetime.strptime(end_date2,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

        stock_data2 = get_stock_data(stock_symbol, start_date2, end_date2)
        if len(stock_data) == 0:
            continue

        x = np.linspace(0, len(stock_data) - 1, len(stock_data))
        y = stock_data

        poly = least_squares_polynomial(x, y, get_degree(days_range))
        trend, strength = evaluate_trend(poly, x)

        #print(stock_data2[-1], stock_data[-1])
        if stock_data2[-1] > stock_data[0] and trend == "Up":
            correct_trend += 1
        elif stock_data2[-1] < stock_data[0] and trend == "Down":
            correct_trend += 1
        else:
            incorrect_trend += 1

    if correct_trend + incorrect_trend > 0:
        correct_trend_rate = correct_trend / (correct_trend + incorrect_trend)
    else:
        correct_trend_rate = 1.0

    print(f"Correct trend rate: {correct_trend_rate:.2f}")
    print(f"Correct trend predictions: {correct_trend}")
    print(f"Incorrect trend predictions: {incorrect_trend}")
    return correct_trend_rate


main()
