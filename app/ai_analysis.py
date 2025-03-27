import json
from openai import OpenAI
from app.config import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)

def analyze_stock_trends(stock_data):
    """
    Uses OpenAI API to generate insights on stock trends based on historical data.
    """
    stock_json = json.dumps(stock_data, indent=2)

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
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"