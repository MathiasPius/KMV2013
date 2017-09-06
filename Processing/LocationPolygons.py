from scipy.spatial import Voronoi, voronoi_plot_2d;
import json;
import os;
from decimal import Decimal;

INPUT_DIRECTORY = "../data/geocoded-corrected/";
OUTPUT_DIRECTORY = "../data/locations/";

def add_location(location):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [location["coordinate"]["lng"], location["coordinate"]["lat"]]
        },
        "properties": {
            "name": location["name"]    
        }    
    }


def generate_polygons():
    locations = {}

    for filename in os.listdir(INPUT_DIRECTORY):
        with open(INPUT_DIRECTORY + filename, "r") as file:
            data = json.load(file);

            locations[data["name"]] = {
                "type": "FeatureCollection",
                "features": []
            }

            for location in data["locations"]:
                locations[data["name"]]["features"].append(add_location(location));

    with open(OUTPUT_DIRECTORY + "locations.json", "w") as out:
        json.dump(locations, out, ensure_ascii = False, indent = 4);

generate_polygons();