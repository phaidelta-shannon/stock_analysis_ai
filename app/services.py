import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def fetch_stock_data(symbol: str, start_date: str = None, end_date:str = None) -> pd.DataFrame:
    """
    Fetch historical stock data for a given symbol within a specified date range.
    If no dates are provided, fetch data for the last 2 days.
    """
    
    if not start_date or not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            return {"error": f"No data found for {symbol} from {start_date} to {end_date}."}
        
        # Convert Timestamp index to string
        stock_data = {
            str(date): row.to_dict()
            for date, row in data[['Open','High','Low','Close','Volume']].iterrows()
        }
        return stock_data
    
    except Exception as e:
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}")