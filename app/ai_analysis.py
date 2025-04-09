# ai_analysis.py
import json
from openai import OpenAI
from app.config import OPEN_API_KEY
from app.utils import resolve_ticker
from app.services import fetch_stock_data, fetch_stock_fundamentals, fetch_analyst_recommendations
from app.logger import logger

client = OpenAI(api_key=OPEN_API_KEY)

# Tools for OpenAI function calling
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
                    "symbol": {"type": "string"},
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"}
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
                    "symbol": {"type": "string"}
                },
                "required": ["symbol"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_analyst_recommendations",
            "description": "Fetch the latest analyst recommendations for a given ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"}
                },
                "required": ["symbol"]
            },
        }
    }
]

def analyze_stock_trends(stock_data):
    logger.info("Generating AI stock trend analysis")
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
        logger.info("AI analysis complete")
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        return f"Error generating insights: {str(e)}"


async def ai_process_query(query: str):
    logger.info(f"AI processing query: {query}")

    system_prompt = (
        "You are a helpful stock analysis assistant. "
        "Resolve company names to tickers, fetch stock data, fundamentals, or analyst recommendations based on user input. "
        "Call only the necessary tool based on the user's request."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    tool_outputs = {}

    try:
        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if not tool_calls:
                final_content = response_message.content
                logger.info("AI final response constructed")
                tool_outputs["ai_summary"] = final_content
                return tool_outputs

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                parameters = json.loads(tool_call.function.arguments)
                logger.info(f"AI chose tool: {function_name} with params: {parameters}")

                if function_name == "resolve_ticker":
                    symbol = resolve_ticker(parameters["company_name"])
                    tool_outputs["symbol"] = symbol
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps({"symbol": symbol})
                    })

                elif function_name == "fetch_stock_data":
                    symbol = parameters["symbol"]
                    start_date = parameters.get("start_date")
                    end_date = parameters.get("end_date")
                    stock_data = fetch_stock_data(symbol, start_date, end_date)
                    ai_insights = analyze_stock_trends(stock_data)
                    tool_outputs.update({
                        "symbol": symbol,
                        "stock_data": stock_data,
                        "ai_insights": ai_insights
                    })
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps({"symbol": symbol, "stock_data": stock_data, "ai_insights": ai_insights})
                    })

                elif function_name == "fetch_stock_fundamentals":
                    symbol = parameters["symbol"]
                    fundamentals = fetch_stock_fundamentals(symbol)
                    tool_outputs.update({"symbol": symbol, "stock_fundamentals": fundamentals})
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps({"symbol": symbol, "stock_fundamentals": fundamentals})
                    })

                elif function_name == "fetch_analyst_recommendations":
                    symbol = parameters["symbol"]
                    recommendations = fetch_analyst_recommendations(symbol)
                    tool_outputs.update({"symbol": symbol, "recommendations": recommendations})
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps({"symbol": symbol, "recommendations": recommendations})
                    })

    except Exception as e:
        logger.error(f"AI process failed: {e}")
        return {"error": str(e)}