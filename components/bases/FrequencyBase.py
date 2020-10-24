import nltk
from components.helpers.FileIO import FileIO


class FrequencyBase:

    def __init__(self, df):
        self._data = None
        self._df = df

    def write_file(self, data, filename):
        if data is None: raise Exception("You can't write to file yet")
        FileIO.write_file(data, filename)

    def get_data(self, column):
        self._data = [x for x in self._df[f"{column}"].values if isinstance(x, str)]

    def get_sorted_fdist(self):
        if self._data is None: raise Exception("You must run get_data first")
        fdist = nltk.FreqDist(self._data)

        freqs = []
        for k,v in fdist.items():
            freqs.append((k,v))

        self.sorted_freqs = sorted(freqs, key=lambda x: x[1], reverse=True)