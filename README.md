# StockTrendFinder440

This code performs a stock trend analysis using historical stock price data. It uses the yfinance library to retrieve stock data from Yahoo Finance and utilizes various mathematical and statistical techniques to evaluate the trend and strength of the stock.

## Prerequisites

Before running the code, ensure that you have the following libraries installed:

- numpy
- matplotlib
- yfinance

You can install these libraries using pip: `pip install numpy matplotlib yfinance`

## How to Use

Import the required libraries and run the main() function. 

Follow the prompts in the command line interface to input the required information. The main functions includes:

Input the stock symbol and range of days to analyze. 
Optionally, enter additional settings for more customized analysis. 
Retrieve the stock data for the specified symbol and date range. 
Perform polynomial fitting and evaluate the trend.
Generate plots to visualize the actual prices, polynomial trend line, and tangent line.
If additional options are specified, perform backtesting and calculate accuracy metrics.

The main function calls a few other functions as descibed.

`get_degree(days_range)`: Returns the degree of the polynomial based on the given range of days.

`get_stock_data(stock_symbol, start_date, end_date)`: Retrieves the stock data for a given symbol and date range.

`least_squares_polynomial(x, y, degree)`: Performs least squares polynomial fitting on the data points.

`tangent_line(strength, x, y_intercept)`: Calculates the tangent line based on the strength and intercept values.

`evaluate_trend(poly, x`): Evaluates the trend and strength based on the polynomial and data points.

`back_test(stock_symbol, days_range, test_back=1, prediction_date=1)`: Performs backtesting on the stock data.

## Output

The code generates a plot showing the stock price trend along with the least squares polynomial trend line and the tangent line. 
The plot also includes a title with information about the trend, its strength, and the accuracy of the trend prediction. 
If additional options are provided, the accuracy metrics from the backtesting are also displayed.
