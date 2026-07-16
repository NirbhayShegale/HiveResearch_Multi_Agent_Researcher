from src.Agents.WriterAgent.writer_prompt import WRITER_AGENT_SYS_PROMPT
from langchain_core.messages import HumanMessage,SystemMessage
from src.Graph.state import AgentState
from src.config.config import get_llm

def Writer_agent(state: AgentState) -> dict:
    original_query = state.get("query", "")
    synthesis = state.get("synthesis", "")
    current_draft = state.get("draft", "")
    feedback = state.get("critic_feedback", "")
    approval = state.get("critic_approval","")

    if approval == False: 
        task_instructions = f"""
        You are an expert editor. Please revise the draft below strictly to address the critic's feedback.
        
        **The Original Question You Must Answer:** 
        {original_query}
        
        **The Current Draft:**
        {current_draft}
        
        **The Critic Feedback to Address:** 
        {feedback}
        
        OUTPUT FORMATTING:
        Output ONLY the final revised draft. Do not include any introductory phrases, conversational filler, or acknowledgements.
        """
       
    else:      
        task_instructions = f"""
        Please write the final comprehensive report.
        
        **The Original Question You Must Answer:** 
        {original_query}
        
        **The Research Synthesis & Outline to follow:**
        {synthesis}
        """

    message =[
        SystemMessage(content=WRITER_AGENT_SYS_PROMPT),
        HumanMessage(content=task_instructions)
    ]

    response = get_llm().invoke(message)
    
    return {"messages":[response],"draft": response.content}

    