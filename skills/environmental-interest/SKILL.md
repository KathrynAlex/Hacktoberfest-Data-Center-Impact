---
name: environmental-interest
description: Use ONLY when the user needs to find areas of environmental interest, such as SSSIs (Sites of Special Scientific Interest), protected landscapes, or conservation areas.
---

# Environmental Interest Finder

This skill helps identify and analyze areas of environmental interest.

## Workflow
1. **Identify Target Area**: Determine the geographic region or coordinates the user is interested in. If coordinates are provided, first verify the location (city/region/country) to ensure the correct regional databases are used.
2. **Search Data Sources**: To find coordinates and boundaries, prioritize using the official UK Environmental Data API: `https://environment.data.gov.uk/geoservices/datasets/e819098e-e248-4a8f-b684-5a21ca521b9b/ogc/features/v1/collections/{collectionId}/search` to retrieve GeoJSON files for various environmental interest sites. Use `webfetch` to query the API. For visual verification and layer identification, use MAGIC Maps (https://magic.defra.gov.uk).
3. **Extract Details**: Look for:
   - Site name and designation (e.g., SSSI, SAC, SPA).
   - Boundaries or coordinate data.
   - Reasons for designation (flora, fauna, geological features).
4. **Synthesize Results**: Present the findings as a list of site names and their bounding areas (e.g., coordinates, boundaries, or general geographic extent). Include the relevant map layer definitions (e.g., MAGIC layer IDs or Natura 2000 classifications) used to locate the site. Save the resulting filtered GeoJSON data as a map layer file in `~/maps/`.

## Key Terms for Search
- "SSSI" (Sites of Special Scientific Interest)
- "SAC" (Special Areas of Conservation)
- "SPA" (Special Protection Areas)
- "RAMSAR" sites
- "Ancient Woodland"
- "Local Nature Reserve" (LNR)
