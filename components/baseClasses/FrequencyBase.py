import nltk
from components.FileIO import FileIO


class FrequencyBase:

    def __init__(self, df):
        self.data = None
        self.df = df

    def write_file(self, data, filename):
        if data is None: raise Exception("You can't write to file yet")
        FileIO.write_file(data, filename)

    def get_data(self, column):
        self.data = [x for x in self.df[f"{column}"].values if isinstance(x, str)]

    def get_sorted_fdist(self):
        if self.data is None: raise Exception("You must run get_data first")
        fdist = nltk.FreqDist(self.data)

        freqs = []
        for k,v in fdist.items():
            freqs.append((k,v))

        self.sorted_freqs = sorted(freqs, key=lambda x: x[1], reverse=True)