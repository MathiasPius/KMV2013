import requests;
from bs4 import BeautifulSoup;
from Result import Result;

from Candidate import CandidateResult;
from Location import LocationResult;

class MunicipalityResult(Result):
    def __init__(self, url):
        if(not url.startswith("http://kmdvalg.dk/kv/2013/")):
            url = "http://kmdvalg.dk/kv/2013/" + url;

        page = requests.get(url);

        if(page.status_code != 200):
            return;

        soup = BeautifulSoup(page.content, "html.parser");

        Result.__init__(self, soup);

        topmost_table = soup.find("table", "tableBottomColorKV");
        primary_table = topmost_table.find_next_sibling("table");
        secondary_table = primary_table.find_next_sibling("table", "tableBottomColorKV");

        # Read the voting locations
        location_info = secondary_table.find("tr", "tableRowSecondary");
        self.__read_location_info(location_info);

    def get_address(self):
        return self.get_name();

    def get_locations(self):
        return [LocationResult(l.get_link()) for l in self.__voting_locations];

    def get_location_names(self):
        return [l.get_name() for f in self.__voting_locations];

    def __read_location_info(self, row):
        self.__voting_locations = list([VotingLocationStub(" ".join(l.stripped_strings), l["href"]) for l in row("a")[1:]]);

class VotingLocationStub:
    def __init__(self, name, link):
        self.__name = name;
        self.__link = link;

    def get_name(self):
        return self.__name;

    def get_link(self):
        return self.__link;