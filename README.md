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
│   │── config.py              # Configuration settings for API keys
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

- If the query contains a **company name**, **stock ticker**, or **acronym** (e.g., *Microsoft*, *MSFT*, *FAANG*, *GAFAM*), the AI will resolve it to one or more corresponding ticker symbols using `yahooquery`.

- Acronyms like **FAANG** (Facebook, Apple, Amazon, Netflix, Google) are supported and automatically expanded into multiple tickers.

- If the query contains an **existing stock ticker**, the AI uses it directly without resolving.

- The AI autonomously decides which tools to invoke based on the user query, including:
  - `resolve_ticker`
  - `fetch_stock_data`
  - `fetch_stock_fundamentals`
  - `fetch_analyst_recommendations`
  - `fetch_stock_news`

- For **stock data**, you can optionally specify `start_date` and `end_date`. If not provided, it defaults to a recent short range (1–2 days).

- **Stock fundamentals** and **analyst recommendations** are independent of date ranges—they reflect the latest available snapshot.

- The system supports **multiple tickers** in one query (e.g., *"Get me the fundamentals for Microsoft and Tesla"*) and returns results per symbol.

- All AI-generated summaries and insights (*including news sentiment analysis - analyzes last 7 days of news sentiment*) are generated via the OpenAI API using real-time data retrieved from `yFinance`.

## 🔀 Try It Out 🔍

`Basic stock analysis`
> *Show me the recent trend for Apple stock*

`Fundamentals check`
> *What's the P/E ratio and market cap of Nvidia?*

`Multi-stock comparison`
> *Compare Tesla and Ford fundamentals*

`Analyst opinions`
> *What are analysts saying about Amazon stock?*

`Sentiment analysis`
> *How positive is the news about Microsoft?*

> *Show me bearish articles for Meta"*

`Mixed request`
> *Get price trends and news sentiment for AMD*

`Acronym expansion`
> *Analyze all FAANG stocks*

> *Get me GAFM fundamentals*