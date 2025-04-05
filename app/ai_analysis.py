import json
from openai import OpenAI
from app.config import OPEN_API_KEY
from app.utils import resolve_ticker
from app.services import fetch_stock_data, fetch_stock_fundamentals

client = OpenAI(api_key=OPEN_API_KEY)

# Define OpenAI tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "resolve_ticker",
            "description": "Convert a company name to its stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The full company name (e.g., 'Microsoft')."
                    }
                },
                "required": ["company_name"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_stock_data",
            "description": "Fetch stock price data for a given ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock ticker symbol (e.g., 'MSFT')."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date for the stock data (YYYY-MM-DD)."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date for the stock data (YYYY-MM-DD)."
                    }
                },
                "required": ["symbol"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_stock_fundamentals",
            "description": "Fetch stock fundamentals like Market Cap, P/E Ratio, and Dividend Yield.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "The stock ticker symbol (e.g., 'MSFT')."}
                },
                "required": ["symbol"]
            },
        }
    }
]


def analyze_stock_trends(stock_data):
    """
    Uses OpenAI API to generate insights on stock trends based on historical data.
    """
    stock_json = json.dumps(stock_data, indent=2)

    system_prompt = "You are a helpful stock analysis assistant."

    prompt = f"""
    You are a financial analyst. Analyze the following stock data and provide a summary:
    - Key price trends
    - Notable fluctuations or anomalies
    - Possible reasons behind changes

    Stock Data:
    {stock_json}

    Provide a concise, human-readable analysis.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def ai_process_query(query: str):
    """
    Uses OpenAI to determine the required actions: resolving a ticker, fetching stock data,
    stock fundamentals, or a combination.
    """

    system_prompt = (
        "You are a helpful stock analysis assistant. "
        "If a company name is given, resolve it to a ticker. "
        # "If a ticker or company name related to stock analysis is given, fetch stock data and provide an AI-driven analysis."
        "Resolve company names to tickers, fetch stock data, fundamentals, or analyst recommendations based on user input. "
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            tools=tools,
            tool_choice="auto",
        )

        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            parameters = json.loads(tool_call.function.arguments)

            if function_name == "resolve_ticker":
                company_name = parameters["company_name"]
                symbol = resolve_ticker(company_name)  # Resolve ticker
                start_date = parameters.get("start_date")
                end_date = parameters.get("end_date")
                stock_data = fetch_stock_data(symbol, start_date, end_date)
                ai_insights = analyze_stock_trends(stock_data)
                stock_fundamentals = fetch_stock_fundamentals(symbol)
                
                return {
                    "symbol": symbol,
                    "stock_data": stock_data,
                    "stock_fundamentals": stock_fundamentals,
                    "ai_insights": ai_insights
                }

            if function_name == "fetch_stock_data":
                company_name = parameters["company_name"]
                symbol = resolve_ticker(company_name)
                start_date = parameters.get("start_date")
                end_date = parameters.get("end_date")

                stock_data = fetch_stock_data(symbol, start_date, end_date)
                ai_insights = analyze_stock_trends(stock_data)
                stock_fundamentals = fetch_stock_fundamentals(symbol)

                return {
                    "symbol": symbol,
                    "stock_data": stock_data,
                    "stock_fundamentals": stock_fundamentals,
                    "ai_insights": ai_insights
                }
            
            if function_name == "fetch_stock_fundamentals":
                company_name = parameters["company_name"]
                symbol = resolve_ticker(company_name)
                stock_fundamentals = fetch_stock_fundamentals(symbol)

                return {
                    "symbol": symbol,
                    "stock_fundamentals": stock_fundamentals
                }

        return {"message": "No relevant function was called."}

    except Exception as e:
        return {"error": str(e)}