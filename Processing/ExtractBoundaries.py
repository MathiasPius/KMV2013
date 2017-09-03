from shapely.geometry import Polygon;
import codecs;
import json;
import os;

INPUT_DIRECTORY = "../data/boundaries-raw/";
OUTPUT_DIRECTORY = "../data/boundaries/";

def reduce_complexity(outline):
    poly = Polygon(outline[0], outline[1:]);
    poly = poly.simplify(0.0005);

    reduced = [
        [[p[0], p[1]] for p in poly.exterior.coords]
    ];

    reduced += [[[p[0], p[1]] for p in hole.coords] for hole in poly.interiors];

    if(len(outline) > 1):
        interiors = list(poly.interiors);

    return reduced;

def extract_boundary(boundary):
    # These have different names between the KMD election data
    # and the OpenStreetMap boundaries data
    replacements = [
        ["Københavns Kommune", "København Kommune"],
        ["Bornholms Regionskommune", "Bornholm Kommune"]
    ];

    localname = boundary["properties"]["localname"];
    for replacement in replacements:
        if localname == replacement[0]:
            localname = replacement[1];

    reduced = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [reduce_complexity(p) for p in boundary["geometry"]["coordinates"]]
        },
        "properties": {
            "name": localname    
        }    
    }

    return reduced;

def extract_boundaries():
    boundaries = {
        "type": "FeatureCollection",
        "features": []
    };

    for filename in os.listdir(INPUT_DIRECTORY):
        with codecs.open(INPUT_DIRECTORY + filename, "r", "utf-8") as file:
            data = json.load(file);
            boundaries["features"].append(extract_boundary(data));

    with open(OUTPUT_DIRECTORY + "all_boundaries.json", "w") as out:
        json.dump(boundaries, out, ensure_ascii = False, indent = 4);

extract_boundaries();