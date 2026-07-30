import sys
from src.Graph.graph import app
from dotenv import load_dotenv
load_dotenv()
import uuid

sys.stdout.reconfigure(encoding='utf-8')

THREAD_ID = "04c9ae9c-e2f2-4547-b018-0a7561848dd4"

def main():
    user_query = "Recent Protest of jantar mantar"
    initial_state = {
        "query": user_query,        
        "messages": [],             
    }
    config = {"configurable": {"thread_id": THREAD_ID}}

    # Check if there's existing state to resume from
    existing = app.get_state(config)
    if existing and existing.values:
        print("--- Resuming from last checkpoint ---")
        return app.stream(None, config=config)
    else:
        print("--- Starting new run ---")
        return app.stream(initial_state, config=config)


if __name__ == "__main__":
    for s in main():
        print(s)
