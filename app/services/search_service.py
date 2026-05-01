from duckduckgo_search import DDGS


import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _search_with_retry(query: str, max_results: int = 5) -> list[dict]:
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                if results:
                    return [{"title": r.get("title", ""), "body": r.get("body", "")} for r in results]
                else:
                    logger.warning(f"No results found for '{query}' on attempt {attempt + 1}")
        except Exception as e:
            logger.warning(f"Search attempt {attempt + 1} failed for '{query}': {e}")
        time.sleep(1)
    
    logger.error(f"All search attempts failed for '{query}'")
    return [{"title": "Live Data Unavailable", "body": f"Could not retrieve real-time web data for: {query}. Please use general industry knowledge."}]

def search_brand(brand_name: str, max_results: int = 5) -> list[dict]:
    return _search_with_retry(f"{brand_name} company overview business model", max_results)


def search_market(industry: str, max_results: int = 5) -> list[dict]:
    return _search_with_retry(f"{industry} market trends latest data", max_results)


def search_competitors(brand_name: str, industry: str, max_results: int = 5) -> list[dict]:
    return _search_with_retry(f"top competitors of {brand_name} in {industry}", max_results)


def search_pro(query: str, max_results: int = 5) -> list[dict]:
    # Professional search for industry reports, whitepapers, and investor decks
    pro_queries = [
        f"{query} industry report 2024 2025",
        f"{query} market analysis whitepaper",
        f"{query} investor presentation filetype:pdf",
        f"{query} key pain points and challenges"
    ]
    all_results = []
    for q in pro_queries[:2]: # limit to 2 pro queries to avoid rate limits
        all_results.extend(_search_with_retry(q, max_results=3))
    return all_results

def gather_research(brand_name: str, industry: str) -> str:
    brand_info = search_brand(brand_name)
    market_info = search_market(industry)
    competitor_info = search_competitors(brand_name, industry)
    pro_info = search_pro(industry)

    research = f"## Brand Research: {brand_name}\n"
    for item in brand_info:
        research += f"- {item['title']}: {item['body']}\n"

    research += f"\n## Market Trends & Pro Insights: {industry}\n"
    for item in pro_info + market_info:
        research += f"- {item['title']}: {item['body']}\n"

    research += f"\n## Competitive Landscape\n"
    for item in competitor_info:
        research += f"- {item['title']}: {item['body']}\n"

    return research
