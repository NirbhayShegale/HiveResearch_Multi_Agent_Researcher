from src.config.config import P_R_llm
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from src.Agents.PlannerAgent.planner_prompt import PLANNER_AGENT_SYS_PROMPT
from src.Agents.PlannerAgent.Planner_model import PlannerModel
from src.Graph.state import AgentState

def PlannerAgent(state: AgentState)-> dict:

    Message = [
        SystemMessage(content=PLANNER_AGENT_SYS_PROMPT),
        HumanMessage(content=state["query"])
    ]

    llm = P_R_llm().with_structured_output(PlannerModel, method="json_mode")


    response = llm.invoke(Message)
    plan = response.model_dump()

    return {"messages": [AIMessage(content=response.model_dump_json())], "sub_tasks": plan["sub_tasks"]}