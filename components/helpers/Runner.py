from components.helpers.FileIO import FileIO
from components.processors.DepartmentsFrequency import DepartmentsFrequency
from components.processors.TechNotesFrequency import TechNotesFrequency
from components.processors.TechReasonsFrequency import TechReasonsFrequency
from components.helpers.Plotter import Plotter
from components.bases.RunnerBase import RunnerBase
from components.helpers.Logger import Logger


class Runner(RunnerBase):
    """
    Runner inherits from RunnerBase
    Controls execution of other components
    """

    def __init__(self, input_file, should_plot, quick_run):
        super().__init__()
        self._input_file = input_file
        self.should_plot = should_plot
        self.quick_run = quick_run


    # def _get_df(self):
    #     Logger.log_message(Logger.INFO, "Getting dataframe")
    #     file_reader = FileIO(self._input_file)
    #     file_reader.clean_df()
    #     self._df = file_reader.df


    @staticmethod
    def _plot(*args, **kwargs):
        """
        Takes processed information needed to plot
        Controls execution of plot
        """
        Logger.log_message(Logger.INFO, f"Plotting results for {args[1]} ")
        p = Plotter(*args,**kwargs)
        p.plot()


    def main(self):
        self._get_df()
        self.ngram(
            "Visit Type Category",
            TechReasonsFrequency,
            "frequency_by_technician_categorization",
            "Reason for Visit According to Technician",
            "Category",
            quick_run=self.quick_run
            )
        self.ngram(
            "Department",
            DepartmentsFrequency,
            "frequency_by_department",
            "VOH Usage by Department",
            "Department Name",
            quick_run=self.quick_run
            )
        self.ngram(
            "Technician Notes",
            TechNotesFrequency,
            "frequency_by_technician_notes",
            "Technician's Terms Found in VOH Notes",
            "Technician Terms",
            quick_run=self.quick_run,
            clean_helper=self.clean_helper,
            bigram=self.bigram_helper,
            trigram=self.trigram_helper
            )
