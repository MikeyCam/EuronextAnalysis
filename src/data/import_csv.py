import pandas as pd
from typing import Dict, Optional


def import_csv(file_location: str, name_mappings: Dict) -> Optional[pd.DataFrame]:
    df = pd.read_csv(file_location, sep=';',
                     usecols=list(name_mappings.keys()))
    df.rename(columns=name_mappings, inplace=True)
    return df
