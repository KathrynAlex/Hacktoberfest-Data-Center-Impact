# Hacktoberfest-Data-Center-Impact
Open source repo for Hacktober 2026

Finds UK nationally significant infrastructure projects (data centres by default) and maps them against nearby protected environmental sites.

## How it works

An agent (`.opencode/agent/infrastructure-impact-analyzer.md`) asks for a region and infrastructure type, then chains three skills:

1. **`uk-infrastructure-tracker`** – searches the [National Infrastructure register](https://nationalinfrastructure.gov.uk) and outputs matching projects as GeoJSON points.
2. **`environmental-interest`** – fetches protected sites around those projects from Natural England's OGC API on the [Defra Data Services Platform](https://environment.data.gov.uk). The search area is the projects' extent plus a 0.25° buffer.
3. **`generate-data-center-impact-map`** – overlays both on a folium HTML map.

Layers fetched: SSSI, SAC, SPA, Ramsar, National Nature Reserves, Local Nature Reserves, National Parks and National Landscapes (AONB).

## Requirements

- Python 3.9+
- `pip install folium requests`
- Network access to `environment.data.gov.uk`, `nationalinfrastructure.gov.uk` and `basemaps.cartocdn.com`

## Usage

Via opencode: select the `infrastructure-impact-analyzer` agent and tell it a region and what to look for.

Or run the steps by hand from the repo root:

```sh
python3 skills/uk-infrastructure-tracker/uk_dc_tracker.py --scope "North West" --query "energy" --format geojson > north_west_energy_projects.geojson
python3 skills/environmental-interest/fetch_env.py --around north_west_energy_projects.geojson --out north_west_energy_env.geojson
python3 skills/generate-data-center-impact-map/render_map.py north_west_energy_projects.geojson north_west_energy_env.geojson north_west_energy_impact_map.html --label "Energy"
python3 -m http.server 8000
```

Then open http://localhost:8000/north_west_energy_impact_map.html.

- `--scope`: a region name (e.g. "South East", "London") or "National".
- `--query`: "data centres", "roads", "energy", "rail" and "water" have keyword mappings. Anything else is used as a plain keyword.
- `fetch_env.py` also takes `--bbox minLon,minLat,maxLon,maxLat`, `--buffer`, `--layers sssi,sac,...` and `--max-per-layer`.
- `render_map.py` takes an optional CartoDB API key as the 4th positional argument.

## Known problems

- **Large maps.** Full-resolution protected-site polygons are heavy. A North West energy map with 10 projects came out at 52MB. Geometry simplification (e.g. `shapely`) or a smaller `--buffer` would help.
- **England only.** The environmental data is Natural England's. Scotland (NatureScot), Wales (NRW) and Northern Ireland (DAERA) aren't covered, so projects there get no environmental layer.
- **No ancient woodland.** No OGC endpoint was found for it.
- **Nationally significant projects only.** Most data centres go through local council planning and won't appear in the register. An empty result doesn't mean nothing is planned.
- **CartoDB tiles may need a key.** folium warns that CartoDB "now require an API key". Keyless Positron tiles currently load fine. If they stop, pass a key from https://carto.com/basemaps/apikey/.
- **No proximity analysis yet.** The map shows overlaps visually, but nothing calculates distances between projects and sites.
- **Per-layer cap.** `fetch_env.py` stops at 500 features per layer by default. Very wide searches may be truncated silently, apart from the counts printed to stderr.
- **No tests.**
- **LibreSSL warning.** macOS system Python prints a urllib3 `NotOpenSSLWarning`. It's harmless; set `PYTHONWARNINGS=ignore` to hide it.
