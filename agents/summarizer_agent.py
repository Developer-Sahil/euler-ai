# ------------------------------
# agents/summarizer_agent.py
# ------------------------------
from typing import List, Dict
from summarizer import summarize_paper
from memory import store_summary
from agents.base import Agent

class SummarizerAgent(Agent):
    def run(self, papers: List[Dict]) -> List[Dict]:
        self.log("start", {"num_papers": len(papers)}, rationale_summary="Summarizing abstracts and storing in vector DB.")
        outputs = []
        for p in papers:
            title = p.get("title", "Untitled")
            abstract = p.get("summary", "")
            try:
                summary = summarize_paper(abstract)
                store_summary(title, summary, p.get("link", ""))
                outputs.append({"title": title, "summary": summary, "link": p.get("link", "")})
                self.log("summarized_one", {"title": title}, rationale_summary="Summary created and stored.")
            except Exception as e:
                self.log("error", {"title": title, "error": str(e)}, rationale_summary="Failed to summarize; skipping.")
        self.log("done", {"num_summarized": len(outputs)}, rationale_summary="Completed summarization batch.")
        return outputs