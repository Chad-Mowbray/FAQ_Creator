from nltk import FreqDist, bigrams, download
from nltk.corpus import stopwords
import string
import copy
download('stopwords')
from components.bases.FrequencyBase import FrequencyBase


class TechNotesFrequency(FrequencyBase):
    
    def __init__(self, df):
        super().__init__(df)
        self.sorted_freqs = None
        self._default_stopwords = None
        self.bigrams_fdist = None
        self.sorted_bigrams = None
        self.add_custom_stopwords()
        self.get_data("notes")


    def add_custom_stopwords(self):
        from components.helpers.FileIO import FileIO
        self._default_stopwords = stopwords.words('english')
        custom_stopwords = FileIO.get_custom_stopwords()
        self._default_stopwords.extend(custom_stopwords)   


    def clean(self):
        # remove stopwords
        notes_stopwords = [n if n not in self._default_stopwords else '' for note in self._data for n in note.split(' ') ]

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
        notes_alpha2 = [n for n in notes_alpha if n not in self._default_stopwords]

        self._data = notes_alpha2

        
    def get_notes_bigrams(self):
        # run after self.clean
        bigrams_list = list(bigrams(self._data))
        bigrams_fdist = FreqDist(bigrams_list)
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


    # TODO: deduplicate trigrams
    # def get_notes_trigrams(self):
    #     trigrams = list(nltk.trigrams(self._data))
    #     trigrams_fdist = nltk.FreqDist(trigrams)
    #     trigram_freqs = []
    #     for k,v in trigrams_fdist.items():
    #         trigram_freqs.append((k,v))

    #     sorted_trigram_freqs = sorted(trigram_freqs, key=lambda x: x[1], reverse=True)
