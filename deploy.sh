#!/bin/bash

# EulerAI Backend Deployment Script for Google Cloud Run

set -e

# Configuration
PROJECT_ID="euler-ai-471908"  # Change this to your project ID
SERVICE_NAME="euler-ai-backend"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Starting deployment of EulerAI Backend to Cloud Run..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Set project
echo "📋 Setting project to ${PROJECT_ID}..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Build the container
echo "🔨 Building Docker container..."
gcloud builds submit --tag ${IMAGE_NAME} .

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --port 8080 \
    --set-env-vars="GROQ_API_KEY=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"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo "✅ Deployment complete!"
echo "🌐 Your service is available at: ${SERVICE_URL}"
echo ""
echo "📝 Next steps:"
echo "1. Test the health endpoint: curl ${SERVICE_URL}/health"
echo "2. Update your frontend to use this URL"
echo "3. Set up environment variables if needed"
echo ""
echo "To set the GROQ API key:"
echo "gcloud run services update ${SERVICE_NAME} --set-secrets=GROQ_API_KEY=groq-api-key:latest --region ${REGION}"