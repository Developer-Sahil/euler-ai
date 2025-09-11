import requests
import feedparser

def fetch_arxiv_papers(topic, max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    search_query = f"all:{topic}"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    response = requests.get(base_url, params=params)
    feed = feedparser.parse(response.text)
    
    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        })
    return papers
