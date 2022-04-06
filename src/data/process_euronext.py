from .import_csv import import_csv
from typing import List
import re
import string


def return_yahoo_city_code(input_text: str) -> str:
    # Create a mapping for the exchange cities to yahoo codes
    stock_exchange_markets_to_main_city_mapping = {
        'Amsterdam': 'AS',
        'Brussels': 'BR',
        'Dublin': 'IR',
        'Lisbon': 'LS',
        'Oslo': 'OL',
        'Paris': 'PA',
        'No city mentioned': 'NA'
    }
    cities_list = list(stock_exchange_markets_to_main_city_mapping.keys())
    split_word_list = re.sub(
        '[' + string.punctuation + ']', '', input_text).split()
    for word in split_word_list:
        if word in cities_list:
            result = word
            break
        else:
            result = "No city mentioned"
    return stock_exchange_markets_to_main_city_mapping[result]


def import_euronext_file():
    file_location = r"data\external\euronext_website_extraction.csv"
    name_mappings = {
        'Name': 'stock_name',
        'ISIN': 'stock_isin',
        'Symbol': 'stock_euronext_symbol',
        'Market': 'stock_exchange_markets',
        'Trading Currency': 'stock_trading_currency'
    }
    df = import_csv(file_location, name_mappings)
    # Correct special character is Oslo Bors if needed, might not be needed if you encoding is correct on the csv
    df['stock_exchange_markets'] = df['stock_exchange_markets'].str.replace(
        '�', 'ø')
    # Get the Yahoo city mapping
    df['yahoo_city_code'] = df['stock_exchange_markets'].apply(
        lambda x: return_yahoo_city_code(x))
    # Create the full city code
    df['yahoo_code'] = df['stock_euronext_symbol'].str.cat(
        df['yahoo_city_code'], sep='.')
    # Keep first occurence and remove other duplicates
    df = df.drop_duplicates(['stock_isin'], keep='first')
    return df
