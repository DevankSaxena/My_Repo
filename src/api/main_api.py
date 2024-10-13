import os
import json
from flask import Flask, request, jsonify
from google.cloud import bigquery
from google.auth import default

# Initialize Flask app
app = Flask(__name__)

# Set up Google Cloud authentication and BigQuery client
_, project_id = default()
client = bigquery.Client(project=project_id)

# Constants
DATASET_NAME = "geotech_dataset"
TABLE_NAME = "geospatial_data"


@app.route('/')
def index():
    return jsonify({"message": "Welcome to the GeoTech Data Intelligence API!"})


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """
    API to fetch all states and their geospatial data from BigQuery.
    """
    query = f"""
        SELECT state_name, ST_AsText(polygon_coords) as polygon_coords, population, area
        FROM `{project_id}.{DATASET_NAME}.{TABLE_NAME}`
        ORDER BY state_name
    """
    query_job = client.query(query)
    results = query_job.result()

    states = []
    for row in results:
        states.append({
            "state_name": row.state_name,
            "polygon_coords": row.polygon_coords,
            "population": row.population,
            "area": row.area
        })

    return jsonify({"states": states})


@app.route('/api/v1/states/<state_name>', methods=['GET'])
def get_state_by_name(state_name):
    """
    API to fetch the details of a specific state by its name.
    """
    query = f"""
        SELECT state_name, ST_AsText(polygon_coords) as polygon_coords, population, area
        FROM `{project_id}.{DATASET_NAME}.{TABLE_NAME}`
        WHERE LOWER(state_name) = @state_name
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("state_name", "STRING", state_name.lower())]
    )

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    state_data = []
    for row in results:
        state_data.append({
            "state_name": row.state_name,
            "polygon_coords": row.polygon_coords,
            "population": row.population,
            "area": row.area
        })

    if not state_data:
        return jsonify({"error": "State not found"}), 404

    return jsonify({"state": state_data[0]})


@app.route('/api/v1/states/filter', methods=['GET'])
def filter_states():
    """
    API to filter states based on population or area.
    Query parameters:
        min_population (optional): Minimum population filter
        max_population (optional): Maximum population filter
        min_area (optional): Minimum area filter
        max_area (optional): Maximum area filter
    """
    min_population = request.args.get('min_population')
    max_population = request.args.get('max_population')
    min_area = request.args.get('min_area')
    max_area = request.args.get('max_area')

    query = f"""
        SELECT state_name, ST_AsText(polygon_coords) as polygon_coords, population, area
        FROM `{project_id}.{DATASET_NAME}.{TABLE_NAME}`
        WHERE 1=1
    """

    # Append conditions dynamically based on provided filters
    if min_population:
        query += f" AND population >= {min_population}"
    if max_population:
        query += f" AND population <= {max_population}"
    if min_area:
        query += f" AND area >= {min_area}"
    if max_area:
        query += f" AND area <= {max_area}"

    query_job = client.query(query)
    results = query_job.result()

    filtered_states = []
    for row in results:
        filtered_states.append({
            "state_name": row.state_name,
            "polygon_coords": row.polygon_coords,
            "population": row.population,
            "area": row.area
        })

    return jsonify({"filtered_states": filtered_states})


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
