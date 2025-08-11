from utils import StateGraph, END
from agents.research import (
    head_of_research_node, # Corrected: Replaces the old function name
    brand_research_node,
    media_scout_node,
    social_intel_node,
    head_of_research_compile_dossier
)
from agents.strategist import strategist_interrogate_dossier
from agents.quality_control import quality_control_dossier_node
from state import AgentState

def create_research_graph():
    research_workflow = StateGraph(AgentState)

    # Define the nodes for the research graph
    research_workflow.add_node("head_of_research", head_of_research_node)
    research_workflow.add_node("brand_research", brand_research_node)
    research_workflow.add_node("media_scout", media_scout_node)
    research_workflow.add_node("social_intel", social_intel_node)
    research_workflow.add_node("compile_dossier", head_of_research_compile_dossier)
    research_workflow.add_node("strategist", strategist_interrogate_dossier)
    research_workflow.add_node("quality_control", quality_control_dossier_node)

    # Set up the entry point and edges
    research_workflow.set_entry_point("head_of_research")

    # Connect the research tasks in parallel
    research_workflow.add_edge("head_of_research", "brand_research")
    research_workflow.add_edge("head_of_research", "media_scout")
    research_workflow.add_edge("head_of_research", "social_intel")

    # The research results all flow into the dossier compilation node
    research_workflow.add_edge("brand_research", "compile_dossier")
    research_workflow.add_edge("media_scout", "compile_dossier")
    research_workflow.add_edge("social_intel", "compile_dossier")
    
    # After compiling, the dossier is interrogated by the strategist, then checked by QC
    research_workflow.add_edge("compile_dossier", "strategist")
    research_workflow.add_edge("strategist", "quality_control")

    # The research graph ends after quality control
    research_workflow.add_edge("quality_control", END)
    
    return research_workflow.compile()