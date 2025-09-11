# ------------------------------
# phase3_main.py
# ------------------------------

from agents.base import AgentLogger
from agents.searcher import SearcherAgent
from agents.summarizer_agent import SummarizerAgent
from agents.questioner import QuestionerAgent
from orchestrator import Orchestrator
import os

def run_phase3(topic: str, mode: str = "2", max_results: int = 5, n_clusters: int = 2):
    """
    Run Phase 3 autonomous research workflow programmatically.
    Args:
        topic (str): base research topic or abstract text
        mode (str): "1" for one round, "2" for two rounds (default)
        max_results (int): number of papers to fetch
        n_clusters (int): number of clusters
    Returns:
        dict: structured output containing summaries, insights, questions
    """
    logger = AgentLogger()
    searcher = SearcherAgent(name="Searcher", logger=logger)
    summarizer_agent = SummarizerAgent(name="Summarizer", logger=logger)
    questioner = QuestionerAgent(name="Questioner", logger=logger)

    orch = Orchestrator(searcher, summarizer_agent, questioner, logger)

    if mode == "1":
        output = orch.run_once(topic, max_results=max_results, n_clusters=n_clusters)
    else:
        output = orch.run_two_rounds(topic, max_results=max_results, n_clusters=n_clusters)

    return output

if __name__ == "__main__":
    print("=== Phase 3: Autonomous Research Workflow ===")
    topic = input("Enter base research topic: ")
    mode = input("Choose mode: [1] one round, [2] two rounds with query expansion (default 2): ").strip() or "2"

    try:
        output = run_phase3(topic, mode=mode)
    except Exception as e:
        print("Fatal error:", e)
        raise

    # Persist results as before
    snapshot_path = os.path.join(logger.run_dir, "snapshot.txt")
    try:
        with open(snapshot_path, "w", encoding="utf-8") as f:
            f.write("=== RESEARCH TOPIC ===\n" + topic + "\n\n")

            rounds = ["round1", "round2"] if "round1" in output else [None]
            for round_key in rounds:
                data = output.get(round_key, output)
                title = round_key.upper() if round_key else "RESULTS"
                f.write(f"\n===== {title} =====\n")

                f.write("\n--- SUMMARIES ---\n")
                for item in data.get("summaries", []):
                    f.write(f"\nTitle: {item['title']}\n")
                    f.write(f"Summary: {item['summary']}\n")
                    f.write(f"Link: {item['link']}\n")

                f.write("\n--- INSIGHTS ---\n")
                for cluster, insight in data.get("insights", {}).items():
                    f.write(f"\n[Cluster {cluster} Insights]\n{insight}\n")

                f.write("\n--- QUESTIONS ---\n")
                for cluster, qs in data.get("questions", {}).items():
                    f.write(f"\n[Cluster {cluster} Questions]\n{qs}\n")

        print(f"\n✅ Full logs written to: {logger.run_dir}")
        print(f"📄 Detailed snapshot: {snapshot_path}")
    except Exception as e:
        print("❌ Failed to write snapshot:", e)
