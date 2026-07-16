import sys
from src.Graph.graph import app

sys.stdout.reconfigure(encoding='utf-8')

def main():
    user_query = "What is the difference in box office revenue between Demon Slayer: Infinity Castle and Superman?"
    initial_state = {
        "query": user_query,        
        "messages": [],             
    }
    return app.stream(initial_state)


if __name__ == "__main__":
    for s in main():
        print(s)
