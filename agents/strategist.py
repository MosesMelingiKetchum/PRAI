from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from typing import Optional, Dict, List

# This node takes the comprehensive dossier from the research team and uses
# the LLM to pull out key insights that are relevant for the campaign.
# It acts as a bridge between research and the creative/writing teams.
def strategist_interrogate_dossier(state: AgentState) -> AgentState:
    """E1: Interrogates dossier for strategic insights."""
    print("---STRATEGIST (E1): Interrogating dossier for insights...---")
    dossier = state.get("dossier", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior strategist. Analyze the following research dossier and extract the most critical insights that will inform a successful PR campaign. Focus on the core message, key selling points, and potential market challenges."),
        ("human", f"Research Dossier: {dossier}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    insights = chain.invoke({"dossier": dossier})
    
    return {"insights": insights} # Status update removed

# This node determines which types of writing briefs are needed for the campaign
# (e.g., creative, design, social media). This decision is based on the strategic
# insights extracted from the dossier.
def strategist_determine_briefs(state: AgentState) -> AgentState:
    """E2: Determines which types of briefs are needed."""
    print("---STRATEGIST (E2): Determining which briefs are needed...---")
    
    # This is a placeholder for an LLM call that would determine the briefs.
    # For now, we will assume we need all of them to make the graph run in parallel.
    brief_types = ["creative_brief_writer", "design_brief_writer", "social_brief_writer", "research_analytics_brief_writer"]
    
    return {"brief_types": brief_types} # Status update removed

# This node takes the list of potential journalists and makes a final selection
# based on the campaign's strategic goals. It refines the list before it's sent
# to the writing team for email personalization.
def strategist_select_journalists(state: AgentState) -> AgentState:
    """J1: Selects the final list of journalists."""
    print("---STRATEGIST (J1): Selecting final journalists...---")
    potential_journalists = state.get("potential_journalists", [])
    
    # In a real application, an LLM would make a strategic selection.
    # For now, we'll assume all potential journalists are selected.
    journalists_list = potential_journalists
    
    return {"journalists_list": journalists_list} # Status update removed