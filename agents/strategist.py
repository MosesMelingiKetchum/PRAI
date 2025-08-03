import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List
import random

from state import AgentState

load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

def strategist_interrogate_dossier(state: AgentState) -> AgentState:
    """E2: Interrogates dossier and adds perspective."""
    print("---STRATEGIST (E2): Interrogating dossier and adding perspective...---")
    dossier = state.get("dossier", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a PR strategist. Analyze the following dossier and add a strategic perspective, identifying key opportunities and potential angles for the campaign."),
        ("human", f"Dossier: {dossier}")
    ])
    chain = prompt | llm | StrOutputParser()
    strategic_perspective = chain.invoke({"dossier": dossier})
    updated_dossier = f"{dossier}\n\nStrategic Perspective: {strategic_perspective}"
    return {"dossier": updated_dossier, "status": "strategist_perspective_added"}

def strategist_select_journalists(state: AgentState) -> AgentState:
    """E4: Selects target journalists from a comprehensive list."""
    print("---STRATEGIST (E4): Selecting target journalists...---")
    journalists_list = state.get("journalists_list", [])
    if journalists_list:
        selected = random.sample(journalists_list, min(len(journalists_list), 3))
    else:
        selected = []
    return {"selected_journalists": selected, "status": "journalists_selected"}

def strategist_determine_briefs(state: AgentState) -> AgentState:
    """E5: Determines what briefs need creating."""
    print("---STRATEGIST (E5): Determining required briefs...---")
    dossier = state.get("dossier", "")
    writing_briefs = {
        "creative_brief": "Create a creative concept.",
        "design_brief": "Create design assets.",
        "social_brief": "Create a social media content plan.",
        "analytics_brief": "Create a research & analytics brief."
    }
    # We are removing the status update here to avoid the concurrency issue.
    return {"writing_briefs": writing_briefs}

