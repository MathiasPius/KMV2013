import googlemaps;

class Geocoder():
    def __init__(self):
        with open("api_key.txt", "r") as file:
            self.__client = googlemaps.Client(key=file.read());

    def lookup(self, address):
        result = self.__client.geocode(address);
        if(len(result) == 0):
            return "@LOCATIONUNKNOWN: " + address;
        else:
            return result[0]["geometry"]["location"];

def fix_locations(result):
    if(isinstance(result['position'], str)):
        # Remove the @LOCATIONUNKNOWN tag
        address = result['position'][18:];
        
        pos = address.find("Indgang")
        # Remove any trailing notes about the entrance
        address = address[0:(pos if pos != -1 else None)];

        print("Looking up " + address);

        while(address != ""):
            try: 
                newpos = geocoder.lookup(address);
                if(not isinstance(newpos, str)):
                    result['position'] = newpos;
                    print("\tFound " + address + " at " + str(newpos) + "!");
                    return;

                # Remove the first item
                address = " ".join(address.split(' ')[1:]);
            except:
                print("\tException");

        print("\tGiving up!");

def fix_all_locations():
    municipalities = json.load(open("data.json", "r"));

    for municipality in municipalities:
        fix_locations(municipality);
        for location in municipality['locations']:
            fix_locations(location);

    json.dump(municipalities, io.open("data-fixed-addr.json", "w"), indent = 4, ensure_ascii = False);

geocoder = Geocoder();

fix_all_locations();