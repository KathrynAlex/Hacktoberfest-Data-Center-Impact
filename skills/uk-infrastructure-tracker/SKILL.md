---
skill_id: uk.infra.tracker
version: 1.0.0
capabilities:
  - name: extract_infrastructure_geojson
    description: Search UK national infrastructure for projects and return as GeoJSON
    inputs:
      scope:
        type: string
        description: The geographic scope (e.g., "National" or "South West")
        default: "National"
      query:
        type: string
        description: The type of project to search for (e.g., "data centres", "roads")
        required: true
      format:
        type: string
        description: Output format
        default: "geojson"
    outputs:
      type: application/geo+json
      description: A GeoJSON FeatureCollection of matching infrastructure projects
    tool: "python3 uk_dc_tracker.py --scope {scope} --query {query} --format {format}"
---

# UK Infrastructure Tracker Skill


This skill allows agents to search the UK National Infrastructure register for specific types of projects within a given location and output the results as a GeoJSON dataset for mapping and analysis.

## Purpose
To extract a structured, mapping-ready list of nationally significant infrastructure projects based on a "thing" (keyword) and a "location" (scope).

## Tooling
The primary tool is the `uk_dc_tracker.py` coordinator script.

**Command:**
`python3 uk_dc_tracker.py --scope <SCOPE> --query <QUERY> --format geojson`

### Arguments:
- `--scope`: 
    - `National`: Searches the entire UK national register.
    - `[Region Name]`: Filters results to a specific region (e.g., "South East", "South West", "London").
- `--query`: The natural language description of the "thing" to search for (e.g., "data centres", "road projects", "energy hubs"). The tool uses internal keyword mapping to broaden the search.
- `--format`: Must be set to `geojson` to produce mapping-compatible output.

## Operational Workflow

1. **Parameter Gathering**:
   If the user's request is missing details, the agent must clarify:
   - **Where?** (Default to "National" if unspecified).
   - **What?** (The type of project/infrastructure).

2. **Execution**:
   Run the command using the gathered parameters.

3. **Output Handling**:
   - The tool returns a GeoJSON `FeatureCollection`.
   - Each feature contains `geometry` (Point coordinates) and `properties` (name, applicant, stage, description, ref).

4. **Empty Results**:
   If no results are found, the agent should inform the user that no *nationally significant* projects match the criteria and suggest that the project may be handled at a local council level.

## Setup Requirements
- Python 3.x
- `requests` library installed (`python3 -m pip install requests`)
- Local cache file `national_projects_full.json` (automatically created by `fetch_national.py` during the first run of the tracker).
