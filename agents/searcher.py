# ------------------------------
# agents/searcher.py
# ------------------------------
from typing import List, Dict
from paper_fetcher import fetch_arxiv_papers
from agents.base import Agent

class SearcherAgent(Agent):
    def run(self, topic: str, max_results: int = 5) -> List[Dict]:
        self.log("start", {"topic": topic, "max_results": max_results}, rationale_summary="Searching arXiv for relevant papers.")
        papers = fetch_arxiv_papers(topic, max_results=max_results)
        self.log("done", {"num_papers": len(papers)}, rationale_summary="Fetched candidates; handing to Summarizer.")
        return papers
