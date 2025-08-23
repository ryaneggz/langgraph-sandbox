import os
from exa_py import Exa
from ratelimit import limits, sleep_and_retry

@limits(calls=5, period=1)
@sleep_and_retry
def linkedin_search(
    query: str,
    num_results: int = 5,
):
    """Run a linkedin search"""
    exa = Exa(api_key = os.environ['EXA_API_KEY'])
    return exa.search_and_contents(
        query,
        text=True,
        num_results=num_results,
        type="auto",
        category="linkedin profile"
    )