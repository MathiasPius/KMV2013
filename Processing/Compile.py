import codecs;
import json;
import os;

INPUT_DIRECTORY = "../data/";
OUTPUT_DIRECTORY = "../Web/";

def read_data(filename):
    with open(INPUT_DIRECTORY + filename, "r") as file:
        return json.load(file);

def compile_data():
    datamap = [
        ["voronois/locations.json", "geometry_locations"],
        ["boundaries/all_boundaries.json", "geometry_municipalities"],
        ["election/locations.json", "electiondata_locations"],
        ["election/municipalities.json", "electiondata_municipalities"]
    ];

    with codecs.open(OUTPUT_DIRECTORY + "data.js", "w", "utf-8") as out:
        out.write(u"// This file was compiled from election data processed elsewhere in the project\n");

        for mapping in datamap:
            out.write("var {} = ".format(mapping[1]));
            json.dump(read_data(mapping[0]), out, ensure_ascii = False);
            out.write(";\n");

compile_data();