from scipy.spatial import Voronoi, voronoi_plot_2d;
import json;
import os;
from decimal import Decimal;

INPUT_DIRECTORY = "../data/geocoded-corrected/";
OUTPUT_DIRECTORY = "../data/voronois/";

def add_location(location_points, location):
    location_points.append([location["name"], [location["coordinate"]["lat"], location["coordinate"]["lng"]]]);

def add_municipality(municipality_points, location_points, municipality):
    municipality_points.append([municipality["name"], [municipality["coordinate"]["lat"], municipality["coordinate"]["lng"]]]);
    for location in municipality["locations"]:
        add_location(location_points, location);

def toDecimal(flt):
    parts = str(flt).split('.');
    return Decimal(parts[0] + "." + parts[1][:2]);

def bounds(points, key):
    return [
        key(min(points, key = lambda p: key(p))), 
        key(max(points, key = lambda p: key(p)))
    ];

def write_voronoi(points, filename):
    # Sort by name
    points.sort(key = lambda m: m[0]);

    lat = bounds(points, lambda p: p[1][0]);
    lng = bounds(points, lambda p: p[1][1]);

    scale_lat = [
        lambda x: (x - lat[0]) / (lat[1] / lat[0]),
        lambda x: x * (lat[1] / lat[0]) + lat[0]
    ];

    scale_lng = [
        lambda x: (x - lng[0]) / (lng[1] / lng[0]),
        lambda x: x * (lng[1] / lng[0]) + lng[0]
    ];

    scale = [
        lambda p: [scale_lat[0](p[0]), scale_lng[0](p[1])],
        lambda p: [scale_lat[1](p[0]), scale_lng[1](p[1])]
    ];

    with open(OUTPUT_DIRECTORY + filename, "w") as out:
        vor = Voronoi([scale[0](p[1]) for p in points], qhull_options='Qbb Qx Qt Qc');

        for p in vor.vertices:
            p[0] = toDecimal(scale_lat[1](p[0]));
            p[1] = toDecimal(scale_lng[1](p[1]));

        polygons = [];
        for i, _ in enumerate(points):
            point = vor.point_region[i];
            region = vor.regions[point];
            polygon = [vor.vertices[vertex] for vertex in region if vertex != -1];

            input_point = vor.points[point];
            polygons.append([points[i][0], [p.tolist() for p in polygon]]);
            

        json.dump(list(filter(None, polygons)), out, ensure_ascii = False);

def generate_polygons():
    municipality_points = [];
    location_points = [];

    for filename in os.listdir(INPUT_DIRECTORY):
        with open(INPUT_DIRECTORY + filename, "r") as file:
            data = json.load(file);
            add_municipality(municipality_points, location_points, data);

    write_voronoi(municipality_points, "municipalities.json");
    write_voronoi(location_points, "locations.json");

generate_polygons();