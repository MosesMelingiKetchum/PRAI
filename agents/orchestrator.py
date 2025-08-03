import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List

from state import AgentState

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
print(f"DEBUG: GROQ_API_KEY loaded: {groq_key}")
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

def orchestrator_create_plan_node(state: AgentState) -> AgentState:
    """B1: Interrogates the brief and creates an initial plan."""
    print("---ORCHESTRATOR (B1): Creating initial plan...---")
    brief = state.get("brief", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert PR campaign orchestrator. Based on the user's brief, create a detailed, step-by-step plan for a PR campaign. The plan should include research, writing, and distribution phases."),
        ("human", f"Brief: {brief}")
    ])
    chain = prompt | llm | StrOutputParser()
    plan = chain.invoke({"brief": brief})
    return {"plan": plan, "status": "plan_created"}

def orchestrator_review_dossier_and_brief(state: AgentState) -> AgentState:
    """B2: Reviews dossier and builds writing briefs."""
    print("---ORCHESTRATOR (B2): Reviewing dossier and building writing briefs...---")
    dossier = state.get("dossier", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the orchestrator. Based on the following research dossier, create a set of writing briefs for different agents. The briefs should be specific and actionable. Create briefs for 'press_release_writer' and 'email_writer'."),
        ("human", f"Dossier: {dossier}")
    ])
    chain = prompt | llm | StrOutputParser()
    writing_briefs_str = chain.invoke({"dossier": dossier})
    writing_briefs = {
        "press_release_writer": "Create an impactful press release based on the dossier.",
        "email_writer": "Create personalized emails for journalists."
    }
    # We are removing the status update here to avoid the concurrency issue.
    return {"writing_briefs": writing_briefs}

def orchestrator_brief_crisis_manager(state: AgentState) -> AgentState:
    """B3: Briefs the Crisis Manager."""
    print("---ORCHESTRATOR (B3): Briefing Crisis Manager...---")
    return {"status": "crisis_manager_briefed"}

def orchestrator_assign_agents(state: AgentState) -> AgentState:
    """B4: Assigns agents to fill gaps (e.g., after QC issues)."""
    print("---ORCHESTRATOR (B4): Re-assigning agents to fix issues...---")
    return {"status": "rework_needed"}

def orchestrator_write_prompts_for_brief_writers(state: AgentState) -> AgentState:
    """B5: Write prompts for brief writer agents."""
    print("---ORCHESTRATOR (B5): Writing prompts for brief writers...---")
    dossier = state.get("dossier", "")
    brief_writers_prompts = {
        "creative_brief": f"Based on the dossier, write a creative brief. Dossier: {dossier}",
        "design_brief": f"Based on the dossier, write a design brief. Dossier: {dossier}",
        "social_brief": f"Based on the dossier, write a social media brief. Dossier: {dossier}",
    }
    return {"writing_briefs": brief_writers_prompts, "status": "brief_prompts_created"}

def orchestrator_collect_final_assets(state: AgentState) -> AgentState:
    """B6: Collects final assets for delivery."""
    print("---ORCHESTRATOR (B6): Collecting final assets...---")
    final_assets = {
        "press_releases": state.get("press_releases", []),
        "personalized_emails": state.get("personalized_emails", []),
        "journalists_list": state.get("selected_journalists", []),
        "media_list": state.get("media_list_excel", ""),
        "crisis_plan": state.get("crisis_plan", ""),
        "writing_briefs": state.get("writing_briefs", {})
    }
    return {"final_assets": final_assets, "status": "campaign_ready"}
