from Municipality import MunicipalityResult;
from bs4 import BeautifulSoup;
import io;
import json;
import requests;


def get_all_municipalities(url = "http://www.kmdvalg.dk/kv/2013/"):
    page = requests.get(url);

    if(page.status_code != 200):
        return;

    soup = BeautifulSoup(page.content, "html.parser");
    
    municipalities = [];
    groups = soup("div", "LetterGroup");
    for group in groups:
        for link in group("a"):
            municipalities.append({'link': link["href"], 'name': " ".join(link.stripped_strings)});

    return municipalities;

def serializeCandidate(candidate):
    return {
        'letter': candidate.get_letter(),
        'name': candidate.get_name(),
        'votes': {
            'count': candidate.get_current_votes(),
            'count_pct': candidate.get_current_votes_pct(),
            'change': candidate.get_votes_change(),
            'change_pct': candidate.get_votes_change_pct()
        }
    };

def serialize(obj):
    d = {
        'name': obj.get_name(),
        'address': obj.get_address(),
        'eligible_voters': obj.get_eligible_voters(),
        'counted_votes': obj.get_counted_votes(),
        'votes': {
            'other': serializeCandidate(obj.get_other_votes()),
            'valid': serializeCandidate(obj.get_valid_votes()),
            'blank': serializeCandidate(obj.get_blank_votes()),
            'invalid': serializeCandidate(obj.get_invalid_votes()),
            'total': serializeCandidate(obj.get_total_votes()),
            'candidates': list([serializeCandidate(c) for c in obj.get_candidates()])
        }
    };

    if(isinstance(obj, MunicipalityResult)):
        locations = obj.get_locations();
        d['locations'] = [];
        for location in locations:
            result = serialize(location);
            d['locations'].append(result);

    return d;

def download_all_municipalities():
    all = list();
    for municipality in get_all_municipalities():
        result = MunicipalityResult(municipality["link"]);

        print("Serializing " + result.get_name());
        serialized = serialize(result);

        json.dump(serialized, io.open("data/" + result.get_name().lower().replace(" ", "_") + ".json", "w"), indent = 4, ensure_ascii = False);
        all.append(serialized);

download_all_municipalities();