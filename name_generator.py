import pickle, random

class NameGenerator:

    def __init__(self):
        with open ('d2-words', 'rb') as fp:
            [nouns, proper_nouns, adjectives] = pickle.load(fp)
        
        self.nouns = nouns
        self.proper_nouns = proper_nouns
        self.adjectives = adjectives

    def rand_name(self): 
        name = self.nouns[random.randint(0, len(self.nouns) -1)].capitalize()

        if random.randint(0,1):
            adjective = self.adjectives[random.randint(0, len(self.adjectives) -1)].capitalize()

            name = adjective + " " + name

        if random.randint(0,1):
            proper_noun = self.proper_nouns[random.randint(0, len(self.proper_nouns) -1)].capitalize()

            if random.randint(0,1):
                name = proper_noun + "'s " + name
            else:
                name = name + " of " + proper_noun

        elif random.randint(0,2) != 2:
            name = "The" + " " + name
        
        return name