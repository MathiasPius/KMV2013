import json;
import os;

INPUT_DIRECTORY = "../data/geocoded-corrected/";
OUTPUT_DIRECTORY = "../data/election/";

def serialize_candidates(candidates):
    serialized = [];
    for candidate in sorted(candidates, key = lambda candidate: -candidate["votes"]["count"]):
        serialized.append([
            candidate["letter"],
            candidate["name"],
            candidate["votes"]["count"],
            candidate["votes"]["count_pct"],
            candidate["votes"]["change"],
            candidate["votes"]["change_pct"]
        ]);

    return serialized;

def serialize(obj):
    return [
        obj["name"],
        obj["parent"],
        [
            obj["eligible_voters"] - obj["counted_votes"], 
            obj["votes"]["blank"]["votes"]["count"],
            obj["votes"]["valid"]["votes"]["count"],
            obj["votes"]["invalid"]["votes"]["count"],
        ],
        serialize_candidates(obj["votes"]["candidates"])
    ];

def add_location(locations, location):
    serialized = serialize(location);
    locations[serialized[0]] = serialized;

def add_municipality(municipalities, locations, municipality):
    municipality["parent"] = "Danmark"

    serialized = serialize(municipality);
    municipalities[serialized[0]] = serialized;
    for location in municipality["locations"]:
        location["parent"] = municipality["name"]
        add_location(locations, location);

def write_data(data, filename):
    with open(OUTPUT_DIRECTORY + filename, "w") as out:
        json.dump(data, out, ensure_ascii = False);

def compile_electiondata():
    municipalities = {};
    locations = {};

    for filename in os.listdir(INPUT_DIRECTORY):
        with open(INPUT_DIRECTORY + filename, "r") as file:
            data = json.load(file);
            add_municipality(municipalities, locations, data);

    write_data(municipalities, "municipalities.json");
    write_data(locations, "locations.json");

compile_electiondata();