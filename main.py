# main.py
from dotenv import load_dotenv
import os

from utils import AgentState
from graphs.main_graph import create_main_graph

# Load environment variables from .env file
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
print("DEBUG: GROQ_API_KEY loaded.")

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Create the final graph
app = create_main_graph()

# Initial state for the campaign
initial_state = AgentState(
    brief="We are a coffee company that wants to launch a new line of sustainable, ethically sourced coffee beans. Our campaign should highlight our commitment to environmental responsibility and fair trade practices. We need a full PR campaign, including a press release, journalist outreach, and a crisis plan."
)

# Run the graph
try:
    final_state = app.invoke(initial_state)
    
    print("\n\n--- CAMPAIGN COMPLETE! FINAL ASSETS ---")
    print(f"Final Status: {final_state.get('status', 'Unknown')}\n")

    final_assets = final_state.get("final_assets", {})

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
    print(final_assets.get("crisis_plan", "No crisis plan generated."))

    print("\n--- Writing Briefs ---")
    for brief_key, brief_content in final_assets.get("writing_briefs", {}).items():
        print(f"**{brief_key.replace('_', ' ').title()}**")
        print(brief_content)
        print("-" * 20)

except Exception as e:
    print(f"An error occurred during the graph execution: {e}")
    # You can inspect the final state even in case of an error
    print("\n--- Current State at Failure ---")
    print(final_state)