from typing import TypedDict, Optional, List, Dict

# The AgentState acts as the single source of truth for the entire workflow.
# All agents read from and write to this state.
# We use TypedDict to give the state a clear, defined structure.
class AgentState(TypedDict):
    """
    Represents the state of our PR campaign, which is passed between agents.
    It's like a shared document that every team member can update.
    """
    # The initial request or instructions from the client.
    brief: str
    
    # The high-level plan created by the orchestrator.
    plan: Optional[str]
    
    # Specific research tasks for the sub-agents to follow.
    research_tasks: Optional[str]
    
    # A dictionary holding the results of the research tasks.
    research_results: Optional[Dict[str, str]]
    
    # A compiled report of all the research findings.
    dossier: Optional[str]
    
    # Specific instructions for writers to create content.
    writing_briefs: Optional[List[Dict[str, str]]]
    
    # The final press releases generated.
    press_releases: Optional[List[str]]
    
    # A list of journalists identified for outreach.
    journalists_list: Optional[List[Dict[str, str]]]
    
    # Personalized emails written for the journalists.
    personalized_emails: Optional[List[str]]
    
    # A detailed plan for handling potential crises.
    crisis_plan: Optional[str]
    
    # A final dictionary containing all the campaign assets.
    final_assets: Optional[Dict]
    
    # The current status of the campaign (e.g., 'plan_needed', 'research_complete').
    status: str
    
    # A flag to indicate if content has passed quality control.
    qc_passed: Optional[bool]
    
    # A temporary list of potential journalists before a final selection is made.
    potential_journalists: Optional[List[Dict[str, str]]]