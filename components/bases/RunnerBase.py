from components.helpers.Logger import Logger
from components.helpers.NGramProcessor import NGramProcessor
from components.helpers.DataFrameCreator import DataFrameCreator

class RunnerBase(NGramProcessor, DataFrameCreator):
    """
    Provides the base class for the Runner
    """
    def __init__(self):
        self._df = None  # TODO: this should probably be made into it's own class too, could potentially help with redundant processing
        self.should_plot = False


    @staticmethod
    def _plot():
        pass
