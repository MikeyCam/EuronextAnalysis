import pandas as pd
import yfinance as yf
from typing import List, Optional
from ignore_SSL_errors import no_ssl_verification
pd.options.display.float_format = '{:.2f}'.format


def get_yahoo_data(ticker_and_isin: List[str]) -> Optional[pd.DataFrame]:
    with no_ssl_verification():
        yahoo_code = ticker_and_isin[0]
        stock_isin = ticker_and_isin[1]
        try:
            ticker = yf.Ticker(yahoo_code)
        except:
            ticker = None
        # Get some basic stock info
        try:
            stock_info = ticker.info
        except:
            stock_info = None
        try:
            yahoo_sector = stock_info['sector']
        except:
            yahoo_sector = None
        try:
            yahoo_industry = stock_info['industry']
        except:
            yahoo_industry = None
        try:
            yahoo_full_time_employees = stock_info['fullTimeEmployees']
        except:
            yahoo_full_time_employees = None
        try:
            yahoo_shares_outstanding = stock_info['sharesOutstanding']
        except:
            yahoo_shares_outstanding = None
        if yahoo_sector or yahoo_industry or yahoo_full_time_employees or yahoo_shares_outstanding:
            stock_info_dict = {
                'stock_isin': stock_isin,
                'yahoo_sector': [yahoo_sector],
                'yahoo_industry': [yahoo_industry],
                'yahoo_full_time_employees': [yahoo_full_time_employees],
                'yahoo_shares_outstanding': [yahoo_shares_outstanding]
            }
            stock_info = pd.DataFrame.from_dict(stock_info_dict)
        else:
            stock_info = pd.DataFrame()
        try:
            # Get the return history
            prices = ticker.history(period="5y")
            renaming_dict = {
                'Date': 'date',
                'Open': 'open_price',
                'High': 'high_price',
                'Low': 'low_price',
                'Close': 'close_price',
                'Adj Close': 'adjusted_close_price',
                'Volume': 'trading_volume',
                'Dividends': 'dividends',
                'Stock Splits': 'stock_splits',
            }
            prices.reset_index(inplace=True)
            prices.rename(columns=renaming_dict, inplace=True)
            prices['stock_isin'] = stock_isin
        except:
            prices = pd.DataFrame()
        # Get financial statement history
        try:
            financials = ticker.financials
            financials.index.set_names(
                ['financial_statement_measure'], inplace=True)
            financials.reset_index(inplace=True)
            financials = pd.melt(financials, id_vars='financial_statement_measure',
                                 var_name='date', value_name='amount')
            financials['stock_isin'] = stock_isin
        except:
            financials = pd.DataFrame()
        # Get earnings history
        try:
            earnings = ticker.earnings
            earnings.index.set_names(['year'], inplace=True)
            earnings.reset_index(inplace=True)
            earnings = pd.melt(earnings, id_vars='year',
                               var_name='earnings_measure', value_name='amount')
            earnings['stock_isin'] = stock_isin
        except:
            earnings = pd.DataFrame()
        # Get balance sheet history
        try:
            balance_sheet = ticker.balance_sheet
            balance_sheet.index.set_names(
                ['balance_sheet_measure'], inplace=True)
            balance_sheet.reset_index(inplace=True)
            balance_sheet = pd.melt(balance_sheet, id_vars='balance_sheet_measure',
                                    var_name='date', value_name='amount')
            balance_sheet['stock_isin'] = stock_isin
        except:
            balance_sheet = pd.DataFrame()
        # Get cashflow history
        try:
            cashflow = ticker.cashflow
            cashflow.index.set_names(['cash_flow_measure'], inplace=True)
            cashflow.reset_index(inplace=True)
            cashflow = pd.melt(cashflow, id_vars='cash_flow_measure',
                               var_name='date', value_name='amount')
            cashflow['stock_isin'] = stock_isin
        except:
            cashflow = pd.DataFrame()
    return stock_info, prices, financials, earnings, balance_sheet, cashflow


# # Test by extracting Apple stock returns
# stock_info, prices, financials, earnings, balance_sheet, cashflow = get_yahoo_data([
#                                                                                    'AAPL', 'US0378331005'])
# print('Stock info:')
# print(stock_info.head().to_markdown())
# print('----------------------------------------------------------')
# print('Historical prices:')
# print(prices.head().to_markdown())
# print('----------------------------------------------------------')
# print('Historical financials:')
# print(financials.head().to_markdown())
# print('----------------------------------------------------------')
# print('Historical earnings:')
# print(earnings.head().to_markdown())
# print('----------------------------------------------------------')
# print('Historical balance sheet:')
# print(balance_sheet.head().to_markdown())
# print('----------------------------------------------------------')
# print('Historical cashflow:')
# print(cashflow.head().to_markdown())
# print('----------------------------------------------------------')
