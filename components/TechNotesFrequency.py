import nltk
from nltk.corpus import stopwords
import string
import copy
nltk.download('stopwords')
from components.FrequencyBase import FrequencyBase


class TechNotesFrequency(FrequencyBase):
    def __init__(self):
        self.notes = None
        self.sorted_notes_freqs = None
        self.default_stopwords = None
        self.bigrams_fdist = None
        self.sorted_bigrams = None

        self.add_custom_stopwords()


    def get_notes(self, df):
        self.notes = [reason for reason in df["notes"].values if isinstance(reason, str)]

    
    def add_custom_stopwords(self):
        from components.FileIO import FileIO
        self.default_stopwords = nltk.corpus.stopwords.words('english')
        custom_stopwords = FileIO.get_custom_stopwords()
        self.default_stopwords.extend(custom_stopwords)   


    def clean(self):
        # remove stopwords
        notes_stopwords = [n if n not in self.default_stopwords else '' for note in self.notes for n in note.split(' ') ]

        # make lowercase
        notes_lower = [n.lower() for n in notes_stopwords]

        # remove blanks
        notes_blanks = [n for n in notes_lower if len(n) > 0]

        # remove punctuation
        table = str.maketrans('', '', string.punctuation)
        stripped = [n.translate(table) for n in notes_blanks]

        # remove non-alphabet characters
        notes_alpha = [n for n in stripped if n.isalpha()]

        # remove stopwords again
        notes_alpha2 = [n for n in notes_alpha if n not in self.default_stopwords]

        self.notes = notes_alpha2
        # print(self.notes)


    def get_sorted_fdist(self):
        # run after self.clean
        notes_fdist = nltk.FreqDist(self.notes)
 
        notes_freqs = []
        for k,v in notes_fdist.items():
            notes_freqs.append((k,v))

        sorted_notes_freqs = sorted(notes_freqs, key=lambda x: x[1], reverse=True)
        self.sorted_notes_freqs = sorted_notes_freqs
        

    def get_notes_bigrams(self):
        # run after self.clean
        bigrams = list(nltk.bigrams(self.notes))
        bigrams_fdist = nltk.FreqDist(bigrams)
        bigram_freqs = []
        for k,v in bigrams_fdist.items():
            bigram_freqs.append((k,v))

        sorted_bigram_freqs = sorted(bigram_freqs, key=lambda x: x[1], reverse=True)

        temp_dict = {}
        for bigram in sorted_bigram_freqs:
            if bigram[0] in temp_dict:
                temp_dict[bigram[0]] += int(bigram[1])
            else:
                temp_dict[bigram[0]] = int(bigram[1])

        dict_copy = {}
        for key in temp_dict.keys():
            if key not in dict_copy:
                dict_copy[key] = temp_dict[key]

            for k in temp_dict.keys():
                if (k[1],k[0]) == key: 
                    dict_copy[key] += temp_dict[(k[0],k[1])]
                    del dict_copy[key]

        mod_bigram_freqs = []
        for k,v in dict_copy.items():
            mod_bigram_freqs.append((k,v))

        mod_sorted_bigram_freqs = sorted(mod_bigram_freqs, key=lambda x: x[1], reverse=True)
        self.sorted_bigrams = mod_sorted_bigram_freqs       


    def get_notes_trigrams(self):
        trigrams = list(nltk.trigrams(self.notes))
        trigrams_fdist = nltk.FreqDist(trigrams)
        trigram_freqs = []
        for k,v in trigrams_fdist.items():
            trigram_freqs.append((k,v))

        sorted_trigram_freqs = sorted(trigram_freqs, key=lambda x: x[1], reverse=True)
        # print(sorted_trigram_freqs)

        from components.FileIO import FileIO
        FileIO.write_notes_trigrams_freqs(sorted_trigram_freqs)