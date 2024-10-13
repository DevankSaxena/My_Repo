import json
import re
from shapely.geometry import shape, Polygon, MultiPolygon

def extract_polygon_coordinates(geojson_geometry):
    """
    Extracts polygon coordinates from a GeoJSON geometry field.
    This function handles both Polygon and MultiPolygon geometries.

    Args:
        geojson_geometry (dict): A GeoJSON geometry object.

    Returns:
        str: The polygon coordinates in WKT format.
    """
    geom = shape(geojson_geometry)
    if isinstance(geom, Polygon):
        return geom.wkt
    elif isinstance(geom, MultiPolygon):
        return geom.wkt
    else:
        raise ValueError("Unsupported geometry type: {}".format(type(geojson_geometry)))

def clean_state_name(state_name):
    """
    Cleans up the state name by removing any unwanted characters or spaces.

    Args:
        state_name (str): The raw state name.

    Returns:
        str: The cleaned state name.
    """
    # Remove any non-alphanumeric characters and extra spaces
    return re.sub(r'[^a-zA-Z0-9\s]', '', state_name).strip()

def enrich_data_with_population(geojson_data, population_data):
    """
    Enriches GeoJSON data with population data from an external source.

    Args:
        geojson_data (dict): GeoJSON object containing geospatial information.
        population_data (dict): A dictionary where keys are state names and values are population numbers.

    Returns:
        list: A list of enriched geospatial data with population information.
    """
    enriched_data = []

    for feature in geojson_data['features']:
        state_name = clean_state_name(feature['properties'].get('name', 'Unknown'))
        geometry = feature['geometry']
        polygon_coords = extract_polygon_coordinates(geometry)
        area = feature['properties'].get('area', None)
        
        # Get population data for the state (if available)
        population = population_data.get(state_name, None)

        enriched_data.append({
            'state_name': state_name,
            'polygon_coords': polygon_coords,
            'population': population,
            'area': area
        })
    
    return enriched_data

def validate_geojson(geojson_data):
    """
    Validates the GeoJSON data format to ensure it meets the required structure.

    Args:
        geojson_data (dict): The GeoJSON data to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    required_fields = ['type', 'features']
    
    if not all(field in geojson_data for field in required_fields):
        raise ValueError("GeoJSON is missing required fields.")
    
    if geojson_data['type'] != 'FeatureCollection':
        raise ValueError("Invalid GeoJSON type. Expected 'FeatureCollection'.")

    for feature in geojson_data['features']:
        if 'geometry' not in feature or 'properties' not in feature:
            raise ValueError("Invalid GeoJSON feature structure.")

    return True

def filter_geojson_by_area(geojson_data, min_area=None, max_area=None):
    """
    Filters GeoJSON features based on area size.

    Args:
        geojson_data (dict): A GeoJSON object.
        min_area (float): Minimum area threshold for filtering (optional).
        max_area (float): Maximum area threshold for filtering (optional).

    Returns:
        dict: Filtered GeoJSON data.
    """
    filtered_features = []

    for feature in geojson_data['features']:
        area = feature['properties'].get('area', None)
        
        if area is not None:
            if (min_area is not None and area < min_area) or (max_area is not None and area > max_area):
                continue
        
        filtered_features.append(feature)
    
    # Return filtered GeoJSON
    return {
        "type": geojson_data['type'],
        "features": filtered_features
    }
