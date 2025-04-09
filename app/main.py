from fastapi import FastAPI, Query
from app.schemas import QueryRequest, StockDateRange, StockDataResponse, FundamentalsResponse
from app.services import fetch_stock_data, fetch_stock_fundamentals
from app.ai_analysis import analyze_stock_trends, ai_process_query
from app.logger import logger

app = FastAPI()

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the AI Stock Analysis API"}

@app.get("/get_stock_analysis/", response_model=StockDataResponse)
def get_stock_analysis(symbol: str, start_date: str = Query(None), end_date: str = Query(None)):
    logger.info(f"GET /get_stock_analysis/ - {symbol} from {start_date} to {end_date}")
    stock_data = fetch_stock_data(symbol, start_date, end_date)
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
    query = request.query
    logger.info(f"POST /ai_stock_analysis/ - query: {query}")
    result = await ai_process_query(query)
    return result

@app.get("/get_stock_fundamentals/", response_model=FundamentalsResponse)
def get_stock_fundamentals(symbol: str):
    logger.info(f"GET /get_stock_fundamentals/ - symbol: {symbol}")
    return {
        "symbol": symbol,
        "stock_fundamentals": fetch_stock_fundamentals(symbol)
    }