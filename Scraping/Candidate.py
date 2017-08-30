class CandidateResult:
    def __init__(self, letter, name, link, current_votes, current_votes_pct, votes_change, votes_change_pct):
        self.__letter = letter;
        self.__name = name;
        self.__link = link;
        self.__current_votes = current_votes;
        self.__current_votes_pct = current_votes_pct;
        self.__votes_change = votes_change;
        self.__votes_change_pct = votes_change_pct;
        
    def get_letter(self):
        return self.__letter;

    def get_name(self):
        return self.__name;

    def get_link(self):
        return self.__link;

    def get_current_votes(self):
        return self.__current_votes;

    def get_current_votes_pct(self):
        return self.__current_votes_pct;

    def get_votes_change(self):
        return self.__votes_change;

    def get_votes_change_pct(self):
        return self.__votes_change_pct;