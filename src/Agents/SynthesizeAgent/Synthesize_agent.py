from langchain_core.messages import HumanMessage,SystemMessage, AIMessage
from src.Graph.state import AgentState
from src.Agents.SynthesizeAgent.synthesize_prompt import SYNTHESIZE_AGENT_SYS_PROMPT
from src.config.config import get_llm

def Synthesize_agent(state: AgentState) -> dict:
    query = state["query"]
    notes = state["research_notes"]
    
    raw_notes = "\n\n".join(notes)
    
    message = f"""Here is the original query:
    **Query:** {query}

    Here is the research compiled by the Researcher agent:
    {raw_notes}
    
    Please synthesize this information into a cohesive summary and build a unified outline."""

    messages = [
        SystemMessage(content=SYNTHESIZE_AGENT_SYS_PROMPT),
        HumanMessage(content=message)
    ]
    
    response = get_llm().invoke(messages)
    
    return {"messages": [AIMessage(content=response.content)],"synthesis": response.content}
