from yahooquery import search
from app.logger import logger

def resolve_ticker(company_name: str) -> str:
    """
    Resolve a company name to its stock ticker symbol using yahooquery.
    """
    logger.info(f"Resolving ticker for: {company_name}")
    try:
        results = search(company_name)
        quotes = results.get("quotes", [])

        if quotes:
            symbol = quotes[0]["symbol"]  # Get the first match
            logger.info(f"Resolved ticker: {symbol}")
            return symbol

        raise ValueError(f"No ticker found for {company_name}")
    except Exception as e:
        logger.error(f"Error resolving ticker for {company_name}: {e}")
        raise