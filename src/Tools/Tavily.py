from langchain_core.tools import tool
from tavily import TavilyClient
import os

@tool
def search_tool (query:str):
    """
    Its a Tavily Search Tool ,which is used to find information on internet,
    used for research 
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=tavily_api_key)
    response = tavily_client.search(
    query=query,
    search_depth="advanced",
    max_results=3
    )
    return response