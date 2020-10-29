from nltk import FreqDist
from components.helpers.FileIO import FileIO


class FrequencyBase:
    """
    Base class for classes that deal with frequencies
    """

    def __init__(self, df):
        self._data = None
        self._df = df
        self.sorted_freqs = None

    @staticmethod
    def write_file(data, filename):
        if data is None: raise Exception("You can't write to file yet")
        FileIO.write_file(data, filename)

    def get_data(self, column):
        self._data = [x for x in self._df[f"{column}"].values if isinstance(x, str)]

    def get_sorted_fdist(self):
        """
        Gets a list of items, sorted by frequency
        """
        if self._data is None: raise Exception("You must run get_data first")
        fdist = FreqDist(self._data)

        freqs = []
        for k,v in fdist.items():
            freqs.append((k,v))

        self.sorted_freqs = sorted(freqs, key=lambda x: x[1], reverse=True)
