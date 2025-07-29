# process_data.py

import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert date to datetime object
    df['date'] = pd.to_datetime(df['date'], utc=True)

    # Optional: Remove duplicates (if any)
    df = df.drop_duplicates(subset=['symbol', 'exchange', 'date'])

    # Fill or drop missing values if applicable
    df = df.fillna(0)

    # Reorder columns to match DB schema (optional)
    columns_order = [
        'symbol', 'exchange', 'date', 'open', 'high', 'low', 'close', 'volume', 
        'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume', 
        'split_factor', 'dividend'
    ]
    df = df[columns_order]

    return df
