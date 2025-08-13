from ddgs import DDGS
from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import re
import random # We need to import random to select a user agent

# Web Search Tool
def web_search_tool(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Performs a web search and returns a list of results."""
    print(f"DEBUG: Performing web search for query: {query}")
    # Using the new DDGS package as recommended
    with DDGS() as ddgs:
        # Correcting the function call to pass the query as a positional argument
        results = [r for r in ddgs.text(query, region='wt-en', safesearch='off', max_results=num_results)]
    
    # Return a list of dictionaries with title, href, and body
    return results if results else []

# Web Scraper Tool
def web_scraper_tool(url: str) -> str:
    """
    Scrapes the text content from a given URL.
    Includes a random User-Agent header to avoid 403 Forbidden errors.
    """
    print(f"DEBUG: Scraping content from URL: {url}")
    
    # A list of common User-Agent strings to rotate through
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
    ]
    
    try:
        # Select a random User-Agent from the list for each request
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        response = requests.get(url, timeout=10, headers=headers)
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
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""
