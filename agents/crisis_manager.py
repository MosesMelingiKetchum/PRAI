import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List

from state import AgentState

load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

def crisis_manager_node(state: AgentState) -> AgentState:
    """K1: Conducts scenario planning."""
    print("---CRISIS MANAGER (K1): Conducting scenario planning...---")
    dossier = state.get("dossier", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a crisis management expert. Based on the campaign brief and dossier, identify potential risks and create a basic crisis communication plan. The plan should include possible negative scenarios and a prepared response."),
        ("human", f"Dossier: {dossier}")
    ])
    chain = prompt | llm | StrOutputParser()
    crisis_plan = chain.invoke({"dossier": dossier})
    return {"crisis_plan": crisis_plan, "status": "crisis_plan_created"}
