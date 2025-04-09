# Analyzing Stocks via AI Agent

### Problem Statement: API-Driven AI Stock Analysis Agent

*Develop a ```FastAPI-based backend``` that serves as an autonomous AI agent for stock analysis. The agent will retrieve historical stock data using ```yFinance``` and resolve company names or acronyms to ticker symbols using ```yahooquery```. It will then leverage the ```OpenAI API``` to analyze the data and generate insights—such as trend analyses, anomaly detections, and predictive summaries. These insights will be exposed through ```dedicated API endpoints```, enabling seamless integration and programmatic access to the AI-generated stock analysis.*

## Project Structure
```bash
stock_analysis_ai/
│── app/
│   │── main.py                # FastAPI application entry point
│   │── services.py            # Fetching stock data using yFinance
│   │── ai_analysis.py         # AI-powered analysis using OpenAI API
│   │── config.py              # Configuration settings for API 
keys
│   ├── logger.py              # Logger setup
│   ├── schemas.py             # Pydantic model setup
│   │__ utils.py               # Resolving ticker symbol from user query
│── venv/                      # Virtual environment
│── requirements.txt           # Dependencies for installation
│── .env                       # Environment variables (API keys)
│── .gitignore
│── README.md
```

## 1️⃣ Install Dependencies
Install the dependencies from the ```requirements.txt``` file:
```python
pip install -r requirements.txt
```
## 2️⃣ Configure API Keys
Create a ```.env``` file to store your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key
```
## 3️⃣ Run the API Server
Start the FastAPI server with:
```python
uvicorn app.main:app --reload
```
## 4️⃣ Test API Endpoints
The application exposes two endpoints for stock analysis:

## Endpoint 1: `/get_stock_analysis/`

Fetch stock data manually by providing the stock symbol and an optional date range.

Request Example:
```
http://127.0.0.1:8000/get_stock_analysis/?symbol=MSFT&start_date=2024-01-01&end_date=2024-03-01
```
## ✅ Expected API Response
```json
{
    "symbol": "MSFT",
    "start_date": "2024-01-01",
    "end_date": "2024-03-01",
    "stock_data": {
        "2024-01-01": {"Open": 345.50, "High": 350.00, "Low": 344.00, "Close": 348.50, "Volume": 2000000},
        "2024-01-15": {"Open": 355.20, "High": 360.00, "Low": 353.00, "Close": 358.10, "Volume": 1800000}
    },
    "ai_insights": "Microsoft's stock price increased by 5% over the selected period, showing a strong uptrend with high volatility. A sharp drop was observed on February 10, likely due to earnings report expectations."
}
```

## Endpoint 2: `/ai_stock_analysis/`
AI-driven stock analysis. The AI will either resolve a company name to a ticker symbol and fetch the stock data, or directly analyze data if a ticker is provided.

Example Request:
```
POST http://127.0.0.1:8000/ai_stock_analysis/
Content-Type: application/json
Body:
{
    "query": "Microsoft stock analysis"
}
```
## ✅ Expected Response
```json
{
    "symbol": "MSFT",
    "stock_data": {
        "2025-03-31": {"Open": 372.54, "High": 377.07, "Low": 367.24, "Close": 375.39, "Volume": 35158100}
    },
    "ai_insights": "Microsoft's stock saw a steady rise during the last two days, indicating strong bullish sentiment in the market."
}
```

## Notes

- If the query contains a company name, the AI will resolve it to the corresponding ticker symbol and fetch the stock data for analysis.

- If the query contains an existing stock ticker (e.g., MSFT), the AI will directly analyze the stock trends.