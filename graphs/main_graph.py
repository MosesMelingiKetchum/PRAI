from utils import StateGraph, END
from typing import TypedDict, Optional, List, Dict

# Import your agent functions
from agents.orchestrator import (
    orchestrator_create_plan_node,
    orchestrator_review_dossier_and_brief,
    orchestrator_collect_final_assets,
)
from agents.crisis_manager import crisis_manager_node

# Import your sub-graphs
from graphs.research_graph import create_research_graph
from graphs.writing_graph import create_writing_graph

# Import the shared state definition
from state import AgentState

# This function is a "conditional router." It looks at the current status
# of the campaign and decides which path to take next.
def should_continue(state: AgentState) -> str:
    """Decides the next step after a sub-graph completes."""
    if state["status"] == "campaign_ready":
        return "end"
    elif state["status"] == "dossier_created":
        return "writing_pipeline"
    else:
        return "continue" # A default path for other scenarios

def create_main_graph():
    # --- MAIN WORKFLOW DEFINITION ---
    workflow = StateGraph(AgentState)
    
    # Add all the nodes to the workflow. The sub-graphs ('research_pipeline' and 'writing_pipeline')
    # are treated as single, self-contained nodes.
    workflow.add_node("orchestrator_create_plan", orchestrator_create_plan_node)
    workflow.add_node("research_pipeline", create_research_graph())
    workflow.add_node("orchestrator_review", orchestrator_review_dossier_and_brief)
    workflow.add_node("writing_pipeline", create_writing_graph())
    workflow.add_node("crisis_manager", crisis_manager_node)
    workflow.add_node("orchestrator_collect_final_assets", orchestrator_collect_final_assets)
    
    # Set the entry point for the entire workflow.
    workflow.set_entry_point("orchestrator_create_plan")
    
    # The path from the initial plan is a direct, non-conditional edge
    workflow.add_edge("orchestrator_create_plan", "research_pipeline")
    
    # Add the conditional edge for when the research pipeline completes
    workflow.add_conditional_edges(
        "research_pipeline",
        should_continue,
        {
            "writing_pipeline": "orchestrator_review",
            "continue": "orchestrator_review",
            "end": END,
        },
    )
    
    # Connect the rest of the nodes with direct edges
    workflow.add_edge("orchestrator_review", "writing_pipeline")
    workflow.add_edge("writing_pipeline", "crisis_manager")
    workflow.add_edge("crisis_manager", "orchestrator_collect_final_assets")
    workflow.add_edge("orchestrator_collect_final_assets", END)
    
    # Compile the final graph, making it ready to be executed.
    return workflow.compile()