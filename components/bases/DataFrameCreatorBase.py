import sys
import pandas as pd
from components.helpers.Logger import Logger


class DataFrameCreatorBase:
    """
    DataFrameCreatorBase
    """

    START_DATE = "03/16/2020"


    def __init__(self, input_file):
        self._input_file = input_file
        self.df = self._read_raw_csv()
        self._clean_df()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    def _read_raw_csv(self):
        try:
            return pd.read_csv(f'files/input/{self._input_file}')
        except Exception as e:
            Logger.log_message(
                Logger.ERROR,
                f"Failed to convert csv file {self._input_file} to dataframe: {e}"
                )
            sys.exit(1)


    def _clean_df(self):
       pass