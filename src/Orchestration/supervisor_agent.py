from src.Graph.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from src.Orchestration.Supervisor_prompt import SUPERVISOR_PROMPT
from src.config.config import P_R_llm
from typing import Optional
import json


def next_agent(state: AgentState) -> str:
    
    sub_tasks = state.get("sub_tasks", None)
    synthesis = state.get("synthesis", "")
    draft = state.get("draft", "")
    critic_approval = state.get("critic_approval", None)

    if sub_tasks is None:
        return "planner"
    if len(sub_tasks) > 0:
        return "researcher"
    if not synthesis:
        return "synthesizer"
    if not draft:
        return "writer"
    if critic_approval is None:
        return "critic"
    if critic_approval is False:
        return "writer"
    return "FINISH"

def supervisor(state: AgentState) -> dict:
    resolved_next = next_agent(state)

    sub_tasks = state.get("sub_tasks", None)
    research_notes = state.get("research_notes", [])
    synthesis = state.get("synthesis", "")
    draft = state.get("draft", "")
    critic_approval = state.get("critic_approval", None)
    critic_feedback = state.get("critic_feedback", "")

    state_summary = f"""

    Chat History: {state['messages']}

    Current workflow state:
    - Planner has run: {'Yes' if sub_tasks is not None else 'No'}
    - Pending sub-tasks: {len(sub_tasks) if sub_tasks else 0}
    - Completed research notes: {len(research_notes)}
    - Synthesis completed: {'Yes' if synthesis else 'No'}
    - Draft completed: {'Yes' if draft else 'No'}
    - Critic approval: {critic_approval}
    - Critic feedback: {critic_feedback or 'None'}

    The next agent to act is: **{resolved_next}**

    Respond with valid JSON. Explain in 1-2 sentences WHY this agent is the correct next step 
    given the current state. Your response must follow this format:
    {{"reasoning": "your explanation here", "next_agent": "{resolved_next}"}}
    """

    try:
        messages = [
            SystemMessage(content=SUPERVISOR_PROMPT),
            HumanMessage(content=state_summary),
        ]
        response = P_R_llm().invoke(messages)
        reasoning = response.content.strip()

        if "reasoning" in reasoning:
            try:
                parsed = json.loads(reasoning)
                reasoning = parsed.get("reasoning", reasoning)
            except json.JSONDecodeError:
                pass
    except Exception:
        reasoning = f"Routing to {resolved_next} based on current workflow state."

    return {"reason": reasoning, "next_agent": resolved_next}