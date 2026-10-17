import csv
import json
import requests
import os
from datetime import datetime

# Use absolute path based on script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_URL = "https://national-infrastructure-consenting.planninginspectorate.gov.uk/api/applications-download"
OUTPUT_FILE = os.path.join(BASE_DIR, "national_projects_full.json")

def fetch_all():
    print(f"Fetching all data from {CSV_URL}...")
    response = requests.get(CSV_URL, timeout=30)
    response.raise_for_status()
    
    content = response.content.decode('utf-8-sig')
    lines = content.splitlines()
    reader = csv.DictReader(lines)
    
    all_projects = []
    
    for row in reader:
        coords_raw = row.get('GPS co-ordinates', '')
        lat, lon = None, None
        if coords_raw:
            try:
                clean_coords = coords_raw.replace("'", "").strip()
                lon, lat = map(float, clean_coords.split(','))
            except (ValueError, IndexError):
                pass

        project = {
            "ref": row.get('Project reference'),
            "name": row.get('Project name'),
            "applicant": row.get('Applicant name'),
            "region": row.get('Region'),
            "location": row.get('Location'),
            "coords": {
                "lat": lat,
                "lon": lon
            },
            "stage": row.get('Stage'),
            "description": row.get('Description'),
            "dates": {
                "application": row.get('Date of application'),
                "decision": row.get('Date of decision'),
                "withdrawn": row.get('Date withdrawn')
            },
            "last_updated": datetime.now().isoformat()
        }
        all_projects.append(project)

    print(f"Successfully mirrored {len(all_projects)} projects.")
    return all_projects

if __name__ == "__main__":
    data = fetch_all()
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved full dataset to {OUTPUT_FILE}")
