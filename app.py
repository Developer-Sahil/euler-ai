import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_paper
from memory import store_summary, search_summaries
from phase3_main import run_phase3
import numpy as np
import json

app = FastAPI(title="EulerAI Backend", version="1.0.0")

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # In production, replace with your actual frontend URL
        # "https://your-frontend-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class AnalyzeInput(BaseModel):
    text: str
    title: str = None
    link: str = None

# ---- Utility: Convert numpy & other non-serializable objects ----
def to_serializable(val):
    if isinstance(val, (np.int32, np.int64)):
        return int(val)
    if isinstance(val, (np.float32, np.float64)):
        return float(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    return str(val)  # fallback

def clean_dict(obj):
    if isinstance(obj, dict):
        return {str(k): clean_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_dict(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(clean_dict(v) for v in obj)
    else:
        return to_serializable(obj)

@app.get("/")
async def root():
    return {
        "message": "Euler AI Backend is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "euler-ai-backend"}

@app.post("/analyze")
async def analyze(inp: AnalyzeInput):
    try:
        # Step 1: Summarize
        summary = summarize_paper(inp.text)

        # Step 2: Store in memory
        if inp.title:
            store_summary(inp.title, summary, inp.link or "")

        # Step 3: Run Phase 3 reasoning (multi-agent workflow)
        report = run_phase3(inp.text)

        # Step 4: Clean up numpy types + keys
        if report:
            report = clean_dict(report)

        return {
            "summary": summary,
            "phase3_report": report,
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "summary": None,
            "phase3_report": None
        }

# Cloud Run specific - use PORT env variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)