# main.py
from dotenv import load_dotenv
load_dotenv()

from fetch_data import fetch_stock_data
from process_data import clean_data
from db import create_tables, get_session, StockData

def main():
    # Create table if does not exist
    create_tables()
    
    # Fetch data from API - specify the symbols you want
    # You can modify this list to include the stocks you're interested in
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Add your desired symbols here
    df = fetch_stock_data(symbols=symbols)
    
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
                date=row['date'].to_pydatetime() if hasattr(row['date'], 'to_pydatetime') else row['date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
                adj_open=row.get('adj_open'),
                adj_high=row.get('adj_high'),
                adj_low=row.get('adj_low'),
                adj_close=row.get('adj_close'),
                adj_volume=row.get('adj_volume'),
                split_factor=row.get('split_factor'),
                dividend=row.get('dividend')
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