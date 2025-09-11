from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_paper
from memory import store_summary, search_summaries
from phase3_main import run_phase3   # 👈 import your Phase 3 orchestrator
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
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
        return {str(k): clean_dict(v) for k, v in obj.items()}  # 🔑 force keys → str
    elif isinstance(obj, list):
        return [clean_dict(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(clean_dict(v) for v in obj)
    else:
        return to_serializable(obj)


@app.post("/analyze")
async def analyze(inp: AnalyzeInput):
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
        "phase3_report": report
    }
