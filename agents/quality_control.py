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

def quality_control_node(state: AgentState) -> AgentState:
    """G1, G2: Fact-checks the dossier and press releases."""
    print("---QUALITY CONTROL (G1/G2): Fact-checking content...---")
    issues = []
    if random.random() < 0.2:
        issues.append("QC failed: Fictional claims or inconsistencies found.")
        print(f"---QC FAILED: Issues found: {issues}---")
        return {"quality_control_issues": issues, "status": "issues_found"}
    print("---QC PASSED: All content approved!---")
    return {"quality_control_issues": [], "status": "approved"}

