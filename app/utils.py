#utils.py
from yahooquery import search
from app.logger import logger
from typing import Union, List

ACRONYM_GROUPS = {
    "FAANG": ["META", "AAPL", "AMZN", "NFLX", "GOOG"],
    "FAAMG": ["FB", "AAPL", "AMZN", "MSFT", "GOOG"],
    "MAMAA": ["META", "AAPL", "MSFT", "AMZN", "GOOG"],
    "ANTMAMA": ["AAPL", "NVDA", "TSLA", "META", "AMZN", "MSFT", "GOOG"],
    "GAFM": ["GOOG", "AMZN", "FB", "MSFT"]
}

def resolve_ticker(company_name: str) -> Union[str, List[str]]:
    """
    Resolve a company name or acronym group to its stock ticker symbol(s) using yahooquery.
    """
    company_upper = company_name.strip().upper()
    if company_upper in ACRONYM_GROUPS:
        logger.info(f"Resolved acronym group {company_upper} to tickers: {ACRONYM_GROUPS[company_upper]}")
        return ACRONYM_GROUPS[company_upper]

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