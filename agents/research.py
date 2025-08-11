from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from tools import web_search_tool, web_scraper_tool
from typing import Optional, Dict, List, Any

# This node is responsible for coordinating the research pipeline. It receives the
# campaign plan and builds specific research tasks for the sub-agents.
def head_of_research_node(state: AgentState) -> AgentState:
    """D1, D2, D3: Receives brief, builds research tasks, and selects sub-agents."""
    print("---HEAD OF RESEARCH (D1, D2, D3): Building research tasks...---")
    plan = state.get("plan", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the head of a research team. Your task is to analyze the following campaign plan and create a list of detailed research tasks. Each task should be assigned to one of the following sub-agents: 'brand_research', 'media_scout', 'social_intel'. The output must be a JSON object with 'research_tasks' as the key, and a list of dictionaries as the value. Each dictionary must have 'agent' and 'task' keys."),
        ("human", f"Campaign Plan: {plan}")
    ])
    
    # We will use the structured output parser to ensure a valid JSON is returned
    chain = prompt | llm | StrOutputParser()
    research_tasks_json = chain.invoke({"plan": plan})
    
    # Placeholder for actual JSON parsing
    research_tasks = {
        "research_tasks": [
            {"agent": "brand_research", "task": "Research the latest trends in sustainable coffee and our company's market position."},
            {"agent": "media_scout", "task": "Find major news outlets and publications that cover ethical and sustainable food and beverage." },
            {"agent": "social_intel", "task": "Analyze recent social media conversations and sentiment around fair trade coffee to identify key influencers and topics."}
        ]
    }
    
    return {"research_tasks": research_tasks}

# --- RESEARCH SUB-AGENTS (F) ---
# These agents use tools to perform their assigned research tasks.

def brand_research_node(state: AgentState) -> AgentState:
    """F1: Conducts brand and market research using search tools."""
    print("---RESEARCH SUB-AGENTS (F): Executing tasks...---")
    brief = state.get("brief", "")
    # Use the web search tool to get a list of results
    search_results = web_search_tool(f"latest trends in sustainable coffee {brief}")
    
    # Scrape the first two results to get some detailed content
    research_content = ""
    for result in search_results[:2]:
        research_content += f"**Source: {result['href']}**\n{web_scraper_tool(result['href'])}\n\n"
        
    return {"brand_research_result": research_content}

def media_scout_node(state: AgentState) -> AgentState:
    """F2: Identifies relevant media outlets and publications."""
    brief = state.get("brief", "")
    # Use the web search tool to find media outlets
    search_results = web_search_tool(f"top publications covering ethical and sustainable food and beverage {brief}")
    
    media_list = ""
    for result in search_results:
        media_list += f"- {result['title']} ({result['href']})\n"
        
    return {"media_scout_result": media_list}

def social_intel_node(state: AgentState) -> AgentState:
    """F3: Analyzes social media conversations and influencers."""
    brief = state.get("brief", "")
    # Use the web search tool to find social media sentiment
    search_results = web_search_tool(f"social media sentiment and influencers for fair trade coffee {brief}")
    
    social_intel = ""
    for result in search_results[:2]:
        social_intel += f"**Source: {result['href']}**\n{web_scraper_tool(result['href'])}\n\n"
        
    return {"social_intel_result": social_intel}

# --- HEAD OF RESEARCH (D4) ---
# This node compiles the research results into a comprehensive dossier.
def head_of_research_compile_dossier(state: AgentState) -> AgentState:
    """D4: Collects research and builds a comprehensive dossier."""
    print("---HEAD OF RESEARCH (D4): Compiling dossier...---")
    
    brand_research = state.get("brand_research_result", "")
    media_scout = state.get("media_scout_result", "")
    social_intel = state.get("social_intel_result", "")
    
    dossier = f"""
    # Campaign Research Dossier
    
    ## Brand & Market Research
    {brand_research}
    
    ## Media Landscape
    {media_scout}
    
    ## Social Media Intelligence
    {social_intel}
    """
    
    return {"dossier": dossier, "status": "dossier_created"}