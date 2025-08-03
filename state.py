from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    """
    The state of the PR campaign workflow.

    Attributes:
        brief: The initial brief from the user.
        plan: The high-level plan created by the Orchestrator.
        dossier: The comprehensive research document.
        research_tasks: A list of research tasks for sub-agents.
        research_results: A dictionary of research results from sub-agents.
        press_releases: The generated press releases.
        journalists_list: A list of target journalists.
        personalized_emails: A list of personalized emails for journalists.
        final_assets: The collected final assets for delivery.
        status: The current status of the campaign.
    """
    brief: Optional[str]
    plan: Optional[str]
    dossier: Optional[str]
    research_tasks: List[str]
    research_results: Optional[Dict[str, str]]
    press_releases: List[str]
    journalists_list: List[str]
    personalized_emails: List[str]
    final_assets: Optional[Dict[str, str]]
    status: Optional[str]
