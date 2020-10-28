from nltk import FreqDist, bigrams, trigrams, download
from nltk.corpus import stopwords
import string
import copy
import itertools
download('stopwords')
from components.bases.FrequencyBase import FrequencyBase

# TODO: separate out bigrams and trigrams (maybe subclass, maybe mixin)
class TechNotesFrequency(FrequencyBase):
    
    def __init__(self, df):
        super().__init__(df)
        self.sorted_freqs = None
        self._default_stopwords = None
        self.bigrams_fdist = None
        self.sorted_bigrams = None

        self.trigrams_fdist = None
        self.sorted_trigrams = None

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
    def get_notes_trigrams(self):
        trigrams_list = list(trigrams(self._data))
        trigrams_fdist = FreqDist(trigrams_list)
        trigram_freqs = []
        for k,v in trigrams_fdist.items():
            trigram_freqs.append((k,v))

        sorted_trigram_freqs = sorted(trigram_freqs, key=lambda x: x[1], reverse=True)

        temp_dict = {}
        for trigram in sorted_trigram_freqs:
            if trigram[0] in temp_dict:
                temp_dict[trigram[0]] += int(trigram[1])
            else:
                temp_dict[trigram[0]] = int(trigram[1])

        new_dict = {}
        to_delete = []

        # There has to be a better way...
        for i,first in enumerate(temp_dict):
            for j,perms in enumerate(list(itertools.permutations(first))):
                for k, second in enumerate(temp_dict):
                    if perms == second and second != first:
                        if first not in new_dict:
                            new_dict[first] = temp_dict[first] + temp_dict[second]
                        else:
                            new_dict[first] = new_dict[first] + temp_dict[second]
                    else:
                        if first not in new_dict:
                            new_dict[first] = temp_dict[first]

        copy_dict = new_dict.copy()

        for i,item in enumerate(new_dict):
            arr = []
            for j,item2 in enumerate(new_dict):
                if j <= i: continue
                if item2 in list(itertools.permutations(item)) and item != item2:
                    if item2 in copy_dict and item2 not in arr:
                        del copy_dict[item2]
                        arr.append(item2)

        mod_trigram_freqs = []
        for k,v in copy_dict.items():
            mod_trigram_freqs.append((k,v))

        # TODO: filter out useless values
        # FALSE_HITS = [('virtual', 'office', 'hours')]
        # for hit in FALSE_HITS:
        #     if hit in mod_trigram_freqs: mod_trigram_freqs.remove(hit)

        mod_sorted_trigram_freqs = sorted(mod_trigram_freqs, key=lambda x: x[1], reverse=True)
        self.sorted_trigrams = mod_sorted_trigram_freqs  



