from src.Graph.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from src.Orchestration.Supervisor_prompt import SUPERVISOR_PROMPT
from src.Graph.router import SupervisorDecision
from src.config.config import get_llm

def supervisor(state: AgentState)-> dict:

    messages = state.get('messages', [])
    formatted_list = []

    for msg in messages:
        sender_type = msg.__class__.__name__ 
        text = msg.content
        formatted_list.append(f"{sender_type}: {text}")

    formatted_messages = "\n".join(formatted_list)

    sub_tasks = state.get("sub_tasks", None)
    synthesis = state.get("synthesis", "")
    draft = state.get("draft", "")

    critic_approval = state.get("critic_approval", None)
    critic_feedback = state.get("critic_feedback", "")

    planner_has_run = sub_tasks is not None
    pending_tasks = len(sub_tasks) if sub_tasks else 0

    state_summary = f"""
    Current State:
    - Planner has run: {'Yes' if planner_has_run else 'No'}
    - Pending Sub-tasks: {pending_tasks}
    - Synthesis completed: {'Yes' if synthesis else 'No'}
    - Draft completed: {'Yes' if draft else 'No'}
    - Critic approval: {critic_approval}
    - Critic feedback: {critic_feedback if critic_feedback else 'None'}
    
    Message History:
    {formatted_messages}
    
    Look at the current state and message history, then decide which agent should act next.
    Look at the RULES in your system prompt. Based ONLY on the facts above, output your JSON routing decision.
    """
    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT),
        HumanMessage(content=state_summary)
    ]
    
    response = get_llm().with_structured_output(SupervisorDecision, method="json_mode").invoke(messages)
    
    return {"reason":response.reasoning,"next_agent": response.next_agent}