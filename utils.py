# utils.py

import os
from dotenv import load_dotenv
from typing import Optional, Dict, List, TypedDict

# LangChain and LangGraph imports are centralized here.
# This makes our agent files much cleaner and more focused on their specific logic.
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

# We also centralize the import for our shared state.
from state import AgentState

# Load environment variables from the .env file.
# This keeps our sensitive API keys safe and separate from the code.
load_dotenv()

# --- LLM INITIALIZATION ---
# This section intelligently decides which LLM to use based on which API key is present.
# We'll use either Groq or OpenAI, with Groq as the default if both are provided.
groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if groq_key:
    print("DEBUG: GROQ_API_KEY loaded.")
    llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)
elif openai_key:
    print("DEBUG: OPENAI_API_KEY loaded.")
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
else:
    raise ValueError("No valid API key found. Please set either GROQ_API_KEY or OPENAI_API_KEY in your .env file.")