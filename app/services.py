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
    
def fetch_stock_fundamentals(symbol: str) -> pd.DataFrame:
    """
    Fetch key stock fundamentals such as market cap, P/E ratio, and dividend yield.
    """
    try:
        stock = yf.Ticker(symbol)
        fundamentals = {
            "Market Cap": stock.info.get("marketCap"),
            "P/E Ratio": stock.info.get("trailingPE"),
            "Dividend Yield": stock.info.get("dividendYield"),
            "EPS": stock.info.get("trailingEps"),
            "52 Week High": stock.info.get("fiftyTwoWeekHigh"),
            "52 Week Low": stock.info.get("fiftyTwoWeekLow")
        }

        if not fundamentals:
            return {"error": f"No fundamentals found for {symbol}."}
        
        return fundamentals
    except Exception as e:
        raise ValueError(f"Error fetching fundamentals for {symbol}: {str(e)}")