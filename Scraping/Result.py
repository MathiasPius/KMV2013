from Candidate import CandidateResult;

class Result:
    def __init__(self, soup):
        topmost_table = soup.find("table", "tableBottomColorKV");
        primary_table = topmost_table.find_next_sibling("table");

        # Read the top municipality info, like votes given, eligible voters, etc.
        municipality_info = primary_table.find("tr");
        self.__read_municipality_info(municipality_info);

        # Read all the candidate lines
        candidate_info = municipality_info.find_next_siblings("tr", ["tableRowPrimary", "tableRowSecondary"]);
        self.__read_candidate_info(candidate_info);
    
    def get_name(self):
        return self.__title;

    def get_eligible_voters(self):
        return self.__eligible_voters;

    def get_counted_votes(self):
        return self.__counted_votes;

    def get_candidates(self):
        return [c for c in self.__candidates if c.get_letter() != ""];

    def get_candidate(self, name):
        return [x for x in self.__candidates if name in x.get_name()][0];

    def get_other_votes(self):
        return self.get_candidate("Øvrige stemmer");

    def get_valid_votes(self):
        return self.get_candidate("I alt gyldige stemmer");

    def get_blank_votes(self):
        return self.get_candidate("Blanke stemmer");

    def get_invalid_votes(self):
        return self.get_candidate("Ugyldige stemmer");

    def get_total_votes(self):
        return self.get_candidate("I alt afgivne stemmer");

    def __read_municipality_info(self, table):
        description = table.find("td");        
        self.__title = " ".join(description.find("tr", "title").stripped_strings);

        #record = counts.find_next_sibling("td");

        # Read the result pairs
        counts = description.find_next_sibling("td");
        results = dict();
        for kv in counts("tr", "statusText"):
            pair = kv("td");
            results[" ".join(pair[0].stripped_strings)] = " ".join(pair[1].stripped_strings);

        self.__eligible_voters = int(results["Stemmeberettigede:"].replace(".", ""));
        self.__counted_votes = int(results["Optalte stemmer:"].replace(".", ""));
        self.__vote_pct = results["Stemmeprocent:"];

    def __read_candidate_info(self, candidate_info):
        self.__candidates = [];
        for row in candidate_info:
            values = row("td");

            link = values[1].find("a");
            link = link["href"] if link != None  else None;

            letter = " ".join(values[0].stripped_strings);

            name = " ".join(values[1].stripped_strings);
            current_votes = int(" ".join(values[2].stripped_strings).replace(".", ""));
            current_votes_pct = " ".join(values[4].stripped_strings);
            votes_change = int(" ".join(values[3].stripped_strings).replace("(", "").replace(")", "").replace(".", ""));
            votes_change_pct = " ".join(values[5].stripped_strings).replace("(", "").replace(")", "");

            if(current_votes_pct != ""):
                current_votes_pct = float(current_votes_pct);
            else:
                current_votes_pct = 0;

            if(votes_change_pct != ""):
                votes_change_pct = float(votes_change_pct);
            else:
                votes_change_pct = 0;

            self.__candidates.append(CandidateResult(
                letter,
                name,
                link,
                current_votes, current_votes_pct, votes_change, votes_change_pct
            ));