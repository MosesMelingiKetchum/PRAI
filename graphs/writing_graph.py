from utils import StateGraph, END
from agents.writers import (
    writers_group_node,
    email_writers_node,
    creative_brief_writer_node,
    design_brief_writer_node,
    social_brief_writer_node,
    research_analytics_brief_writer_node
)
from agents.strategist import strategist_determine_briefs, strategist_select_journalists
from agents.quality_control import quality_control_press_releases_node, quality_control_emails_node
from agents.journalist_research import journalist_research_identify_and_save # Updated import
from state import AgentState

def create_writing_graph():
    writing_workflow = StateGraph(AgentState)
    
    writing_workflow.add_node("writers_group", writers_group_node)
    writing_workflow.add_node("journalist_research", journalist_research_identify_and_save)
    writing_workflow.add_node("quality_control_pr", quality_control_press_releases_node)
    writing_workflow.add_node("quality_control_emails", quality_control_emails_node)
    writing_workflow.add_node("strategist_determine_briefs", strategist_determine_briefs)
    writing_workflow.add_node("strategist_select_journalists", strategist_select_journalists)
    writing_workflow.add_node("email_writers", email_writers_node)
    
    # Brief writer nodes
    writing_workflow.add_node("creative_writer", creative_brief_writer_node)
    writing_workflow.add_node("design_writer", design_brief_writer_node)
    writing_workflow.add_node("social_writer", social_brief_writer_node)
    writing_workflow.add_node("research_writer", research_analytics_brief_writer_node)
    
    # Entry point
    writing_workflow.set_entry_point("writers_group")
    
    # Edges
    writing_workflow.add_edge("writers_group", "quality_control_pr")
    writing_workflow.add_edge("quality_control_pr", "strategist_determine_briefs")
    
    # Parallel paths
    writing_workflow.add_edge("quality_control_pr", "journalist_research")
    
    # Parallel brief writers
    writing_workflow.add_edge("strategist_determine_briefs", "creative_writer")
    writing_workflow.add_edge("strategist_determine_briefs", "design_writer")
    writing_workflow.add_edge("strategist_determine_briefs", "social_writer")
    writing_workflow.add_edge("strategist_determine_briefs", "research_writer")

    # Journalist research path
    writing_workflow.add_edge("journalist_research", "strategist_select_journalists")
    writing_workflow.add_edge("strategist_select_journalists", "email_writers")
    writing_workflow.add_edge("email_writers", "quality_control_emails")
    
    # End node is the last parallel process that finishes.
    writing_workflow.add_edge("quality_control_emails", END)
    writing_workflow.add_edge("creative_writer", END)
    writing_workflow.add_edge("design_writer", END)
    writing_workflow.add_edge("social_writer", END)
    writing_workflow.add_edge("research_writer", END)

    return writing_workflow.compile()