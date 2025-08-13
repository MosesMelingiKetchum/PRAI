from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from tools import web_search_tool, web_scraper_tool
from typing import Optional, Dict, List
import json
import re

def journalist_research_identify_and_save(state: AgentState) -> AgentState:
    """I1, I2: Identifies journalists and titles and saves them."""
    print("---JOURNALIST RESEARCH (I1, I2): Identifying and saving journalists...---")
    brief = state.get("brief", "")
    
    # Refined the search query to be more specific to coffee
    search_query = f"journalists who write about sustainable coffee and fair trade"
    search_results = web_search_tool(search_query)

    potential_journalists_list = []

    # Scrape relevant pages and use LLM to extract journalist info
    for result in search_results[:3]: # Scrape top 3 results for diversity
        try:
            scraped_content = web_scraper_tool(result['href'])
            
            # Use a more detailed prompt to get the LLM to extract information
            # Added a critical instruction to filter for relevance.
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a media researcher. Extract a list of journalists from the provided text who write about coffee, sustainability, or fair trade. The output MUST be a JSON object with a single key 'journalists'. The value is a list of dictionaries, where each dictionary has three keys: 'name', 'outlet', and 'contact'. The contact can be an email or a social media handle. If no journalists are found, return an empty list. ONLY return the JSON, nothing else. DO NOT add any extra text or conversational filler."),
                ("human", f"Text from web page: {scraped_content}")
            ])
            
            chain = prompt | llm | StrOutputParser()
            
            llm_response = chain.invoke({"scraped_content": scraped_content})
            
            # Use regex to find a clean JSON block in case the LLM adds extra text
            json_match = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
            if json_match:
                json_string = json_match.group(1)
            else:
                json_string = llm_response
            
            extracted_info = json.loads(json_string)
            potential_journalists_list.extend(extracted_info.get("journalists", []))
        except json.JSONDecodeError:
            print("DEBUG: Could not parse LLM response as JSON. Skipping this result.")
        except Exception as e:
            print(f"DEBUG: An unexpected error occurred: {e}. Skipping this result.")
    
    if not potential_journalists_list:
        print("DEBUG: No journalists found. The list will be empty.")

    return {"potential_journalists": potential_journalists_list}
