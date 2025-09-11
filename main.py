# main.py
from paper_fetcher import fetch_arxiv_papers
from summarizer import summarize_paper
from memory import store_summary, search_summaries
from clustering import cluster_summaries
from insight_detector import detect_contradictions
from question_generator import generate_questions

def main():
    topic = input("Enter research topic: ")
    papers = fetch_arxiv_papers(topic)

    print("\n--- Fetching & Summarizing Papers ---\n")
    summaries = []
    for paper in papers:
        summary = summarize_paper(paper["summary"])
        summaries.append(summary)
        print(f"\nTitle: {paper['title']}")
        print(f"Summary: {summary}")
        store_summary(paper["title"], summary, paper["link"])

    print("\n--- Clustering Summaries ---\n")
    clusters = cluster_summaries(summaries, n_clusters=2)
    for label, cluster in clusters.items():
        print(f"Cluster {label+1}:")
        for text in cluster:
            print(f" - {text}")

    print("\n--- Detecting Contradictions and Insights ---\n")
    for label, cluster in clusters.items():
        cluster_text = "\n".join(cluster)
        insights = detect_contradictions(cluster_text)
        print(f"\nCluster {label+1} Insights:\n{insights}")

    print("\n--- Generating Research Questions ---\n")
    for label, cluster in clusters.items():
        cluster_text = "\n".join(cluster)
        questions = generate_questions(cluster_text)
        print(f"\nCluster {label+1} Questions:\n{questions}")

    print("\n--- Memory Retrieval Test ---\n")
    query = input("Search memory for: ")
    results = search_summaries(query)
    if not results.get("documents") or not results["documents"][0]:
        print("No results found.")
    else:
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            print(f"\nTitle: {meta['title']}\nSummary: {doc}\nLink: {meta['link']}")

if __name__ == "__main__":
    main()
