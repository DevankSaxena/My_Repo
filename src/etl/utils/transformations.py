import json
import csv

# Load GeoJSON file , if required we can convert the complex geojson files into CSV files that can be loaded into Bigquery.
geojson_file = 'states.geojson'
output_csv = 'states_bigquery.csv'

def geojson_to_wkt(geometry):
    # Convert GeoJSON geometry to WKT (Well-Known Text) for BigQuery GEOGRAPHY type
    if geometry['type'] == 'MultiPolygon':
        # Example WKT format: MULTIPOLYGON (((x1 y1, x2 y2, ...)))
        coordinates = geometry['coordinates']
        polygons = []
        for polygon in coordinates:
            rings = []
            for ring in polygon:
                ring_coords = ', '.join(f"{coord[0]} {coord[1]}" for coord in ring)
                rings.append(f"({ring_coords})")
            polygons.append(f"({', '.join(rings)})")
        return f"MULTIPOLYGON ({', '.join(polygons)})"
    return None

# Open CSV for writing
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['STATEFP', 'STUSPS', 'NAME', 'geometry']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    with open(geojson_file) as f:
        geojson_data = json.load(f)
        for feature in geojson_data['features']:
            properties = feature['properties']
            geometry = geojson_to_wkt(feature['geometry'])
            writer.writerow({
                'STATEFP': properties['STATEFP'],
                'STUSPS': properties['STUSPS'],
                'NAME': properties['NAME'],
                'geometry': geometry
            })

print(f"GeoJSON data successfully converted to {output_csv}")
