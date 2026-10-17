---
name: DC Impact Analyzer
description: Orchestrates the discovery of UK data center infrastructure and maps their potential environmental impacts using national registers and environmental APIs.
version: 1.0.0
author: opencode
---

# DC Impact Analyzer Agent

## System Requirements
- **Python 3.9+**
- **Required Python Libraries:**
  - `folium` (for map generation)
  - `requests` (for API interaction)
  - `branca` (dependency for folium)
- **Network Access:** Ability to reach `environment.data.gov.uk` and `nationalinfrastructure.gov.uk`.
- **Optional:** A [CartoDB API Key](https://carto.com/basemaps/apikey/) for high-quality map tiles.

## Capabilities
1. **Infrastructure Discovery**: Uses the `uk-infrastructure-tracker` skill to find data center projects in a specific UK region.
2. **Environmental Analysis**: Uses the `environmental-interest` skill to fetch protected sites (SSSI, SAC, SPA) within a bounding box.
3. **Impact Mapping**: Uses the `generate-data-center-impact-map` skill to overlay these datasets into a visual HTML report.

## Workflow
1. **Region Identification**: Ask the user for the target UK region (e.g., "South East", "North West").
2. **API Key Check**: Ask the user if they have a CartoDB API key to ensure the tiles load correctly.
3. **Data Collection**:
    - Run `uk_dc_tracker.py` for the specified region.
    - Determine the bounding box for the region and fetch environmental data.
4. **Visualisation**:
    - Run `render_map.py` using the generated GeoJSON files.
    - **Serving the Map**: Since local file paths can cause CORS or loading issues with tiles, launch the `serve_map.py` utility to host the result on a local server.
    - Provide the user with the local URL (e.g., `http://localhost:8000/south_east_impact_map.html`).

## Skill Commands Reference
- **Search**: `python3 skills/uk-infrastructure-tracker/uk_dc_tracker.py --scope "<REGION>"`
- **Map**: `python3 skills/generate-data-center-impact-map/render_map.py <infra_geojson> <env_geojson> <output_html> [api_key]`
- **Serve**: `python3 serve_map.py [port]`
