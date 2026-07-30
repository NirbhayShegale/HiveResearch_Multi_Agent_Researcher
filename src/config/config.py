from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def P_R_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

def synthesis_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.6,
    )

def writer_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.9,
    )

def critic_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
    )
