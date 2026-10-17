---
name: generate-data-center-impact-map
description: Use ONLY when the user wants to generate a map visualizing data center planning applications and nearby sites of environmental interest.
---

# Generate Data Center Impact Map

This skill guides the agent in creating a map that overlays data center planning applications with environmental interest sites.

## Workflow

1. **Data Collection**:
   - Locate GeoJSON files for data center planning applications.
   - Locate GeoJSON files for sites of environmental interest (e.g., SSSIs, AONBs). Use the skill environmental-interest to generate the GeoJSON for sites of environmental interest.
   - If data is in CSV or other formats, convert them to GeoJSON using a script.

2. **Map Generation**:
   - Use a Python script (utilizing `folium`) to render the map.
   - Use distinct colors for different layers:
     - Planning Applications: Red/Orange.
     - Environmental Sites: Green.
   - Use `CartoDB positron` as the tile provider to avoid OpenStreetMap access blocks.

3. **Analysis**:
   - Identify overlaps or close proximities (buffers) between the data center sites and environmental zones.

## Implementation Reference
The following Python template should be used for the render:

**Command:**
`python3 render_map.py <dc_file> <env_file> <output_file> [cartodb_api_key]`

The script handles the overlay of GeoJSON layers and can use a CartoDB API key to ensure high-quality base tiles load without restrictions.
