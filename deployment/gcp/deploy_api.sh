#!/bin/bash

# Set variables
PROJECT_ID="your-gcp-project-id"
SERVICE_NAME="geotech-api-service"
REGION="us-central1"  # Specify your region
IMAGE_NAME="gcr.io/$PROJECT_ID/geotech-api"
PORT=8080  # The port Flask will run on

# Step 1: Authenticate with GCP
echo "Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $PROJECT_ID

# Step 2: Enable required services
echo "Enabling required GCP services..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 3: Build the Docker image and push to Google Container Registry
echo "Building Docker image for Flask API..."
gcloud builds submit --tag $IMAGE_NAME .

# Step 4: Deploy the Docker image to Cloud Run
echo "Deploying API to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port $PORT

# Step 5: Get the deployed Cloud Run URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format "value(status.url)")
echo "API deployed successfully. Accessible at: $SERVICE_URL"

