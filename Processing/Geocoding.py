import googlemaps;
import json;
import time;
import os;

DATA_DIRECTORY = "../data/";
RAW_DIRECTORY = DATA_DIRECTORY + "raw/";
GEOCODED_DIRECTORY = DATA_DIRECTORY + "geocoded/";
CORRECTED_DIRECTORY = DATA_DIRECTORY + "geocoded-corrected/";

class Geocoder():
    def __init__(self):
        with open("google.apikey", "r") as file:
            self.__client = googlemaps.Client(key=file.read());

    def lookup(self, address):
        result = self.__client.geocode(address);
        if(len(result) == 0):
            return "failed", None;
        elif(len(result) > 1):
            return "multiple", result;
        else:
            return "single", result[0]["geometry"]["location"];

geocoder = Geocoder();

def geocode(obj, municipality = None):
    address = obj["address"].lower();
    
    # Remove any trailing notes
    for note in ["indgang ", "valget "]:
        pos = address.find(note);
        address = address[0:(pos if pos != -1 else None)];

    if(municipality):
        address += ", " + municipality;
    address += ", Danmark";

    (status, coordinate) = geocoder.lookup(address);
    if(status == "single"):
        obj["coordinate"] = coordinate;
    elif(status == "multiple"):
        print("Found multiple results for \"{}\" at \"{}".format(obj["name"], address));
        obj["coordinate"] = coordinate[0]["geometry"]["location"];
    else:
        print("Failed to look up \"{}\"".format(address));
        obj["coordinate"] = "{UNKNOWN}";

def geocode_municipality(municipality):
    print("Geocoding " + municipality["name"]);
    geocode(municipality);
    for location in municipality["locations"]:
        geocode(location, municipality["name"]);

def geocode_all_municipalities():
    for filename in os.listdir(RAW_DIRECTORY):
        with open(RAW_DIRECTORY + filename, "r") as file:
            data = json.load(file);
            processed = geocode_municipality(data);

            with open(GEOCODED_DIRECTORY + filename, "w") as out:
                json.dump(data, out, indent = 4, ensure_ascii = False);

def correct(obj, municipality = None):
    address = obj["address"];
    if(municipality):
        address += ", " + municipality;
    address += ", Danmark";

    if(isinstance(obj["coordinate"], str) and obj["coordinate"] == "{UNKNOWN}"):
        while(True):
            print("Correct \"{}\"".format(address));
            revised = input("revised address: ");

            if(municipality):
                revised += ", " + municipality;
            revised += ", Danmark";

            (status, coordinate) = geocoder.lookup(revised);
            if(status == "single"):
                print("Address corrected!");
                obj["coordinate"] = coordinate;
                break;
            elif(status == "multiple"):
                print("Found multiple results for \"{}\" at \"{}".format(obj["name"], revised));
                obj["coordinate"] = coordinate[0]["geometry"]["location"];
                break;
            else:
                print("Failed to look up \"{}\"".format(revised));

def correct_municipality(municipality):
    print("Correcting " + municipality["name"]);
    correct(municipality);
    for location in municipality["locations"]:
        correct(location, municipality["name"]);

def interactive_correction():
    for filename in os.listdir(GEOCODED_DIRECTORY):
        data = "";
        with open(GEOCODED_DIRECTORY + filename, "r") as file:
            data = json.load(file);

        correct_municipality(data);
        
        print("Writing revised data");
        with open(CORRECTED_DIRECTORY + filename, "w") as out:
            json.dump(data, out, indent = 4, ensure_ascii = False);


while(True):
    cmd = input("[q]uit/ [a]ll / [p]ostprocess correction:");
    if(cmd == "q"):
        break;
    elif(cmd == "a"):
        geocode_all_municipalities();
    elif(cmd == "p"):
        interactive_correction();
    else:
        print("Unknown command {}".format(cmd));