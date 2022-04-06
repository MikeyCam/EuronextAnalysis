from data.process_euronext import import_euronext_file
from utils.pretty_print import print_sample_df

df = import_euronext_file()
print_sample_df(df)
