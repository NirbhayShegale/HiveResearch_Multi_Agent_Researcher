from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langsmith import traceable
from src.Graph.graph import app as graph_app
import uuid
import json

app = FastAPI()


class QueryRequest(BaseModel):
    userquery: str

@app.get('/')
def read_root():
    return {"message": "Welcome to the HIVE MIND"}

@app.post("/research")
@traceable(run_type="chain", name="Hive Mind Research")
def research(request: QueryRequest):
    
    initial_state = {
        "query": request.userquery,        
        "messages": [],             
    }
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    def event_stream():
        for event in graph_app.stream(initial_state, config=config, stream_mode="updates"):
            for node_name, node_output in event.items():
                serializable = {k: v for k, v in node_output.items() if k != "messages"}
                chunk = json.dumps({"node": node_name, "data": serializable}, default=str)
                yield f"data: {chunk}\n\n"
                
    return StreamingResponse(event_stream(), media_type="text/event-stream")
