import yfinance as yf

def fetch_stock_data(symbol: str, start_date: str, end_date:str):
    """
    Fetch historical stock data for a given symbol within a specified date range.
    """
    
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            return {"error": "No data found for the given time period."}
        
        # Convert Timestamp index to string
        stock_data = {
            str(date): row.to_dict()
            for date, row in data[['Open','High','Low','Close','Volume']].iterrows()
        }
        return stock_data
    
    except Exception as e:
        return {"error": str(e)}