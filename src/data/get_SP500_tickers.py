import pandas as pd

def download_tickers():
  payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  df = payload[0]
  name_mappings = {
          'Security': 'stock_name',
          'CIK': 'stock_isin',
          'Symbol': 'stock_ticker',
          'GICS Sector': 'stock_markets'
      }
  df.rename(columns=name_mappings, inplace=True)
  df = df.drop_duplicates(['stock_isin'], keep='first')
  return df[['stock_name', 'stock_isin', 'stock_ticker', 'stock_markets']]

# df = download_tickers()
# print(df.head().to_markdown())