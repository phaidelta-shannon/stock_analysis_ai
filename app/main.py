from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from app.services import fetch_stock_data, fetch_stock_fundamentals
from app.ai_analysis import analyze_stock_trends, ai_process_query
from app.logger import logger

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the AI Stock Analysis API"}

@app.get("/get_stock_analysis/")
def get_stock_analysis(
    symbol: str,
    start_date: str = Query(None, regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Query(None, regex="^\d{4}-\d{2}-\d{2}$")
):
    """
    Fetch stock data manually via query parameters and analyze trends.
    Dates are optional; if missing, the service sets them to the last 2 days.
    """
    logger.info(f"GET /get_stock_analysis/ - {symbol} from {start_date} to {end_date}")
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    if "error" in stock_data:
        return stock_data
    
    ai_insights = analyze_stock_trends(stock_data)
    return {
        "symbol": symbol,
        "start_date": start_date or "Auto-set by service",
        "end_date": end_date or "Auto-set by service",
        "stock_data": stock_data,
        "ai_insights": ai_insights
    }

@app.post("/ai_stock_analysis/")
async def ai_stock_analysis(request: QueryRequest):
    """
    AI-driven stock analysis. AI decides whether to fetch stock data or resolve tickers.
    """
    logger.info(f"POST /ai_stock_analysis/ - query: {request.query}")
    result = ai_process_query(request.query)
    return result

@app.get("/get_stock_fundamentals/")
def get_stock_fundamentals(symbol: str):
    logger.info(f"GET /get_stock_fundamentals/ - symbol: {symbol}")
    return fetch_stock_fundamentals(symbol)