import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import storage, bigquery
import json
import requests
from datetime import datetime

# Define global variables
GCP_PROJECT = "your-gcp-project-id"
BUCKET_NAME = "your-cloud-storage-bucket"
GEOJSON_FILE_PATH = "gs://your-cloud-storage-bucket/states.geojson"
BIGQUERY_DATASET = "geotech_dataset"
BIGQUERY_TABLE = "geospatial_data"

# BigQuery schema
BIGQUERY_SCHEMA = [
    {"name": "state_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "polygon_coords", "type": "GEOGRAPHY", "mode": "REQUIRED"},
    {"name": "population", "type": "INT64", "mode": "NULLABLE"},
    {"name": "area", "type": "FLOAT", "mode": "NULLABLE"},
]

def fetch_geojson_from_storage():
    """
    Fetch GeoJSON data from Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(GEOJSON_FILE_PATH.split("/")[-1])
    
    # Download and return the GeoJSON content
    geojson_content = blob.download_as_string()
    return json.loads(geojson_content)


def fetch_population_data(api_url):
    """
    Fetch population data from an external API.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API: {api_url}")


def process_geojson(geojson_data, population_data):
    """
    Process GeoJSON data, enrich with population data and prepare for BigQuery ingestion.
    """
    processed_data = []
    
    for feature in geojson_data['features']:
        state_name = feature['properties']['name']
        polygon_coords = json.dumps(feature['geometry'])
        area = feature['properties'].get('area', None)
        population = population_data.get(state_name, None)

        processed_data.append({
            'state_name': state_name,
            'polygon_coords': f"POLYGON(({polygon_coords}))",
            'population': population,
            'area': area
        })
    
    return processed_data


class WriteToBigQuery(beam.DoFn):
    def __init__(self, project, dataset, table, schema):
        super().__init__()
        self.project = project
        self.dataset = dataset
        self.table = table
        self.schema = schema

    def start_bundle(self):
        self.client = bigquery.Client(project=self.project)

    def process(self, element):
        table_ref = self.client.dataset(self.dataset).table(self.table)
        errors = self.client.insert_rows_json(table_ref, [element])
        
        if errors:
            raise Exception(f"BigQuery insert errors: {errors}")


def run_pipeline():
    """
    Apache Beam pipeline for the ETL process.
    """
    # Fetch data from external sources
    geojson_data = fetch_geojson_from_storage()
    population_data = fetch_population_data("https://api.example.com/population_data")

    # Beam pipeline options
    pipeline_options = PipelineOptions(
        project=GCP_PROJECT,
        temp_location=f"gs://{BUCKET_NAME}/temp",
        region="your-gcp-region",
        runner="DataflowRunner"  # You can also use DirectRunner for local execution
    )

    with beam.Pipeline(options=pipeline_options) as p:
        # Create pipeline
        (
            p
            | 'Start' >> beam.Create([geojson_data])
            | 'Process GeoJSON' >> beam.FlatMap(lambda geojson: process_geojson(geojson, population_data))
            | 'Write to BigQuery' >> beam.ParDo(WriteToBigQuery(GCP_PROJECT, BIGQUERY_DATASET, BIGQUERY_TABLE, BIGQUERY_SCHEMA))
        )

if __name__ == "__main__":
    run_pipeline()
