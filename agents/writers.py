import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List

from state import AgentState

load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

def writers_group_node(state: AgentState) -> AgentState:
    """H1: Creates press releases based on briefs."""
    print("---WRITERS (H1): Creating press releases...---")
    dossier = state.get("dossier", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional press release writer. Based on the following dossier, write a compelling press release. The release should be newsworthy and formatted correctly."),
        ("human", f"Dossier: {dossier}")
    ])
    chain = prompt | llm | StrOutputParser()
    press_release = chain.invoke({"dossier": dossier})
    return {"press_releases": [press_release], "status": "press_release_written"}

def journalist_research_identify_and_save(state: AgentState) -> AgentState:
    """I1, I2: Identifies journalists and saves a comprehensive list."""
    print("---JOURNALIST RESEARCH (I1, I2): Identifying and saving journalists...---")
    dossier = state.get("dossier", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a media researcher. Based on the product and information in the dossier, identify 10 relevant journalists and their media outlets. Return a list of names and their outlets, e.g., 'Name, Outlet'."),
        ("human", f"Dossier: {dossier}")
    ])
    chain = prompt | llm | StrOutputParser()
    journalists_str = chain.invoke({"dossier": dossier})
    journalists_list = [j.strip() for j in journalists_str.split('\n')]
    media_list_excel = f"Comprehensive Media List:\n{journalists_str}"
    return {"journalists_list": journalists_list, "media_list_excel": media_list_excel, "status": "journalists_identified"}

def email_writers_node(state: AgentState) -> AgentState:
    """J1: Creates personalized emails for the target journalists."""
    print("---EMAIL WRITERS (J1): Creating personalized emails...---")
    journalists = state.get("selected_journalists", [])
    press_releases = state.get("press_releases", [])
    personalized_emails = []
    for journalist in journalists:
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are an expert email marketer. Write a highly personalized, compelling email pitch to the journalist named {journalist}. The email should briefly summarize the attached press release and explain why this story is relevant to their specific media outlet. Be concise and persuasive."),
            ("human", f"Press Release:\n{press_releases[0]}")
        ])
        chain = prompt | llm | StrOutputParser()
        email_content = chain.invoke({})
        personalized_emails.append(email_content)
    return {"personalized_emails": personalized_emails, "status": "emails_written"}

def creative_brief_writer_node(state: AgentState) -> AgentState:
    """M1: Creates a creative brief."""
    print("---BRIEF WRITER (M1): Creating creative brief...---")
    # This is a simplified function. A real LLM call would generate this.
    brief = "Creative Brief: Develop a campaign concept around the theme 'Sip Sustainably'."
    # We are removing the status update to avoid concurrency issues.
    return {"writing_briefs": {"creative_brief": brief}}

def design_brief_writer_node(state: AgentState) -> AgentState:
    """M2: Creates a design brief."""
    print("---BRIEF WRITER (M2): Creating design brief...---")
    # Simplified function.
    brief = "Design Brief: Create modern, eco-friendly visuals for social media and a landing page."
    # We are removing the status update to avoid concurrency issues.
    return {"writing_briefs": {"design_brief": brief}}

def social_brief_writer_node(state: AgentState) -> AgentState:
    """M3: Creates a social brief."""
    print("---BRIEF WRITER (MWRITERS): Creating social brief...---")
    # Simplified function.
    brief = "Social Brief: Plan a content calendar focusing on brand ambassadors and sustainability."
    # We are removing the status update to avoid concurrency issues.
    return {"writing_briefs": {"social_brief": brief}}

def research_analytics_brief_writer_node(state: AgentState) -> AgentState:
    """M4: Creates a research & analytics brief."""
    print("---BRIEF WRITER (M4): Creating research & analytics brief...---")
    # Simplified function.
    brief = "Research & Analytics Brief: Set up tracking for campaign performance and sentiment analysis."
    # We are removing the status update to avoid concurrency issues.
    return {"writing_briefs": {"analytics_brief": brief}}
