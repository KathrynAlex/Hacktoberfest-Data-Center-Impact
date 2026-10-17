import folium
import json
import os
import sys

def create_impact_map(dc_file, env_file, output="impact_map.html"):
    """
    Generates a map overlaying infrastructure and environmental data.
    Paths are handled relative to the current working directory.
    """
    # Centering the map roughly on the UK
    m = folium.Map(location=[52.0, -2.0], zoom_start=6, tiles="CartoDB positron")
    
    # Data Centers Layer
    try:
        with open(dc_file, 'r') as f:
            dc_data = json.load(f)
            # Ensure we are dealing with a FeatureCollection
            features = dc_data['features'] if 'features' in dc_data else dc_data
            
            folium.GeoJson(
                dc_data, 
                name="Data Center Applications", 
                style_function=lambda x: {'color': 'red'},
                tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Project:'])
            ).add_to(m)
    except Exception as e:
        print(f"Error loading DC file {dc_file}: {e}")
        
    # Environmental Sites Layer
    try:
        with open(env_file, 'r') as f:
            env_data = json.load(f)
            features = env_data['features'] if 'features' in env_data else env_data
            
            folium.GeoJson(
                env_data, 
                name="Environmental Interest", 
                style_function=lambda x: {'color': 'green'},
                tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Site:'])
            ).add_to(m)
    except Exception as e:
        print(f"Error loading Env file {env_file}: {e}")
        
    folium.LayerControl().add_to(m)
    m.save(output)
    print(f"Map successfully saved to {output}")

if __name__ == "__main__":
    # Expects arguments: python3 render_map.py <dc_geojson> <env_geojson> [output_file]
    if len(sys.argv) < 3:
        print("Usage: python3 render_map.py <dc_geojson> <env_geojson> [output_file]")
        sys.exit(1)
        
    dc_path = sys.argv[1]
    env_path = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else "impact_map.html"
    
    create_impact_map(dc_path, env_path, out_path)
