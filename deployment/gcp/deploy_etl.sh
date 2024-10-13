#!/bin/bash

# Set variables
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"  # Set your region
CLUSTER_NAME="geotech-dataproc-cluster"
BUCKET_NAME="your-bucket-name"  # Replace with your GCS bucket name
GCS_CODE_PATH="gs://$BUCKET_NAME/etl_jobs/main_etl.py"
BIGQUERY_DATASET="geotech_dataset"
BIGQUERY_TABLE="geospatial_data"
JOB_NAME="geotech-etl-job"

# Step 1: Authenticate with GCP (if needed)
gcloud auth login
gcloud config set project $PROJECT_ID

# Step 2: Create a Dataproc cluster (if it doesn't already exist)
echo "Creating Dataproc cluster..."
gcloud dataproc clusters create $CLUSTER_NAME \
    --region=$REGION \
    --single-node \
    --master-machine-type=n1-standard-4 \
    --master-boot-disk-size=100GB \
    --image-version=2.0-debian10 \
    --optional-components=ANACONDA,JUPYTER \
    --enable-component-gateway

# Step 3: Upload ETL code to Google Cloud Storage
echo "Uploading ETL code to GCS bucket..."
gsutil cp ../etl/main_etl.py $GCS_CODE_PATH

# Step 4: Submit the Spark job to Dataproc
echo "Submitting ETL job to Dataproc cluster..."
gcloud dataproc jobs submit pyspark $GCS_CODE_PATH \
    --cluster=$CLUSTER_NAME \
    --region=$REGION \
    --properties spark.submit.deployMode=cluster \
    -- async \
    --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    -- $PROJECT_ID $BIGQUERY_DATASET $BIGQUERY_TABLE

# Step 5: Monitor the Dataproc job
echo "Monitoring Dataproc job..."
gcloud dataproc jobs wait $JOB_NAME --region=$REGION

# Step 6: Clean up Dataproc cluster (optional)
echo "Cleaning up Dataproc cluster..."
gcloud dataproc clusters delete $CLUSTER_NAME --region=$REGION --quiet

echo "ETL job completed successfully."
