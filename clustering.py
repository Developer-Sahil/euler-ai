from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster_summaries(summaries, n_clusters=2):
    """Cluster research paper summaries into n_clusters using embeddings."""
    if not summaries:
        return {}

    embeddings = model.encode(summaries)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    clustered = {}
    for idx, label in enumerate(labels):
        clustered.setdefault(label, []).append(summaries[idx])
    return clustered
