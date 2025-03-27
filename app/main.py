from fastapi import FastAPI, Query
from app.services import fetch_stock_data
from app.ai_analysis import analyze_stock_trends

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the AI Stock Analysis API"}

@app.get("/get_stock_analysis/")
def get_stock_analysis(
    symbol: str,
    start_date: str = Query(..., regex="^\d{4}-\d{2}-\d{2}$"),
    end_date: str = Query(..., regex="^\d{4}-\d{2}-\d{2}$")
):
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    if "error" in stock_data:
        return stock_data
    
    ai_insights = analyze_stock_trends(stock_data)
    return {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "stock_data": stock_data,
        "ai_insights": ai_insights
    }