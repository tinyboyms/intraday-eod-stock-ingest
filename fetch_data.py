import requests
import pandas as pd
from config import API_URL, ACCESS_KEY

def fetch_stock_data(symbols=None, limit=100, offset=0):
    """
    Fetch EOD stock data from Marketstack API
    Note: Marketstack API requires at least one symbol to be specified
    
    Args:
        symbols: List of stock symbols or comma-separated string (required by API)
        limit: Number of records to fetch (default: 100, max: 1000 for free plan)
        offset: Pagination offset
    """
    
    # Check if API key is available
    if not ACCESS_KEY:
        raise ValueError("API key is not set. Check your .env file and MARKETSTACK_API_KEY variable.")
    
    # Default symbols if none provided (popular stocks)
    if symbols is None:
        symbols = 'AAPL,MSFT,GOOGL,AMZN,TSLA,META,NVDA,NFLX,CRM,ORCL'
    
    # Convert list to comma-separated string if needed
    if isinstance(symbols, list):
        symbols = ','.join(symbols)
    
    params = {
        'access_key': ACCESS_KEY,
        'symbols': symbols,
        'limit': limit,
        'offset': offset
    }
    
    print(f"Fetching EOD data for symbols: {symbols}")
    print(f"Limit: {limit}, Offset: {offset}")
    
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 422:
            print("422 Error details:")
            print("Response text:", response.text)
            print("Request URL:", response.url)
            try:
                error_json = response.json()
                print("Error JSON:", error_json)
            except:
                print("Could not parse error response as JSON")
            raise requests.exceptions.HTTPError(f"422 Client Error: {response.text}")
        
        if response.status_code == 401:
            print("401 Unauthorized - Check your API key")
            print("Response:", response.text)
            raise requests.exceptions.HTTPError("Invalid API key")
        
        if response.status_code == 429:
            print("429 Rate limit exceeded")
            print("Response:", response.text)
            raise requests.exceptions.HTTPError("Rate limit exceeded")
        
        response.raise_for_status()
        
        try:
            json_data = response.json()
        except ValueError as e:
            print("Failed to parse JSON response")
            print("Response content:", response.text[:500])
            raise ValueError(f"Invalid JSON response: {e}")
        
        # Check response structure
        print("Response keys:", list(json_data.keys()) if isinstance(json_data, dict) else "Not a dict")
        
        if 'error' in json_data:
            print("API returned error:", json_data['error'])
            raise ValueError(f"API Error: {json_data['error']}")
        
        # Check if data exists
        if 'data' not in json_data:
            print("No 'data' key in response")
            print("Full response:", json_data)
            return pd.DataFrame()
        
        raw_data = json_data.get('data', [])
        
        if not raw_data:
            print("No data returned from API")
            return pd.DataFrame()
        
        print(f"Successfully fetched {len(raw_data)} records")
        
        # Show sample of first record for debugging
        if raw_data:
            print("Sample record keys:", list(raw_data[0].keys()) if isinstance(raw_data[0], dict) else "First record is not a dict")
        
        df = pd.DataFrame(raw_data)
        return df
        
    except requests.exceptions.Timeout:
        print("Request timed out")
        raise
    except requests.exceptions.ConnectionError:
        print("Connection error - check your internet connection")
        raise
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Error type: {type(e)}")
        raise