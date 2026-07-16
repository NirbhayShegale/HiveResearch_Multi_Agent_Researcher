from pydantic import BaseModel
from typing import  Literal
from src.Graph.state import AgentState

class SupervisorDecision(BaseModel):
    reasoning: str
    next_agent: Literal["planner", "researcher","synthesizer" ,"writer","critic","FINISH"]


def router(state: AgentState)-> dict:
    return state['next_agent']

