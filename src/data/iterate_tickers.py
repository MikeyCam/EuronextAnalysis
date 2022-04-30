import concurrent.futures
from extract_yahoo_data import get_yahoo_data


# Define function to run through all the ticker codes and extract price data
# https://docs.python.org/3/library/concurrent.futures.html
def iterate_tickers(isin_and_ticker_df):
    relevant_tickers = isin_and_ticker_df[[
        'stock_ticker', 'stock_isin']].dropna()
    tickers = relevant_tickers.to_numpy().tolist()
    stock_info_list, prices_list, financials_list, earnings_list, balance_sheet_list, cashflow_list = (
        list() for i in range(6))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its ticker and ISN number
        download_ticker_info = {executor.submit(
            get_yahoo_data, ticker_and_isn): ticker_and_isn for ticker_and_isn in tickers}
        for future in concurrent.futures.as_completed(download_ticker_info):
            current_download = download_ticker_info[future]
            stock_info, prices, financials, earnings, balance_sheet, cashflow = future.result()
            stock_info_list.append(stock_info)
            prices_list.append(prices)
            financials_list.append(financials)
            earnings_list.append(earnings)
            balance_sheet_list.append(balance_sheet)
            cashflow_list.append(cashflow)
            # Check mark \u2713 cross mark \u2717
            # Retrieval status
            SI = '\u2717' if stock_info.empty else '\u2713'
            F = '\u2717' if financials.empty else '\u2713'
            E = '\u2717' if earnings.empty else '\u2713'
            BS = '\u2717' if balance_sheet.empty else '\u2713'
            CF = '\u2717' if cashflow.empty else '\u2713'
            print(f'{current_download}: SI{SI},F{F},E{E},BS{BS},CF{CF}')
    return stock_info_list, prices_list, financials_list, earnings_list, balance_sheet_list, cashflow_list
