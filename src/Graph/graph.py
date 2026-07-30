
from langgraph.graph import StateGraph, START, END
from src.Graph.state import AgentState
from src.Graph.router import router
from src.Orchestration.supervisor_agent import supervisor
from src.Agents.PlannerAgent.planner_agent import PlannerAgent
from src.Agents.ResearcherAgent.researcher_Agent import ResearchAgent
from src.Agents.ResearcherAgent.researcher_Agent import ResearcherTools
from src.Agents.SynthesizeAgent.Synthesize_agent import Synthesize_agent
from src.Agents.WriterAgent.writer_agent import Writer_agent
from src.Agents.CriticAgent.critic_agent import CriticAgent
from langgraph.prebuilt import tools_condition
from Database.database import create_checkpoint

checkpointer=create_checkpoint()

graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor)
graph.add_node("Planner", PlannerAgent)
graph.add_node("Researcher", ResearchAgent)
graph.add_node("ResearcherTools",ResearcherTools)
graph.add_node("SynthesizeAgent",Synthesize_agent)
graph.add_node("WriterAgent",Writer_agent)
graph.add_node("CriticAgent",CriticAgent)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges(
    "supervisor",
    router,  
    {
        "planner": "Planner",
        "researcher": "Researcher",
        "synthesizer": "SynthesizeAgent",
        "writer": "WriterAgent",
        "critic": "CriticAgent",
        "FINISH": END,
    }
)
graph.add_edge("Planner", "supervisor")

graph.add_conditional_edges("Researcher",tools_condition,{"tools": "ResearcherTools",END: "supervisor"})
graph.add_edge("ResearcherTools", "Researcher")

graph.add_edge("SynthesizeAgent", "supervisor")

graph.add_edge("WriterAgent", "supervisor")

graph.add_edge("CriticAgent","supervisor")

app = graph.compile(checkpointer=checkpointer)