# main.py
from dotenv import load_dotenv
load_dotenv()

from fetch_data import fetch_stock_data
from process_data import clean_data
from db import create_tables, get_session, StockData

def main():
    # Create table if does not exist
    create_tables()

    # Fetch data from API
    df = fetch_stock_data()

    # Clean data
    clean_df = clean_data(df)

    # Insert into DB
    session = get_session()
    try:
        # Convert DataFrame rows to ORM objects
        records = [
            StockData(
                symbol=row['symbol'],
                exchange=row['exchange'],
                date=row['date'].to_pydatetime(),
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                adj_open=row['adj_open'],
                adj_high=row['adj_high'],
                adj_low=row['adj_low'],
                adj_close=row['adj_close'],
                adj_volume=row['adj_volume'],
                split_factor=row['split_factor'],
                dividend=row['dividend']
            )
            for idx, row in clean_df.iterrows()
        ]

        session.bulk_save_objects(records)
        session.commit()
        print(f"Inserted {len(records)} records successfully.")

    except Exception as e:
        session.rollback()
        print("Error inserting records:", e)
    finally:
        session.close()

if __name__ == "__main__":
    main()
