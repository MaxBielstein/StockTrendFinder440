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
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=True)
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
    test_back = 0
    stock_symbol = input("Enter the stock symbol: ").upper()
    days_range = int(input("Enter the range of days to look back (10-1000): "))
    more_options = input("Enter anything to be prompted with more settings: ")
    if more_options != "":
        test_back = int(input("Enter a number of days ago to start the test: "))
        prediction_date = int(input("enter how many days past the period you want to assess the accuracy of the trend from: "))

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

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(stock_data.index, stock_data, label="Actual Prices")
    ax.plot(stock_data.index, y_trend, label="Least Squares Polynomial")
    ax.plot(stock_data.index[(days_range // 3) + 1:], y_tangent[(days_range // 3) + 1:], label="Trend Line",
            linestyle="--")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    if more_options != "":
        correct_trend_rate, avg_strength, avg_incorrect_strength = back_test(stock_symbol, days_range, test_back, prediction_date)
    else:
        correct_trend_rate, avg_strength, avg_incorrect_strength = back_test(stock_symbol, days_range)

    ax.set_title(
        f"{stock_symbol} Stock Price Trend\nTrend: {trend}, Strength: {np.abs(strength):.2f}, Accuracy: {correct_trend_rate:.2f}, \n Avg Strength of Correct Predictions: {avg_strength:.2f}, Avg Strength of Incorrect Predictions: {avg_incorrect_strength:.2f}")

    ax.legend()
    fig.autofmt_xdate()
    plt.show()

def back_test(stock_symbol, days_range, test_back=1, prediction_date=1):
    correct_trend = 0
    incorrect_trend = 0
    correct_strengths = []
    incorrect_strengths = []

    for i in range(50):
        end_date = (datetime.today() - timedelta(days=i*5 +test_back)).strftime('%Y-%m-%d')
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')
        #print(end_date)
        #print(start_date)
        #print(start_date)
        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        end_date2 = (datetime.today() - timedelta(days=i*5 + test_back)).strftime('%Y-%m-%d')
        start_date2 = (datetime.strptime(end_date2,'%Y-%m-%d') - timedelta(days=days_range)).strftime('%Y-%m-%d')
        end_date2 = (datetime.strptime(end_date2,'%Y-%m-%d') + timedelta(days=prediction_date)).strftime('%Y-%m-%d')
        #print(start_date2)
        #print(end_date)
        #print(end_date2)
        stock_data2 = get_stock_data(stock_symbol, start_date2, end_date2)
        if len(stock_data) == 0:
            continue

        x = np.linspace(0, len(stock_data) - 1, len(stock_data))
        y = stock_data

        poly = least_squares_polynomial(x, y, get_degree(days_range))
        trend, strength = evaluate_trend(poly, x)

        if stock_data2[-1] > stock_data[-1] and trend == "Up":
            correct_trend += 1
            correct_strengths.append(abs(strength))
        elif stock_data2[-1] < stock_data[-1] and trend == "Down":
            correct_trend += 1
            correct_strengths.append(abs(strength))
        else:
            incorrect_trend += 1
            incorrect_strengths.append(abs(strength))

    if correct_trend + incorrect_trend > 0:
        correct_trend_rate = correct_trend / (correct_trend + incorrect_trend)
    else:
        correct_trend_rate = 1.0

    avg_strength = np.mean(correct_strengths) if correct_strengths else 0
    average_incorrect_strength = np.mean(incorrect_strengths) if incorrect_strengths else 0

    return correct_trend_rate, abs(avg_strength), abs(average_incorrect_strength)


main()
