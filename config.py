import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # App Configuration
    APP_NAME = "EulerAI Backend"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8080))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # Model Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.3))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Research Configuration
    MAX_PAPERS = int(os.getenv("MAX_PAPERS", 5))
    N_CLUSTERS = int(os.getenv("N_CLUSTERS", 2))
    
    # Cloud Run Detection
    IS_CLOUD_RUN = os.getenv("K_SERVICE") is not None

config = Config()