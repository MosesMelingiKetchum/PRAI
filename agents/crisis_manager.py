from utils import llm, ChatPromptTemplate, StrOutputParser, AgentState
from typing import Optional, Dict, List

def crisis_manager_node(state: AgentState) -> AgentState:
    """K1: Conducts scenario planning based on the client brief."""
    print("---CRISIS MANAGER (K1): Conducting scenario planning...---")
    
    brief = state.get("brief", "")
    
    # Define a detailed prompt to guide the LLM in generating a crisis plan.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Crisis Manager. Your task is to develop a comprehensive crisis plan for a new product launch. Analyze the client brief for potential risks and vulnerabilities related to the campaign's core message. Your plan should include: a) a list of potential crisis scenarios, b) a recommended communication strategy for each scenario, and c) a list of key stakeholders to engage with."),
        ("human", f"Client Brief: {brief}")
    ])
    
    # Create an LLM chain to process the request.
    chain = prompt | llm | StrOutputParser()
    
    # Invoke the chain to get the crisis plan.
    crisis_plan = chain.invoke({"brief": brief})
    
    # Return the new state with the generated crisis plan.
    return {"crisis_plan": crisis_plan}