from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

def generate_questions(cluster_text):
    """Generate deep research questions based on summaries."""
    prompt = f"""
    Based on these research summaries, generate 3-5 deep research questions
    that would advance understanding in this domain.

    Summaries:
    {cluster_text}
    """
    response = llm.invoke(prompt)
    return response.content
