import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
import json
from shapely.geometry import shape
from shapely.wkt import dumps as wkt_dumps
from google.cloud import bigquery

class FetchGeoJsonFromAPI(beam.DoFn):
    def process(self, api_url):
        """
        Fetch geospatial data from API and return as a dictionary
        """
        response = requests.get(api_url)
        if response.status_code == 200:
            return [response.json()]  # Output the GeoJSON
        else:
            raise Exception(f"Failed to fetch data from {api_url}: {response.status_code}")

class TransformGeoJsonToBigQuery(beam.DoFn):
    def process(self, geojson_data):
        """
        Transform GeoJSON data into a format suitable for BigQuery.
        Extract geometries and convert to WKT format.
        """
        for feature in geojson_data['features']:
            properties = feature['properties']
            geometry = feature['geometry']

            # Convert the geometry to WKT format
            geom_wkt = wkt_dumps(shape(geometry))

            # Create output dictionary with WKT and properties
            yield {
                'geometry': geom_wkt,
                **properties  # Add other properties to the output
            }

class LoadToBigQuery(beam.PTransform):
    def __init__(self, dataset, table):
        self.dataset = dataset
        self.table = table

    def expand(self, pcoll):
        return (
                pcoll
                | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
            f'{self.dataset}.{self.table}',
            schema=self.table_schema(),
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
        )

    def table_schema(self):
        """Define the BigQuery table schema."""
        return {
            'fields': [
                {'name': 'geometry', 'type': 'GEOGRAPHY'},
                {'name': 'NAME', 'type': 'STRING'},
                {'name': 'STATEFP', 'type': 'STRING'},
                {'name': 'STUSPS', 'type': 'STRING'}# Example attribute
                # Add other fields based on the properties in the GeoJSON
            ]
        }

def run(api_url, geojson_file, dataset, table, project, region, temp_location):
    """
    Run the Apache Beam pipeline for transforming and loading geospatial data into BigQuery.
    """
    options = PipelineOptions(
        runner='DataflowRunner',
        project=project,
        region=region,
        temp_location=temp_location,
        save_main_session=True
    )

    with beam.Pipeline(options=options) as pipeline:
        # Read GeoJSON from a file (local or GCS)
        geojson_from_file = (
                pipeline
                | 'ReadGeoJSONFile' >> beam.io.ReadFromText(geojson_file)
                | 'ParseGeoJSONFile' >> beam.Map(json.loads)
                | 'TransformGeoJsonFile' >> beam.ParDo(TransformGeoJsonToBigQuery())
        )

        # Fetch GeoJSON from API and transform
        geojson_from_api = (
                pipeline
                | 'CreateAPIUrl' >> beam.Create([api_url])
                | 'FetchGeoJsonFromAPI' >> beam.ParDo(FetchGeoJsonFromAPI())
                | 'TransformGeoJsonAPI' >> beam.ParDo(TransformGeoJsonToBigQuery())
        )

        # Combine the data from both file and API
        all_geojson_data = (geojson_from_file, geojson_from_api) | beam.Flatten()

        # Write the combined transformed data into BigQuery
        all_geojson_data | 'LoadDataIntoBigQuery' >> LoadToBigQuery(dataset, table)

if __name__ == '__main__':
    api_url = 'https://example.com/api/geospatial-data'
    geojson_file = 'gs://your-bucket/path-to-your-geojson-file.geojson'
    dataset = 'your_dataset_id'
    table = 'your_table_id'
    project = 'your_gcp_project_id'
    region = 'your_region'
    temp_location = 'gs://your-bucket/temp'

    run(api_url, geojson_file, dataset, table, project, region, temp_location)
