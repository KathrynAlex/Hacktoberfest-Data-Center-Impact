---
name: environmental-interest
description: Use ONLY when the user needs to find areas of environmental interest, such as SSSIs (Sites of Special Scientific Interest), protected landscapes, or conservation areas.
---

# Environmental Interest Finder

This skill helps identify and analyze areas of environmental interest.

## Workflow
1. **Identify Target Area**: Either a bounding box (`minLon,minLat,maxLon,maxLat`) or a GeoJSON file of Point features (e.g. output from `uk-infrastructure-tracker`) to search around.
2. **Fetch Data**: Run the fetch script. It queries Natural England's OGC API layers on the Defra Data Services Platform (`https://environment.data.gov.uk/spatialdata/<dataset>/ogc/features/v1/...`), follows pagination, and tags each feature with a `designation`.

   **Command:**
   `python3 skills/environmental-interest/fetch_env.py --around <points.geojson> [--buffer 0.25] --out <env.geojson>`
   or
   `python3 skills/environmental-interest/fetch_env.py --bbox <minLon,minLat,maxLon,maxLat> --out <env.geojson>`

   Optional: `--layers sssi,sac,spa,ramsar,nnr,lnr,np,aonb` (default: all), `--max-per-layer 500`.
3. **Extract Details**: Each feature has `name` and `designation`, plus layer-specific fields (e.g. `ref_code`, `sac_code`, `hyperlink`).
4. **Synthesize Results**: Summarise the sites found by designation. The output GeoJSON is a map layer file usable by `generate-data-center-impact-map`.

## Coverage & Limits
- **England only.** Scotland (NatureScot), Wales (NRW) and Northern Ireland (DAERA) are not covered.
- Ancient Woodland has no OGC endpoint at the moment, so it isn't fetched.
- Large bounding boxes (e.g. "National") return heavy geometry; prefer `--around` with a buffer.

## Key Terms for Search
- "SSSI" (Sites of Special Scientific Interest)
- "SAC" (Special Areas of Conservation)
- "SPA" (Special Protection Areas)
- "RAMSAR" sites
- "Ancient Woodland"
- "Local Nature Reserve" (LNR)
