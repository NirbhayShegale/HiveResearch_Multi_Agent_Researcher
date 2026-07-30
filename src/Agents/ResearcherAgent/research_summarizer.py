from langchain_core.messages import SystemMessage, HumanMessage
from src.config.config import get_llm

_llm = get_llm()

def research_summarizer(task: dict, tool_results: str) -> str:
    question = task.get("question", "the research question")
    messages = [
        SystemMessage(content=(
            "You are a research analyst. Summarize the provided search results "
            "into a clear, concise, factual note that directly answers the question."
        )),
        HumanMessage(content=(
            f"Question: {question}\n\n"
            f"Search Results:\n{tool_results}\n\n"
            "Write a focused summary answering the question above."
        )),
    ]
    response = _llm.invoke(messages)
    return response.content