import pandas as pd
from get_euronext_tickers import import_euronext_file
from get_SP500_tickers import download_tickers
from iterate_tickers import iterate_tickers


def data_pipeline():
    # Gather all ticker symbols
    # Euronext stocks
    euro_stocks = import_euronext_file()
    euro_stocks.to_csv(
        'data/interim/euro_stocks.csv', sep='|', index=False)
    us_stocks = download_tickers()
    us_stocks.to_csv(
        'data/interim/us_stocks.csv', sep='|', index=False)
    # Loop through all tickers to acquire data
    stock_info_list, price_list, financials_list, earnings_list, balance_sheet_list, cashflow_list = iterate_tickers(
        us_stocks)
    # Yahoo stock info
    stock_info_yahoo = pd.concat(stock_info_list)
    stock_info_yahoo.to_csv(
        'data/raw/stock_info_yahoo.csv', sep='|', index=False)
    # Price history
    price_data = pd.concat(price_list)
    price_data.to_csv(
        'data/raw/price_yahoo.csv', sep='|', index=False)
    # Financials history
    financials_data = pd.concat(financials_list)
    financials_data.to_csv(
        'data/raw/financials_yahoo.csv', sep='|', index=False)
    # Earnings history
    earnings_data = pd.concat(earnings_list)
    earnings_data.to_csv(
        'data/raw/earnings_yahoo.csv', sep='|', index=False)
    # Balance sheet history
    balance_sheet__data = pd.concat(balance_sheet_list)
    balance_sheet__data.to_csv(
        'data/raw/balance_sheet_yahoo.csv', sep='|', index=False)
    # Cash flow history
    cashflow_data = pd.concat(cashflow_list)
    cashflow_data.to_csv(
        'data/raw/cashflow_yahoo.csv', sep='|', index=False)
