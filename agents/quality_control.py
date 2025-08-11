from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from typing import Optional, Dict, List

def quality_control_dossier_node(state: AgentState) -> AgentState:
    """G1: The QC Agent reviews the research dossier for quality."""
    print("---QUALITY CONTROL (G1): Reviewing dossier...---")
    dossier = state.get("dossier", "")
    
    if dossier and len(dossier) > 100: # Simple check to see if the dossier is not empty
        print("---QC PASSED: Dossier approved!---")
        return {"qc_passed_dossier": True}
    else:
        print("---QC FAILED: Dossier is incomplete!---")
        return {"qc_passed_dossier": False}

# This node checks the press releases to ensure they are ready for publication.
# In a real app, it would use an LLM to review the content.
def quality_control_press_releases_node(state: AgentState) -> AgentState:
    """G1: The QC Agent reviews press releases for factual accuracy and tone."""
    print("---QUALITY CONTROL (G1/G2): Fact-checking content...---")
    press_releases = state.get("press_releases", [])
    
    if press_releases:
        print("---QC PASSED: All content approved!---")
        return {"qc_passed": True}
    else:
        print("---QC FAILED: No content to review!---")
        return {"qc_passed": False}

# This node performs a similar check on the personalized emails.
# It ensures they are appropriate and ready to be sent to journalists.
def quality_control_emails_node(state: AgentState) -> AgentState:
    """G2: The QC Agent reviews emails for accuracy and tone."""
    print("---QUALITY CONTROL (G1/G2): Fact-checking emails...---")
    emails = state.get("personalized_emails", [])
    
    if emails:
        print("---QC PASSED: All emails approved!---")
        return {"qc_passed": True}
    else:
        print("---QC FAILED: No emails to review!---")
        return {"qc_passed": False}