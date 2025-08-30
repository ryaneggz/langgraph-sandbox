import os
from typing import List
from exa_py import Exa
from markitdown import MarkItDown
from ratelimit import limits, sleep_and_retry

md = MarkItDown(enable_plugins=False)

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

def web_scrape(urls: List[str]) -> str:
    """Retrieve content from a list of URLs or Paths"""
    docs = []
    for url in urls:
        document = md.convert(url)
        if document.title:
            formatted_output = f"# {document.title}\n\n{document.markdown}"
        else:
            formatted_output = document.markdown
        docs.append(formatted_output)
    return "\n\n---\n\n".join(docs)