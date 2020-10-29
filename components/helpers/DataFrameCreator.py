from components.helpers.FileIO import FileIO
from components.helpers.Logger import Logger


class DataFrameCreator:

    def _get_df(self):
        Logger.log_message(Logger.INFO, "Getting dataframe")
        file_reader = FileIO(self._input_file)
        file_reader.clean_df()
        self._df = file_reader.df