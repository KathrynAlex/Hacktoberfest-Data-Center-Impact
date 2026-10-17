import argparse
import folium
import json

def _point_bounds(geojson):
    """[[minLat, minLon], [maxLat, maxLon]] for Point features, or None."""
    coords = [ft['geometry']['coordinates'] for ft in geojson.get('features', [])
              if ft.get('geometry') and ft['geometry'].get('type') == 'Point']
    if not coords:
        return None
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return [[min(lats), min(lons)], [max(lats), max(lons)]]

def _load(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def create_impact_map(infra_file, env_file, output="impact_map.html", cartodb_api_key=None, infra_label="Infrastructure Projects"):
    """
    Generates a map overlaying infrastructure and environmental data.
    Paths are handled relative to the current working directory.
    """
    if cartodb_api_key:
        tile_url = f"https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png?key={cartodb_api_key}"
        attr = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>'
        m = folium.Map(location=[52.0, -2.0], zoom_start=6, tiles=tile_url, attr=attr)
    else:
        # Positron basemaps don't require a key; avoids OSM tile blocks
        m = folium.Map(location=[52.0, -2.0], zoom_start=6, tiles="cartodbpositron")

    # Environmental layer first so infrastructure markers sit on top
    env_data = _load(env_file)
    if env_data:
        fields, aliases = ['name'], ['Site:']
        if any('designation' in ft.get('properties', {}) for ft in env_data.get('features', [])):
            fields, aliases = ['name', 'designation'], ['Site:', 'Designation:']
        folium.GeoJson(
            env_data,
            name="Environmental Interest",
            style_function=lambda x: {'color': 'green', 'weight': 2, 'fillOpacity': 0.4},
            tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases, localize=True)
        ).add_to(m)

    infra_data = _load(infra_file)
    if infra_data:
        folium.GeoJson(
            infra_data,
            name=infra_label,
            marker=folium.CircleMarker(radius=8, color='red', fill=True, fill_color='orange', fill_opacity=0.9),
            tooltip=folium.GeoJsonTooltip(
                fields=['name', 'applicant', 'stage'],
                aliases=['Project:', 'Applicant:', 'Stage:'],
                localize=True
            )
        ).add_to(m)

    # Zoom to the projects if there are any, else to the environmental search area
    bounds = _point_bounds(infra_data) if infra_data else None
    if not bounds and env_data and env_data.get('bbox'):
        b = env_data['bbox']
        bounds = [[b[1], b[0]], [b[3], b[2]]]
    if bounds:
        m.fit_bounds(bounds, padding=(30, 30), max_zoom=12)

    folium.LayerControl().add_to(m)
    m.save(output)
    print(f"Map successfully saved to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Overlay infrastructure projects and environmental sites on a map.")
    parser.add_argument("infra_geojson")
    parser.add_argument("env_geojson")
    parser.add_argument("output", nargs="?", default="impact_map.html")
    parser.add_argument("api_key", nargs="?", default=None, help="Optional CartoDB API key")
    parser.add_argument("--label", default="Infrastructure Projects", help="Layer name for the projects, e.g. 'Data Centres'")
    args = parser.parse_args()

    create_impact_map(args.infra_geojson, args.env_geojson, args.output, args.api_key, args.label)
