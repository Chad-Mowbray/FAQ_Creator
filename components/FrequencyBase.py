from components.FileIO import FileIO


class FrequencyBase:

    def __init__(self, df):
        self.data = None
        self.df = df

    def write_file(self, data, filename):
        if data is None: raise Exception("You can't write to file yet")
        FileIO.write_file(data, filename)

    def get_data(self, column):
        self.data = [reason for reason in self.df[f"{column}"].values if isinstance(reason, str)]