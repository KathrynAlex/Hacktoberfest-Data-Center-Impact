---
name: environmental-interest
description: Use ONLY when the user needs to find areas of environmental interest, such as SSSIs (Sites of Special Scientific Interest), protected landscapes, or conservation areas.
---

# Environmental Interest Finder

This skill helps identify and analyze areas of environmental interest.

## Workflow
1. **Identify Target Area**: Determine the geographic region or coordinates. For API requests, define a bounding box (`bbox=[minLon,minLat,maxLon,maxLat]`) to avoid oversized responses.
2. **Search Data Sources**: Query the official UK Environmental Data API.
   - **Endpoint**: `https://environment.data.gov.uk/geoservices/datasets/e819098e-e248-4a8f-b684-5a21ca521b9b/ogc/features/v1/collections/{collectionId}/items`
   - **Format**: Use `f=json` to retrieve GeoJSON data.
   - **Filtering**: Always include a `bbox` parameter and a `limit` (e.g., `limit=100`) to ensure the request is processed successfully.
3. **Extract Details**: Look for:
   - Site name and designation (e.g., SSSI, SAC, SPA).
   - Boundaries or coordinate data.
   - Reasons for designation (flora, fauna, geological features).
4. **Synthesize Results**: Present the findings as a list of site names and their bounding areas. Save the resulting filtered GeoJSON data as a map layer file in the current working directory.

## Key Terms for Search
- "SSSI" (Sites of Special Scientific Interest)
- "SAC" (Special Areas of Conservation)
- "SPA" (Special Protection Areas)
- "RAMSAR" sites
- "Ancient Woodland"
- "Local Nature Reserve" (LNR)
