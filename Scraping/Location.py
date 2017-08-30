import requests;
from bs4 import BeautifulSoup;
from Result import Result;
from Candidate import CandidateResult;

class LocationResult(Result):
    def __init__(self, url):
        url = "http://kmdvalg.dk/kv/2013/" + url;
        page = requests.get(url);

        if(page.status_code != 200):
            return;

        soup = BeautifulSoup(page.content, "html.parser");
        Result.__init__(self, soup);

        topmost_table = soup.find("table", "tableBottomColorKV");
        primary_table = topmost_table.find_next_sibling("table");
        municipality_info = primary_table.find("tr");

        description = municipality_info.find("td");
        counts = description.find_next_sibling("td");
        record = counts.find_next_sibling("td");

        sublist = record("tr", "statusText")[1:];
        words = [word for strings in sublist for word in strings.stripped_strings];
        self.__address = " ".join(words[1:]);
        self.__title = " ".join(description.find("tr", "title").find_next_sibling("tr").stripped_strings);

    def get_address(self):
        return self.__address;

    def get_name(self):
        return self.__title;