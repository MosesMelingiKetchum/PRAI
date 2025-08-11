from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
import re
from typing import List, Dict

# Web Search Tool
def web_search_tool(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Performs a web search and returns a list of results."""
    print(f"DEBUG: Performing web search for query: {query}")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(keywords=query, region='wt-en', safesearch='off', max_results=num_results)]
    
    # Return a list of dictionaries with title, href, and body
    return results if results else []

# Web Scraper Tool
def web_scraper_tool(url: str) -> str:
    """Scrapes the text content from a given URL."""
    print(f"DEBUG: Scraping content from URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from the body and remove script/style tags
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()
            
        text = soup.get_text()
        
        # Clean up whitespace and newlines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit the text to a reasonable size to avoid large token usage
        return text[:4000]
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL {url}: {e}")
        return ""