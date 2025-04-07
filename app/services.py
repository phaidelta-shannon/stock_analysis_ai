import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from app.logger import logger

def fetch_stock_data(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    
    if not start_date or not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    
    logger.info(f"Fetching stock data for {symbol} from {start_date} to {end_date}")
    
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            logger.warning(f"No data found for {symbol} between {start_date} and {end_date}")
            return {"error": f"No data found for {symbol} from {start_date} to {end_date}."}

        stock_data = {
            str(date): row.to_dict()
            for date, row in data[['Open', 'High', 'Low', 'Close', 'Volume']].iterrows()
        }

        logger.info(f"Fetched {len(stock_data)} records for {symbol}")
        return stock_data

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}")

def fetch_stock_fundamentals(symbol: str) -> pd.DataFrame:
    logger.info(f"Fetching fundamentals for {symbol}")
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
            logger.warning(f"No fundamentals found for {symbol}")
            return {"error": f"No fundamentals found for {symbol}."}

        logger.info(f"Fetched fundamentals for {symbol}")
        return fundamentals

    except Exception as e:
        logger.error(f"Error fetching fundamentals for {symbol}: {e}")
        raise ValueError(f"Error fetching fundamentals for {symbol}: {str(e)}")
