import argparse
import json
import sys

import requests

BASE_URL = "https://environment.data.gov.uk/spatialdata/{slug}/ogc/features/v1/collections/{collection}/items"

# Natural England designation layers (England only).
LAYERS = {
    "sssi": ("SSSI", "sites-of-special-scientific-interest-england", "Sites_of_Special_Scientific_Interest_England"),
    "sac": ("SAC", "special-areas-of-conservation-england", "Special_Areas_of_Conservation_England"),
    "spa": ("SPA", "special-protection-areas-england", "Special_Protection_Areas_England"),
    "ramsar": ("Ramsar", "ramsar-england", "Ramsar_England"),
    "nnr": ("National Nature Reserve", "national-nature-reserves-england", "National_Nature_Reserves_England"),
    "lnr": ("Local Nature Reserve", "local-nature-reserves-england", "Local_Nature_Reserves_England"),
    "np": ("National Park", "national-parks-england", "National_Parks_England"),
    "aonb": ("National Landscape (AONB)", "areas-of-outstanding-natural-beauty-england", "Areas_of_Outstanding_Natural_Beauty_England"),
}

PAGE_SIZE = 100


def bbox_from_geojson(path, buffer_deg):
    """Bounding box around all Point features in a GeoJSON file, padded by buffer_deg."""
    with open(path, 'r') as f:
        data = json.load(f)
    coords = [ft['geometry']['coordinates'] for ft in data.get('features', [])
              if ft.get('geometry') and ft['geometry'].get('type') == 'Point']
    if not coords:
        return None
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return [min(lons) - buffer_deg, min(lats) - buffer_deg, max(lons) + buffer_deg, max(lats) + buffer_deg]


def fetch_layer(key, bbox, max_features):
    """Fetch one designation layer within bbox, following 'next' links up to max_features."""
    designation, slug, collection = LAYERS[key]
    url = BASE_URL.format(slug=slug, collection=collection)
    params = {"f": "json", "bbox": ",".join(str(round(v, 5)) for v in bbox), "limit": PAGE_SIZE}
    features = []

    while url and len(features) < max_features:
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        for ft in data.get('features', []):
            props = ft['properties']
            props['designation'] = designation
            # SAC/SPA layers leave 'name' empty and use sac_name/spa_name instead
            props['name'] = props.get('name') or props.get('sac_name') or props.get('spa_name') or ''
            features.append(ft)
        url = next((l['href'] for l in data.get('links', []) if l.get('rel') == 'next'), None)
        params = None  # 'next' href already carries the query string

    return features[:max_features]


def main():
    parser = argparse.ArgumentParser(description="Fetch protected sites in England as GeoJSON.")
    area = parser.add_mutually_exclusive_group(required=True)
    area.add_argument("--bbox", help="minLon,minLat,maxLon,maxLat")
    area.add_argument("--around", help="GeoJSON file of Point features; bbox is derived from their extent")
    parser.add_argument("--buffer", type=float, default=0.25, help="Degrees to pad --around extent (default 0.25)")
    parser.add_argument("--layers", default=",".join(LAYERS), help=f"Comma-separated: {','.join(LAYERS)}")
    parser.add_argument("--max-per-layer", type=int, default=500)
    parser.add_argument("--out", required=True, help="Output GeoJSON path")
    args = parser.parse_args()

    if args.bbox:
        bbox = [float(v) for v in args.bbox.split(",")]
    else:
        bbox = bbox_from_geojson(args.around, args.buffer)
        if bbox is None:
            print(f"No Point features in {args.around}; nothing to search around.", file=sys.stderr)
            sys.exit(1)

    features = []
    for key in [k.strip().lower() for k in args.layers.split(",") if k.strip()]:
        if key not in LAYERS:
            print(f"Unknown layer '{key}', skipping.", file=sys.stderr)
            continue
        try:
            layer = fetch_layer(key, bbox, args.max_per_layer)
            print(f"{LAYERS[key][0]}: {len(layer)}", file=sys.stderr)
            features.extend(layer)
        except requests.RequestException as e:
            print(f"{LAYERS[key][0]}: failed ({e})", file=sys.stderr)

    with open(args.out, 'w') as f:
        json.dump({"type": "FeatureCollection", "bbox": bbox, "features": features}, f)
    print(f"Saved {len(features)} features to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
