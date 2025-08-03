from langgraph.graph import StateGraph, END

# Import the shared state
from state import AgentState

# Import the agents from our new modular files
from agents.orchestrator import (
    orchestrator_review_dossier_and_brief,
    orchestrator_assign_agents
)
from agents.writers import (
    writers_group_node,
    journalist_research_identify_and_save,
    email_writers_node,
    creative_brief_writer_node,
    design_brief_writer_node,
    social_brief_writer_node,
    research_analytics_brief_writer_node
)
from agents.strategist import strategist_select_journalists, strategist_determine_briefs
from agents.quality_control import quality_control_node

def create_writing_graph() -> StateGraph:
    """
    Creates and returns a sub-graph for the writing and outreach pipeline.
    This graph takes a dossier and produces press releases and emails.
    """
    writing_pipeline = StateGraph(AgentState)

    # Add the nodes (agents)
    writing_pipeline.add_node("orchestrator_review", orchestrator_review_dossier_and_brief)
    writing_pipeline.add_node("writers_group", writers_group_node)
    writing_pipeline.add_node("quality_control_press_releases", quality_control_node)
    writing_pipeline.add_node("rework_needed", orchestrator_assign_agents)
    writing_pipeline.add_node("journalist_research", journalist_research_identify_and_save)
    writing_pipeline.add_node("strategist_select_journalists", strategist_select_journalists)
    writing_pipeline.add_node("email_writers", email_writers_node)

    # These are for the brief writers, as per the flowchart
    writing_pipeline.add_node("strategist_determine_briefs", strategist_determine_briefs)
    writing_pipeline.add_node("creative_writer", creative_brief_writer_node)
    writing_pipeline.add_node("design_writer", design_brief_writer_node)
    writing_pipeline.add_node("social_writer", social_brief_writer_node)
    writing_pipeline.add_node("analytics_writer", research_analytics_brief_writer_node)

    # Set the entry point for this sub-graph
    writing_pipeline.set_entry_point("orchestrator_review")

    # Define the edges (connections)
    writing_pipeline.add_edge("orchestrator_review", "writers_group")
    writing_pipeline.add_edge("writers_group", "quality_control_press_releases")
    writing_pipeline.add_edge("quality_control_press_releases", "journalist_research")
    writing_pipeline.add_edge("journalist_research", "strategist_select_journalists")
    writing_pipeline.add_edge("strategist_select_journalists", "email_writers")

    # Connect the brief writers pipeline (these will be run in parallel)
    writing_pipeline.add_edge("orchestrator_review", "strategist_determine_briefs")
    writing_pipeline.add_edge("strategist_determine_briefs", "creative_writer")
    writing_pipeline.add_edge("strategist_determine_briefs", "design_writer")
    writing_pipeline.add_edge("strategist_determine_briefs", "social_writer")
    writing_pipeline.add_edge("strategist_determine_briefs", "analytics_writer")

    # The Quality Control conditional logic.
    # If the QC passes, we move on. If not, we go back to the orchestrator to assign agents.
    writing_pipeline.add_conditional_edges(
        "quality_control_press_releases",
        lambda state: "rework" if state.get("quality_control_issues") else "end_of_graph",
        {
            "rework": "rework_needed",
            "end_of_graph": END,
        },
    )

    # Rework loop. If rework is needed, we end this graph.
    # In the main graph, we will route back to the appropriate place.
    writing_pipeline.add_edge("rework_needed", END)
    
    # We will assume brief writers run in parallel and end the graph.
    writing_pipeline.add_edge("creative_writer", END)
    writing_pipeline.add_edge("design_writer", END)
    writing_pipeline.add_edge("social_writer", END)
    writing_pipeline.add_edge("analytics_writer", END)
    
    return writing_pipeline.compile()


if __name__ == "__main__":
    # This is for testing the sub-graph in isolation.
    writing_pipeline_graph = create_writing_graph()
    
    # We need to simulate a dossier from the previous step.
    test_dossier = "This is a comprehensive dossier about a new eco-friendly AI coffee maker. Key features include sustainable materials, a smart brewing system, and a subscription service for custom coffee beans. Target audience is environmentally conscious tech enthusiasts. The key messaging is 'Sip Smart, Sip Sustainably'."
    
    initial_state = {
        "brief": "I need a press campaign to announce our new AI-powered eco-friendly coffee maker.",
        "dossier": test_dossier,
        "research_tasks": [], "research_results": {},
        "press_releases": [], "journalists_list": [], "personalized_emails": [],
    }
    
    final_state = writing_pipeline_graph.invoke(initial_state)
    
    print("\n--- Writing Pipeline Complete ---")
    print(f"Final Status: {final_state['status']}")
    print(f"Final Press Release:\n{final_state.get('press_releases', ['N/A'])[0][:200]}...")
    print(f"Final Journalists Identified: {final_state.get('journalists_list', ['N/A'])}")
