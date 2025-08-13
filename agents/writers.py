from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from typing import Optional, Dict, List

# This is the primary writing agent. It takes the research dossier and a brief
# and uses the LLM to generate a full press release.
def writers_group_node(state: AgentState) -> AgentState:
    """H1: Writers generate a press release."""
    print("---WRITERS GROUP (H1): Generating press release...---")
    dossier = state.get("dossier", "")
    writing_briefs = state.get("writing_briefs", {})
    
    press_release_brief = writing_briefs.get("press_release_writer", "")
    
    # Updated the prompt to be more direct and less conversational.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert PR writer. Using the following dossier and brief, write a compelling and professional press release. The response should be a complete press release, including a headline, body, and contact information. Do NOT add conversational preambles or explanations."),
        ("human", f"Dossier: {dossier}\n\nBrief: {press_release_brief}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    # The actual LLM call to generate the press release
    press_release = chain.invoke({"dossier": dossier, "press_release_brief": press_release_brief})
    
    return {"press_releases": [press_release]}

# --- PLACEHOLDER BRIEF WRITERS (RUNS IN PARALLEL) ---
# These are placeholder functions that would, in a more complex setup, use the LLM
# to generate specific creative briefs. For this project, they simply return a
# dictionary with a placeholder string. This demonstrates how a graph can run
# multiple tasks at the same time.
def creative_brief_writer_node(state: AgentState) -> AgentState:
    """H2: Creates a creative brief."""
    print("---WRITERS GROUP (H2): Creating creative brief...---")
    # This now returns a unique key so it doesn't conflict with other brief writers
    return {"creative_brief": "Creative brief content here."}

def design_brief_writer_node(state: AgentState) -> AgentState:
    """H3: Creates a design brief."""
    print("---WRITERS GROUP (H3): Creating design brief...---")
    # This now returns a unique key so it doesn't conflict with other brief writers
    return {"design_brief": "Design brief content here."}

def social_brief_writer_node(state: AgentState) -> AgentState:
    """H4: Creates a social media brief."""
    print("---WRITERS GROUP (H4): Creating social media brief...---")
    # This now returns a unique key so it doesn't conflict with other brief writers
    return {"social_brief": "Social media brief content here."}

def research_analytics_brief_writer_node(state: AgentState) -> AgentState:
    """H5: Creates a research and analytics brief."""
    print("---WRITERS GROUP (H5): Creating research brief...---")
    # This now returns a unique key so it doesn't conflict with other brief writers
    return {"research_analytics_brief": "Research brief content here."}
    
# This agent takes the final list of journalists and uses the LLM to write a
# personalized email for each one.
def email_writers_node(state: AgentState) -> AgentState:
    """J2: Writers generate personalized emails."""
    print("---EMAIL WRITERS (J2): Generating personalized emails...---")
    journalists = state.get("journalists_list", [])
    dossier = state.get("dossier", "")
    emails = []

    for journalist in journalists:
        # Added more specific instructions to ensure the email is about coffee
        # and doesn't contain placeholders.
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a PR assistant. Write a personalized outreach email to {journalist['name']} at {journalist['outlet']} about a new line of sustainable, ethically sourced coffee beans. Use the following dossier to inform your pitch. The email should start with a subject line and should be concise and professional. Do not add any conversational filler or preambles."),
            ("human", f"Dossier: {dossier}")
        ])
        chain = prompt | llm | StrOutputParser()
        email_content = chain.invoke({"dossier": dossier})
        emails.append(f"To: {journalist['contact']}\n\n{email_content}")
    
    return {"personalized_emails": emails}