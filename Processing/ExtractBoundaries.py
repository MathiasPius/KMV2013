from shapely.geometry import Polygon;
import codecs;
import json;
import os;

INPUT_DIRECTORY = "../data/boundaries-raw/";
OUTPUT_DIRECTORY = "../data/boundaries/";

def reduce_complexity(outline):
    poly = Polygon(outline);
    poly = poly.simplify(0.003);
    return [[p[1], p[0]] for p in poly.exterior.coords];

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

    return [
        localname,
        [reduce_complexity(p[0]) for p in boundary["geometry"]["coordinates"]]
    ];

def extract_boundaries():
    boundaries = [];

    for filename in os.listdir(INPUT_DIRECTORY):
        with codecs.open(INPUT_DIRECTORY + filename, "r", "utf-8") as file:
            data = json.load(file);
            boundaries.append(extract_boundary(data));

    with open(OUTPUT_DIRECTORY + "all_boundaries.json", "w") as out:
        json.dump(boundaries, out, ensure_ascii = False);

extract_boundaries();