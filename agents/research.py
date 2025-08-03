import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List

from state import AgentState

load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

def head_research_node(state: AgentState) -> AgentState:
    """D1, D2, D3: Receives brief, collaborates on plan, builds tasks for sub-agents."""
    print("---HEAD OF RESEARCH (D1, D2, D3): Building research tasks...---")
    plan = state.get("plan", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Head of Research. Based on the campaign plan, create a list of specific research tasks for sub-agents like Brand Research, Media Scout, and Social Intel. The tasks should be clear and actionable. Return the tasks as a comma-separated list."),
        ("human", f"Campaign plan: {plan}")
    ])
    chain = prompt | llm | StrOutputParser()
    research_tasks_str = chain.invoke({"plan": plan})
    research_tasks = [task.strip() for task in research_tasks_str.split(',')]
    return {"research_tasks": research_tasks, "status": "research_tasks_created"}

def head_research_collect_dossier(state: AgentState) -> AgentState:
    """D4: Collects research and builds a comprehensive dossier."""
    print("---HEAD OF RESEARCH (D4): Compiling dossier...---")
    research_results = state.get("research_results", {})
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research analyst. Compile the following research results into a comprehensive, well-structured dossier. Ensure the dossier is easy to read and contains all key information."),
        ("human", "Research Results: {research_results}") # Corrected line
    ])
    chain = prompt | llm | StrOutputParser()
    dossier = chain.invoke({"research_results": research_results})
    return {"dossier": dossier, "status": "dossier_created"}

def research_sub_agents_node(state: AgentState) -> AgentState:
    """F: Simulates the Brand, Media, and Social research sub-agents."""
    print("---RESEARCH SUB-AGENTS (F): Executing tasks...---")
    research_tasks = state.get("research_tasks", [])
    research_results = {}
    for task in research_tasks:
        research_results[task] = f"Sample research data for task: '{task}'. This is where web search or other tools would run."
    return {"research_results": research_results, "status": "research_complete"}
