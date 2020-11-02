import pandas as pd
from components.bases.DataFrameCreatorBase import DataFrameCreatorBase


class DataFrameCreatorEngagement(DataFrameCreatorBase):
    """
    DataFrameCreatorEngagement
    """

    def __init__(self, input_file):
        super().__init__(input_file)
        self._clean_df()


    def _clean_df(self):
        pass