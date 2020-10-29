from components.helpers.NGramProcessor import NGramProcessor
from components.helpers.FileIO import FileIO

class RunnerBase(NGramProcessor, FileIO):
    """
    Provides the base class for the Runner
    """

    def __init__(self):
        self._df = None


    @staticmethod
    def _plot():
        pass
