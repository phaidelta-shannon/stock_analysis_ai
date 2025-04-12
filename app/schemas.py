from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class QueryRequest(BaseModel):
    query: str

class StockDateRange(BaseModel):
    symbol: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class StockDataResponse(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    stock_data: Dict[str, Dict]
    ai_insights: str

class FundamentalsResponse(BaseModel):
    symbol: str
    stock_fundamentals: Dict[str, Optional[float]]

class AnalystRecommendationsResponse(BaseModel):
    symbol: str
    recommendations: List[Dict[str, Any]]

class AIStockQuery(BaseModel):
    query: str

class StockNewsResponse(BaseModel):
    symbol: str
    news: List[Dict[str, Any]]
    sentiment_analysis: Optional[Dict[str, float]] = None