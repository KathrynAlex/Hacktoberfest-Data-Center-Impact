import folium
import json
import os
import sys

def create_impact_map(dc_file, env_file, output="impact_map.html", cartodb_api_key=None):
    """
    Generates a map overlaying infrastructure and environmental data.
    Paths are handled relative to the current working directory.
    """
    # Set up tiles
    if cartodb_api_key:
        # Use CartoDB Positron with API Key
        # Format: https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png?key=YOUR_KEY
        tile_url = f"https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png?key={cartodb_api_key}"
        attr = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>'
    else:
        # Fallback to standard OpenStreetMap if no key provided
        tile_url = "OpenStreetMap"
        attr = "OpenStreetMap contributors"

    m = folium.Map(
        location=[52.0, -2.0], 
        zoom_start=6, 
        tiles=tile_url, 
        attr=attr
    )
    
    # Data Centers Layer
    try:
        with open(dc_file, 'r') as f:
            dc_data = json.load(f)
            folium.GeoJson(
                dc_data, 
                name="Data Center Applications", 
                style_function=lambda x: {'color': 'red', 'weight': 3},
                tooltip=folium.GeoJsonTooltip(
                    fields=['name', 'applicant', 'stage'], 
                    aliases=['Project:', 'Applicant:', 'Stage:'],
                    localize=True
                )
            ).add_to(m)
    except Exception as e:
        print(f"Error loading DC file {dc_file}: {e}")
        
    # Environmental Sites Layer
    try:
        with open(env_file, 'r') as f:
            env_data = json.load(f)
            folium.GeoJson(
                env_data, 
                name="Environmental Interest", 
                style_function=lambda x: {'color': 'green', 'weight': 2, 'fillOpacity': 0.4},
                tooltip=folium.GeoJsonTooltip(
                    fields=['name'], 
                    aliases=['Site:'],
                    localize=True
                )
            ).add_to(m)
    except Exception as e:
        print(f"Error loading Env file {env_file}: {e}")
        
    folium.LayerControl().add_to(m)
    m.save(output)
    print(f"Map successfully saved to {output}")

if __name__ == "__main__":
    # Expects arguments: python3 render_map.py <dc_geojson> <env_geojson> [output_file] [api_key]
    if len(sys.argv) < 3:
        print("Usage: python3 render_map.py <dc_geojson> <env_geojson> [output_file] [api_key]")
        sys.exit(1)
        
    dc_path = sys.argv[1]
    env_path = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else "impact_map.html"
    api_key = sys.argv[4] if len(sys.argv) > 4 else None
    
    create_impact_map(dc_path, env_path, out_path, api_key)
