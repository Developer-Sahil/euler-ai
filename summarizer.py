from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",  # Groq’s best for reasoning/summarization
    temperature=0.3
)

template = """
Summarize the following research paper abstract in 3-4 bullet points.
Abstract: {abstract}
"""
prompt = PromptTemplate(input_variables=["abstract"], template=template)

def summarize_paper(abstract):
    return llm.predict(prompt.format(abstract=abstract))
