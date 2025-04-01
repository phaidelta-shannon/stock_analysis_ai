from yahooquery import search

def resolve_ticker(company_name: str) -> str:
    """
    Resolve a company name to its stock ticker symbol using yahooquery.
    """
    try:
        results = search(company_name)
        quotes = results.get("quotes", [])

        if quotes:
            return quotes[0]["symbol"]  # Get the first match

        raise ValueError(f"No ticker found for {company_name}")
    except Exception as e:
        raise ValueError(f"Unable to resolve ticker for {company_name}: {str(e)}")