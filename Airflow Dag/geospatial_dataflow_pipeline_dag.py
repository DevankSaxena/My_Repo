import os
from datetime import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowCreateJobOperator
from airflow.utils.dates import days_ago

# Set default arguments
default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'project': 'your-gcp-project-id',
    'region': 'your-region',  # e.g., 'us-central1'
    'gcp_conn_id': 'google_cloud_default',
    'temp_location': 'gs://your-bucket/temp',
    'staging_location': 'gs://your-bucket/staging',
}

# Define the DAG
with models.DAG(
    'geospatial_dataflow_job_dag',
    default_args=default_args,
    schedule_interval=None,  # Manually triggered or set to a specific interval
    catchup=False,
    max_active_runs=1,
) as dag:

    # Define environment variables for the pipeline
    job_name = 'geospatial-dataflow-job'
    gcs_geojson_file = 'gs://your-bucket/path-to-your-geojson-file.geojson'
    api_url = 'https://example.com/api/geospatial-data'
    dataset = 'your_dataset_id'
    table = 'your_table_id'

    # Define the Apache Beam pipeline as a Dataflow job
    dataflow_task = DataflowCreateJobOperator(
        task_id="run_dataflow_geospatial_pipeline",
        job_name=job_name,
        py_file='gs://your-bucket/path-to-beam-pipeline.py',  # Path to your Apache Beam Python script
        options={
            'project': '{{ dag_run.conf["project"] if dag_run else params.project }}',
            'region': '{{ dag_run.conf["region"] if dag_run else params.region }}',
            'temp_location': '{{ dag_run.conf["temp_location"] if dag_run else params.temp_location }}',
            'staging_location': '{{ dag_run.conf["staging_location"] if dag_run else params.staging_location }}',
            'api_url': api_url,
            'geojson_file': gcs_geojson_file,
            'dataset': dataset,
            'table': table,
            'runner': 'DataflowRunner',
        },
        location='{{ dag_run.conf["region"] if dag_run else params.region }}',
        wait_until_finished=True,  # Optional: Set to False for async job submission
    )

# End of DAG
