#utils.py
from yahooquery import search
from app.logger import logger
from typing import Union, List
from difflib import get_close_matches

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
    Returns ticker symbol(s) or raises ValueError with suggestion if possible.
    """
    company_upper = company_name.strip().upper()
    
    # First check if it's a known acronym group
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
        
        # If no exact match found, try to suggest similar tickers
        all_possible_symbols = []
        for group in ACRONYM_GROUPS.values():
            all_possible_symbols.extend(group)
        
        for quote in quotes:
            if 'symbol' in quote:
                all_possible_symbols.append(quote['symbol'])
        
        # Find closest match (minimum similarity: 60%)
        suggestions = get_close_matches(company_upper, all_possible_symbols, n=1, cutoff=0.6)
        
        if suggestions:
            error_msg = f"No ticker found for '{company_name}'. Did you mean '{suggestions[0]}'?"
            logger.warning(f"Ticker resolution failed with suggestion: {error_msg}")
            raise ValueError(error_msg)
        else:
            error_msg = f"No ticker found for '{company_name}'. Please check the company name."
            logger.warning(f"Ticker resolution failed: {error_msg}")
            raise ValueError(error_msg)
        
    except Exception as e:
        logger.error(f"Error resolving ticker for {company_name}: {e}")
        raise ValueError(f"Could not process request for '{company_name}'. Please try again.")