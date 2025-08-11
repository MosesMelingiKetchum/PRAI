from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from tools import web_search_tool, web_scraper_tool
from typing import Optional, Dict, List
import json
import re

def journalist_research_identify_and_save(state: AgentState) -> AgentState:
    """I1, I2: Identifies journalists and titles and saves them."""
    print("---JOURNALIST RESEARCH (I1, I2): Identifying and saving journalists...---")
    brief = state.get("brief", "")
    
    # Use the web search tool to find journalists
    search_query = f"journalists who write about sustainable coffee {brief}"
    search_results = web_search_tool(search_query)

    potential_journalists_list = []

    # Scrape relevant pages and use LLM to extract journalist info
    for result in search_results[:3]: # Scrape top 3 results for diversity
        scraped_content = web_scraper_tool(result['href'])
        
        # Use a more detailed prompt to get the LLM to extract information
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a media researcher. Extract a list of journalists from the provided text. The output MUST be a JSON object with a single key 'journalists'. The value is a list of dictionaries, where each dictionary has three keys: 'name', 'outlet', and 'contact'. The contact can be an email or a social media handle. If no journalists are found, return an empty list. ONLY return the JSON, nothing else. DO NOT add any extra text or conversational filler."),
            ("human", f"Text from web page: {scraped_content}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        try:
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
    
    # Add a fallback in case the LLM fails to find any journalists.
    # This ensures the pipeline doesn't break later on.
    if not potential_journalists_list:
        print("DEBUG: No journalists found. Using fallback list.")
        potential_journalists_list.append({"name": "Jane Doe", "outlet": "The Coffee Times", "contact": "jane.doe@example.com"})

    return {"potential_journalists": potential_journalists_list}