from typing import Dict
from agents.questioner import QuestionerAgent
from agents.searcher import SearcherAgent
from agents.summarizer_agent import SummarizerAgent
from agents.base import AgentLogger

class Orchestrator:
    """
    Minimal coordinator that wires the three agents into an autonomous loop.
    Loop design:
      Round 1: Searcher -> Summarizer -> Questioner
      Round 2 (optional): Use top questions to expand the query and repeat.
    """
    def __init__(self, searcher: SearcherAgent, summarizer: SummarizerAgent, questioner: QuestionerAgent, logger: AgentLogger):
        self.searcher = searcher
        self.summarizer = summarizer
        self.questioner = questioner
        self.logger = logger

    def run_once(self, topic: str, max_results: int = 5, n_clusters: int = 2) -> Dict:
        self.logger.log(agent="orchestrator", event="start_round", payload={"topic": topic}, rationale_summary="Kick off round with base topic.")
        papers = self.searcher.run(topic, max_results=max_results)
        summarized = self.summarizer.run(papers)
        analysis = self.questioner.run(summarized, n_clusters=n_clusters)
        self.logger.log(agent="orchestrator", event="round_complete", payload={"topic": topic}, rationale_summary="Round finished.")
        return {"papers": papers, "summaries": summarized, **analysis}

    def run_two_rounds(self, topic: str, max_results: int = 5, n_clusters: int = 2) -> Dict:
        # Round 1
        first = self.run_once(topic, max_results=max_results, n_clusters=n_clusters)
        # Extract a few questions to expand query (heuristic: first cluster's first 2 lines)
        expanded = topic
        try:
            any_cluster = next(iter(first.get("questions", {}).values()))
            lines = [ln.strip("- • ") for ln in any_cluster.splitlines() if ln.strip()]
            expanded_candidates = lines[:2]
            if expanded_candidates:
                expanded = topic + " " + " ".join(expanded_candidates)
        except Exception:
            pass
        self.logger.log(agent="orchestrator", event="expand_query", payload={"expanded_query": expanded}, rationale_summary="Expanded search query using generated questions.")
        # Round 2
        second = self.run_once(expanded, max_results=max_results, n_clusters=n_clusters)
        return {"round1": first, "round2": second}