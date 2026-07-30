from src.Agents.CriticAgent.critic_model import CriticModel
from src.Agents.CriticAgent.critic_prompt import CRITIC_AGENT_SYS_PROMPT
from src.Graph.state import AgentState
from src.config.config import critic_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def CriticAgent(state: AgentState) -> dict:
    original_query = state["query"]
    draft = state.get("draft", "")
    synthesis = state.get("synthesis", "")

    task_instructions = f"""
    Please review the following draft.
    
    **The Original Question It Must Answer:** 
    {original_query}
    
    **The Research Synthesis (for reference):**
    {synthesis}
    
    **The Current Draft to Review:**
    {draft}
    """

    message = [
        SystemMessage(content=CRITIC_AGENT_SYS_PROMPT),
        HumanMessage(content=task_instructions)
    ]

    
    
    response = critic_llm().with_structured_output(CriticModel, method="json_mode").invoke(message)
    
    return {
        "messages": [AIMessage(content=response.feedback)],
        "critic_approval": response.approved,
        "critic_feedback": response.feedback
    }
