from src.Graph.state import AgentState
from src.Agents.ResearcherAgent.researcher_prompt import RESEARCHER_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.Tools.Tavily import search_tool
from langgraph.prebuilt import ToolNode
from src.Agents.ResearcherAgent.research_summarizer import research_summarizer
from src.config.config import P_R_llm


llm = P_R_llm()
Researcher_llm_with_tools= llm.bind_tools([search_tool])
ResearcherTools = ToolNode([search_tool])

def ResearchAgent(state: AgentState) -> dict:
    tasks = state.get("sub_tasks", [])

    if len(tasks) == 0:
        return {
            "sub_tasks": [],
            "messages": [AIMessage(content="No pending research tasks.")]
        }

    current_task = tasks[0]
    global_messages = state.get("messages", [])

    last_message = global_messages[-1] if global_messages else None

    task_instructions = f"""
        Here is your current research assignment:
        **Question:** {current_task["question"]}
        **Specific Aspect to Focus On:** {current_task["aspect"]}
        **Preferred Source Type:** {current_task["source_type"]}

        Please use your Tavily search tool to research this topic
    """

    # --- After tool invocation: summarize and move on ---
    if last_message and getattr(last_message, "type", "") == "tool":


        search_results = last_message.content
        summary = research_summarizer(current_task, search_results)

        mapped_note = (
            f"### Research for Sub-Task: {current_task['question']}\n"
            f"{summary}"
        )

        return {
            "messages": [AIMessage(content=summary)],
            "research_notes": [mapped_note],
            "sub_tasks": tasks[1:]
        }

    # --- First time invoking for this task: let the LLM decide to search ---
    message = [
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
        HumanMessage(content=task_instructions),
    ]

    response = Researcher_llm_with_tools.invoke(message)

    update = {"messages": [response]}

    if not response.tool_calls and response.content:
        summary = research_summarizer(current_task, response.content)
        mapped_note = (
            f"### Research for Sub-Task: {current_task['question']}\n"
            f"{summary}"
        )
        update["messages"] = [AIMessage(content=summary)]
        update["research_notes"] = [mapped_note]
        update["sub_tasks"] = tasks[1:]

    return update