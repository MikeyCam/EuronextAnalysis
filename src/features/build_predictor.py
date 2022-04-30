# Import packages
import pandas as pd
import numpy as np
import datetime


def one_year_return(stock_isin, year_end, pricing_return_df, reporting_lag_period_days=90):
    year_end_formatted = datetime.datetime.strptime(year_end, '%Y-%m-%d')
    data_availability_start_date = year_end_formatted + \
        datetime.timedelta(days=reporting_lag_period_days)
    data_availability_end_date = data_availability_start_date + \
        datetime.timedelta(
            days=365)  # Can be improved to account for leap years
    filtered_isin = pricing_return_df[pricing_return_df['stock_isin'] == stock_isin]
    mask = (filtered_isin['date'] > data_availability_start_date) & (
        filtered_isin['date'] <= data_availability_end_date)
    try:
        filtered_dates = filtered_isin.loc[mask]
        one_year_holding_return = filtered_dates['daily_pct_change_plus_one'].prod(
        ) - 1
        trading_days = len(filtered_dates.index)
    except:
        one_year_holding_return = np.nan
    return one_year_holding_return, trading_days, data_availability_start_date, data_availability_end_date


def build_predictor(price_df, financials_df):
    # The rows that make up a distinct combination of stock_isin and date (year-end) will make up by full dataset
    df = financials_df.groupby(
        ['stock_isin', 'date']).size().reset_index().drop(columns=[0])
    df['financial_year_end'] = pd.to_datetime(df['date'])
    # I want to focus on total return which will include dividends, this means days that pay a dividend get a higher return
    price_df['close_price_plus_dividends'] = price_df['close_price'] + \
        price_df['dividends']
    # First I will sort by date for each unique ISIN and drop irrelevant columns
    price_df.sort_values(["stock_isin", "date"],
                         axis=0, ascending=True,
                         inplace=True)
    price_df = price_df[['stock_isin', 'date',
                         'close_price', 'dividends', 'close_price_plus_dividends']]
    price_df['date'] = pd.to_datetime(price_df['date'])
    # Calculate % change
    price_df['daily_pct_change'] = price_df['close_price'].pct_change()
    price_df['daily_pct_change_plus_one'] = price_df['daily_pct_change'] + 1
    # Add our predictor to our dataset
    df[['one_year_holding_return', 'trading_days', 'return_calc_start_date', 'return_calc_end_date']] = df.apply(lambda x: one_year_return(
        x['stock_isin'], x['date'], price_df), axis=1, result_type='expand')
    return df


financials_yahoo = pd.read_csv(r'data/raw/financials_yahoo.csv', sep='|')
price_yahoo = pd.read_csv(r'data/raw/price_yahoo.csv', sep='|')
df = build_predictor(price_yahoo, financials_yahoo)
df.to_csv(
    'data/processed/y.csv', sep='|', index=False)
# print(df.head(20).to_markdown())
