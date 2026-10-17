import json
import os
import re
from math import radians, cos, sin, asin, sqrt

# Absolute path based on script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "national_projects_full.json")

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * 6371

def load_projects():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def search_projects(keywords=None, region=None, max_distance_km=None, user_coords=None):
    projects = load_projects()
    results = []

    for p in projects:
        if region and (not p['region'] or p['region'].lower() != region.lower()):
            continue
        
        if keywords:
            search_text = f"{p['name']} {p['description']}".lower()
            matched = False
            for k in keywords:
                if re.search(rf'\b{re.escape(k.lower())}\b', search_text):
                    matched = True
                    break
            if not matched:
                continue
        
        if max_distance_km and user_coords:
            if p['coords']['lat'] is None or p['coords']['lon'] is None:
                continue
            
            dist = haversine(
                user_coords['lon'], user_coords['lat'], 
                p['coords']['lon'], p['coords']['lat']
            )
            if dist > max_distance_km:
                continue
            p['distance_km'] = round(dist, 2)

        results.append(p)
    
    return results

if __name__ == "__main__":
    import sys
    import json as j
    kws = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    reg = sys.argv[2] if len(sys.argv) > 2 else None
    print(j.dumps(search_projects(keywords=kws, region=reg), indent=2))
