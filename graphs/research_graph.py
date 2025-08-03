from langgraph.graph import StateGraph
from langgraph.graph import END

# Import the shared state
from state import AgentState

# Import the agents from our new modular files
from agents.research import (
    head_research_node,
    head_research_collect_dossier,
    research_sub_agents_node
)
from agents.strategist import strategist_interrogate_dossier
from agents.orchestrator import orchestrator_brief_crisis_manager

def create_research_graph() -> StateGraph:
    """
    Creates and returns a sub-graph for the research and dossier-building pipeline.
    This graph starts from the brief and ends with a complete dossier.
    """
    # Initialize the sub-graph
    research_pipeline = StateGraph(AgentState)

    # Add the nodes (agents)
    research_pipeline.add_node("head_research", head_research_node)
    research_pipeline.add_node("research_team", research_sub_agents_node)
    research_pipeline.add_node("head_research_collect_dossier", head_research_collect_dossier)
    research_pipeline.add_node("strategist_interrogate_dossier", strategist_interrogate_dossier)
    research_pipeline.add_node("brief_crisis_manager", orchestrator_brief_crisis_manager)
    
    # Define the entry and exit points
    research_pipeline.set_entry_point("head_research")
    
    # Define the edges (connections) for the sub-graph
    research_pipeline.add_edge("head_research", "research_team")
    research_pipeline.add_edge("research_team", "head_research_collect_dossier")
    research_pipeline.add_edge("head_research_collect_dossier", "strategist_interrogate_dossier")
    research_pipeline.add_edge("strategist_interrogate_dossier", END)
    
    return research_pipeline.compile()

if __name__ == "__main__":
    # This is for testing the sub-graph in isolation.
    # We will not run this in the final main.py.
    research_pipeline_graph = create_research_graph()
    
    initial_state = {
        "brief": "I need a press campaign to announce our new AI-powered eco-friendly coffee maker.",
        "research_tasks": [], "research_results": {}, "dossier": ""
    }
    
    final_state = research_pipeline_graph.invoke(initial_state)
    
    print("\n--- Research Pipeline Complete ---")
    print(f"Final Status: {final_state['status']}")
    print(f"Final Dossier:\n{final_state['dossier'][:200]}...") # Print a snippet
