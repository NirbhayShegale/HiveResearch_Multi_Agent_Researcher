from langgraph.graph import add_messages
from typing import TypedDict, Annotated,List
import operator
from langchain_core.messages import  BaseMessage

class AgentState(TypedDict):
    query: str
    messages: Annotated[list[BaseMessage], add_messages] 
    next_agent: str
    reason: str
    
    sub_tasks: List[dict]

    research_notes: Annotated[list[str], operator.add]

    synthesis : str

    draft: str

    critic_approval : bool
    critic_feedback : str
    
