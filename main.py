from langgraph.graph import StateGraph, END

# Import the shared state
from state import AgentState

# Import individual agents that are not part of a sub-graph
from agents.orchestrator import (
    orchestrator_create_plan_node,
    orchestrator_collect_final_assets,
)
from agents.crisis_manager import crisis_manager_node

# Import the sub-graph creation functions
from graphs.research_graph import create_research_graph
from graphs.writing_graph import create_writing_graph

# 1. Initialize the main StateGraph
workflow = StateGraph(AgentState)

# 2. Add individual nodes first (e.g., entry/exit points, or single agents)
workflow.add_node("orchestrator_create_plan", orchestrator_create_plan_node)
workflow.add_node("crisis_manager", crisis_manager_node)
workflow.add_node("orchestrator_collect_assets", orchestrator_collect_final_assets)

# 3. Add our sub-graphs as nodes to the main graph
# Note: LangGraph compiles the sub-graphs first, then adds them as nodes.
research_pipeline = create_research_graph()
writing_pipeline = create_writing_graph()

workflow.add_node("research_pipeline_node", research_pipeline)
workflow.add_node("writing_pipeline_node", writing_pipeline)

# 4. Set the entry point
workflow.set_entry_point("orchestrator_create_plan")

# 5. Define the edges (connections) of the main graph
workflow.add_edge("orchestrator_create_plan", "research_pipeline_node")
workflow.add_edge("research_pipeline_node", "writing_pipeline_node")
workflow.add_edge("writing_pipeline_node", "crisis_manager")
workflow.add_edge("crisis_manager", "orchestrator_collect_assets")

# Final end point
workflow.add_edge("orchestrator_collect_assets", END)

# 6. Compile the main workflow into a runnable LangGraph app.
app = workflow.compile()

# --- RUNNING THE APPLICATION ---
if __name__ == "__main__":
    # Define the initial state with the user's brief.
    initial_brief = "I need a press campaign to announce our new AI-powered coffee maker that is eco-friendly. It should highlight sustainability and cutting-edge technology."
    initial_state = {
        "brief": initial_brief, 
        "research_tasks": [], 
        "press_releases": [], 
        "journalists_list": [], 
        "personalized_emails": [],
        "quality_control_issues": [],
    }

    # Invoke the graph with the initial state.
    final_state = app.invoke(initial_state)

    # Print the final output.
    print("\n\n--- CAMPAIGN COMPLETE! FINAL ASSETS ---")
    print(f"Final Status: {final_state['status']}")
    
    final_assets = final_state.get('final_assets', {})
    print("\n--- Press Releases ---")
    for pr in final_assets.get("press_releases", []):
        print(pr)
    
    print("\n--- Target Journalists ---")
    for j in final_assets.get("journalists_list", []):
        print(j)
    
    print("\n--- Personalized Emails ---")
    for e in final_assets.get("personalized_emails", []):
        print(e)
        
    print("\n--- Crisis Plan ---")
    print(final_assets.get("crisis_plan", "No crisis plan found."))
    
    print("\n--- Writing Briefs ---")
    for name, brief in final_assets.get("writing_briefs", {}).items():
        print(f"Brief for {name}:\n{brief}")