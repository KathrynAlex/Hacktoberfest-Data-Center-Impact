import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

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
        result = subprocess.run([sys.executable, FETCH_SCRIPT], capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def is_cache_stale():
    """Returns True if the cache file is older than 24 hours or doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return True
    mtime = os.path.getmtime(DATA_FILE)
    return datetime.now().timestamp() - mtime > 86400

def convert_to_geojson(projects):
    features = []
    for p in projects:
        if p['coords']['lat'] is None or p['coords']['lon'] is None:
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
    if is_cache_stale():
        success, msg = run_fetch()
        if not success:
            return {"error": f"Failed to update data: {msg}"}

    try:
        with open(DATA_FILE, 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        return {"error": "Cache missing. Please run fetch_national.py."}

    keywords = []
    if query:
        query_lower = query.lower()
        matched_categories = []
        for category, terms in INFRA_KEYWORDS.items():
            if any(term in query_lower for term in terms):
                matched_categories.append(category)

        # Priority: Use specific categories. If "broadband" matches "road",
        # the AI should be smart, but we can avoid collisions by ensuring
        # a better matching logic. For now, we use all matched categories' terms.
        for cat in matched_categories:
            keywords.extend(INFRA_KEYWORDS[cat])
    
    if not keywords and query:
        keywords = [query]

    from search import search_projects
    results = search_projects(keywords=keywords, region=None if scope.lower() == "national" else scope)
    
    if output_format == "geojson":
        return convert_to_geojson(results)
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="National")
    parser.add_argument("--query", help="What to search for")
    parser.add_argument("--format", default="geojson")
    
    args = parser.parse_args()
    
    result = execute_tracker(scope=args.scope, query=args.query, output_format=args.format)
    print(json.dumps(result, indent=2))
