import json
import os
import subprocess
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FETCH_SCRIPT = os.path.join(BASE_DIR, "fetch_national.py")
SEARCH_SCRIPT = os.path.join(BASE_DIR, "search.py")
DATA_FILE = os.path.join(BASE_DIR, "national_projects_full.json")

# Keyword mapping for AI inference
INFRA_KEYWORDS = {
    "data_centre": ["data centre", "data center", "compute", "it load", "hyperscale", "digital infrastructure"],
    "roads": ["road", "highway", "motorway", "transport", "junction", "bypass"],
    "energy": ["energy", "solar", "wind", "nuclear", "battery", "bess", "grid", "electricity"],
    "rail": ["rail", "train", "track", "station", "viaduct"],
    "water": ["water", "reservoir", "sewage", "pipeline"]
}

def run_fetch():
    """Updates the local data cache."""
    try:
        result = subprocess.run(["python3", FETCH_SCRIPT], capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def convert_to_geojson(projects):
    """Converts internal project JSON to GeoJSON FeatureCollection."""
    features = []
    for p in projects:
        if not p['coords']['lat'] or not p['coords']['lon']:
            continue
            
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p['coords']['lon'], p['coords']['lat']]
            },
            "properties": {
                "name": p['name'],
                "applicant": p['applicant'],
                "region": p['region'],
                "stage": p['stage'],
                "description": p['description'],
                "ref": p['ref'],
                "last_updated": p.get('last_updated', ''),
                "type": "Infrastructure Project"
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

def execute_tracker(scope="National", query=None, output_format="geojson"):
    """
    Main entry point for the AI.
    scope: "National" or region.
    query: Natural language query (e.g., "road projects").
    """
    # 1. Data Refresh
    if scope.lower() == "national":
        run_fetch()

    # 2. Keyword Inference
    # AI determines which keyword set to use based on the query
    keywords = []
    if query:
        query_lower = query.lower()
        for category, terms in INFRA_KEYWORDS.items():
            if any(term in query_lower for term in terms):
                keywords.extend(terms)
                break
    
    if not keywords and query:
        # Fallback: use the query itself as a keyword
        keywords = [query]

    # 3. Search Execution
    # We call search.py via subprocess or import it. For stability, we'll import.
    from search import search_projects
    results = search_projects(keywords=keywords, region=None if scope.lower() == "national" else scope)
    
    # 4. Format Output
    if output_format == "geojson":
        return convert_to_geojson(results)
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="National")
    parser.add_argument("--query", help="What to search for (e.g. 'road projects')")
    parser.add_argument("--format", default="geojson")
    
    args = parser.parse_args()
    
    result = execute_tracker(scope=args.scope, query=args.query, output_format=args.format)
    print(json.dumps(result, indent=2))
