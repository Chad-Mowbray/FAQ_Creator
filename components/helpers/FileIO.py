import sys
from components.helpers.Logger import Logger


class FileIO():
    """
    FileIO
    """

    def __init__(self, filename):
        self._input_file = filename


    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    @staticmethod
    def write_file(data, filename):
        Logger.log_message(Logger.INFO, f"Writing file {filename}")
        try:
            with open(f'files/output/{filename}.txt', 'w') as file:
                for pair in data:
                    file.write(str(pair) + "\n")
        except Exception as e:
            Logger.log_message(Logger.ERROR, f"Failed to write file {filename} \
                                                to output directory: {e}")


    @staticmethod
    def get_custom_stopwords():
        try:
            custom_stopwords = []
            with open('components/utils/extra_stopwords.txt', 'r') as file:
                for line in file.readlines():
                    custom_stopwords.append(line.strip('\n'))

            assert len(custom_stopwords) > 0
            return custom_stopwords
        except Exception as e:
            Logger.log_message(Logger.ERROR, f"Failed to read custom stopwords: {e}")
            sys.exit(1)
