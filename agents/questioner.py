# ------------------------------
# agents/questioner.py
# ------------------------------
from agents.base import Agent
from typing import List, Dict
from clustering import cluster_summaries
from insight_detector import detect_contradictions
from question_generator import generate_questions

class QuestionerAgent(Agent):
    def run(self, summarized: List[Dict], n_clusters: int = 2) -> Dict:
        self.log("start", {"num_items": len(summarized), "n_clusters": n_clusters}, rationale_summary="Clustering summaries, detecting contradictions, generating questions.")
        summaries = [s["summary"] for s in summarized]
        clusters = cluster_summaries(summaries, n_clusters=n_clusters) if summaries else {}
        insights = {}
        questions = {}
        for label, items in clusters.items():
            joined = "\n\n".join(items)
            try:
                contr = detect_contradictions(joined)
            except Exception as e:
                contr = f"Insight detection failed: {e}"
            try:
                qs = generate_questions(joined)
            except Exception as e:
                qs = f"Question generation failed: {e}"
            insights[label] = contr
            questions[label] = qs
            self.log("cluster_analyzed", {"cluster": int(label), "size": len(items)}, rationale_summary="Produced insight/contradiction summary and questions.")
        result = {"clusters": clusters, "insights": insights, "questions": questions}
        self.log("done", {"num_clusters": len(clusters)}, rationale_summary="Analysis complete.")
        return result