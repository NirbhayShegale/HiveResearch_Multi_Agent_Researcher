from src.Graph.state import AgentState
from src.Agents.ResearcherAgent.researcher_prompt import RESEARCHER_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.config.config import get_llm
from src.Tools.Tavily import search_tool
from langgraph.prebuilt import ToolNode


llm = get_llm()
Researcher_llm_with_tools= llm.bind_tools([search_tool])

ResearcherTools = ToolNode([search_tool])

def ResearchAgent(state: AgentState) -> dict:
    tasks = state.get("sub_tasks", [])
    
    if not tasks:
        return {
            "sub_tasks": [],
            "messages": [AIMessage(content="No pending research tasks.")]
        }
    
    current_task = tasks[0]
    global_messages = state.get("messages", [])
    
    last_message = global_messages[-1] if global_messages else None
    
    hints_list = current_task.get("search_hints", [])
    hints_str = "\n".join([f"- {h}" for h in hints_list])
        
    task_instructions = f"""
        Here is your current research assignment:
        **Question:** {current_task["question"]}
        **Specific Aspect to Focus On:** {current_task["aspect"]}
        **Preferred Source Type:** {current_task["source_type"]}
        
        **Suggested Search Queries/Hints:**
        {hints_str}
        
        Please use your Tavily search tool to research this topic and write a summary of your findings.
    """

    # SCENARIO B: RETURNING FROM A TOOL CALL


    if last_message and getattr(last_message, "type", "") == "tool":
        

        short_context = [
            SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
            HumanMessage(content=f"Please summarize the findings for this question: {current_task['question']}"),
            global_messages[-2], # The AIMessage making the tool call
            global_messages[-1]  # The ToolMessage containing the Tavily results
        ]
        
        response = Researcher_llm_with_tools.invoke(short_context)
        update = {"messages": [response]}

        if not response.tool_calls and response.content:
            mapped_note = f"### Research for Sub-Task: {current_task['question']}\n{response.content}"
            update["research_notes"] = [mapped_note]
            update["sub_tasks"] = tasks[1:] 
            
        return update

    # SCENARIO A: STARTING A NEW TASK


    fresh_messages = [
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
        HumanMessage(content=task_instructions)
    ]
        
    response = Researcher_llm_with_tools.invoke(fresh_messages)
    update = {"messages": [response]}
    
    if not response.tool_calls and response.content:
        mapped_note = f"### Research for Sub-Task: {current_task['question']}\n{response.content}"
        update["research_notes"] = [mapped_note]
        update["sub_tasks"] = tasks[1:] # Pop it

    return update