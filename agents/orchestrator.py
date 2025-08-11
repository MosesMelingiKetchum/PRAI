from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from typing import Optional, Dict, List

# --- Agent 1: The Orchestrator (Orchestrator_Create_Plan) ---
def orchestrator_create_plan_node(state: AgentState) -> AgentState:
    """B1: The Orchestrator creates an initial campaign plan."""
    print("---ORCHESTRATOR (B1): Creating initial plan...---")
    brief = state.get("brief", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the head of a PR firm. Your task is to review the client brief and create an initial campaign plan. Do not write any campaign materials yet."),
        ("human", "Brief: {brief}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    plan = chain.invoke({"brief": brief})
    
    return {"plan": plan}

# --- Agent 2: The Orchestrator (Orchestrator_Review_Dossier_and_Brief) ---
def orchestrator_review_dossier_and_brief(state: AgentState) -> AgentState:
    """B2: The Orchestrator reviews the research dossier and builds writing briefs."""
    print("---ORCHESTRATOR (B2): Reviewing dossier and building writing briefs...---")
    dossier = state.get("dossier", "")
    insights = state.get("insights", "")
    
    # Placeholder for an LLM call to build the briefs.
    # For now, we use a simple placeholder to represent the action.
    press_release_brief = f"Based on these insights:\n\n{insights}\n\nWrite a compelling press release highlighting the new sustainable coffee line. The dossier provides the key details. Focus on the environmental and fair trade aspects."
    
    return {"writing_briefs": {"press_release_writer": press_release_brief}}

# --- Agent 3: The Orchestrator (Orchestrator_Collect_Final_Assets) ---
def orchestrator_collect_final_assets(state: AgentState) -> AgentState:
    """B6: The Orchestrator collects all final assets."""
    print("---ORCHESTRATOR (B6): Collecting final assets...---")

    press_releases = state.get("press_releases", [])
    journalists_list = state.get("journalists_list", [])
    personalized_emails = state.get("personalized_emails", [])
    crisis_plan = state.get("crisis_plan", "")

    # We now collect briefs differently to avoid the ValueError.
    writing_briefs = {}
    
    # The briefs are now stored as individual keys in the state.
    # We collect them and place them into a single dictionary.
    if state.get("creative_brief"):
        writing_briefs["creative"] = state.get("creative_brief")
    if state.get("design_brief"):
        writing_briefs["design"] = state.get("design_brief")
    if state.get("social_brief"):
        writing_briefs["social"] = state.get("social_brief")
    if state.get("research_analytics_brief"):
        writing_briefs["research_analytics"] = state.get("research_analytics_brief")
    
    # Placeholder for a more complex LLM call to assemble the final report.
    final_report = {
        "press_releases": press_releases,
        "journalists_list": journalists_list,
        "personalized_emails": personalized_emails,
        "writing_briefs": writing_briefs,
        "crisis_plan": crisis_plan
    }
    
    return {"final_assets": final_report, "status": "campaign_ready"}