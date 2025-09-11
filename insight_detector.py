from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

def detect_contradictions(cluster_text):
    """Analyze summaries to find contradictions and unique insights."""
    prompt = f"""
    Analyze the following research summaries:
    1. Identify contradictions or conflicting findings.
    2. Highlight unique insights.

    Summaries:
    {cluster_text}
    """
    response = llm.invoke(prompt)
    return response.content
