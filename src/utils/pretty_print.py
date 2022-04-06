import pandas as pd


def print_sample_df(df, total_lines=5):
    return print(df.head(total_lines).to_markdown())
