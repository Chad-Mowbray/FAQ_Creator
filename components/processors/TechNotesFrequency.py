from nltk import download
from nltk.corpus import stopwords
import string
import copy
import itertools
download('stopwords')
from components.bases.FrequencyBase import FrequencyBase
from components.mixins.BigramsMixin import BigramsMixin
from components.mixins.TrigramsMixin import TrigramsMixin


class TechNotesFrequency(FrequencyBase, BigramsMixin, TrigramsMixin):
    
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
