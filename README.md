# Analyzing Stocks via AI Agent

### Problem Statement: API-Driven AI Stock Analysis Agent

*Develop a ```FastAPI-based backend``` that serves as an autonomous AI agent for stock analysis. The agent will retrieve historical stock data using ```yFinance```, then leverage the ```OpenAI API``` to analyze the data and generate insights—such as trend analyses, anomaly detections, and predictive summaries. These insights will be exposed through ```dedicated API endpoints```, enabling seamless integration and programmatic access to the AI-generated stock analysis.*

## Project Structure
```bash
stock_analysis_ai/
│── app/
│   │── main.py                # FastAPI application entry point
│   │── services.py            # Fetching stock data using yFinance
│   │── ai_analysis.py         # AI-powered analysis using OpenAI API
│   │── config.py              # Configuration settings for API keys
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