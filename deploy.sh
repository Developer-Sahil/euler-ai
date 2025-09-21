#!/bin/bash

# Script to prepare your code for Cloud Console deployment

echo "📦 Preparing deployment package..."

# Create a clean deployment directory
DEPLOY_DIR="euler-deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# Copy all necessary files
cp -r agents $DEPLOY_DIR/
cp *.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp Dockerfile $DEPLOY_DIR/
cp .dockerignore $DEPLOY_DIR/

# Create config.py if it doesn't exist
if [ ! -f "$DEPLOY_DIR/config.py" ]; then
    cat > $DEPLOY_DIR/config.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    APP_NAME = "EulerAI Backend"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8080))
    HOST = os.getenv("HOST", "0.0.0.0")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.3))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MAX_PAPERS = int(os.getenv("MAX_PAPERS", 5))
    N_CLUSTERS = int(os.getenv("N_CLUSTERS", 2))
    IS_CLOUD_RUN = os.getenv("K_SERVICE") is not None

config = Config()
EOF
fi

# Create a simple Dockerfile if it doesn't exist
if [ ! -f "$DEPLOY_DIR/Dockerfile" ]; then
    cat > $DEPLOY_DIR/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs/agent_runs

ENV PORT=8080

CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}
EOF
fi

# Create ZIP file
cd $DEPLOY_DIR
zip -r ../euler-backend-deploy.zip . -x "*.pyc" -x "*__pycache__*" -x "*.env"
cd ..

echo "✅ Deployment package created: euler-backend-deploy.zip"
echo "📝 Next: Upload this ZIP file to Cloud Console"