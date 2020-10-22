from components.FileIO import FileIO


class FrequencyBase:

    def write_file(self, data, filename):
        if data is None: raise Exception("You can't write to file yet")
        FileIO.write_file(data, filename)