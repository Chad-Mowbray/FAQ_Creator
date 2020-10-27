from components.helpers.FileIO import FileIO
from components.processors.DepartmentsFrequency import DepartmentsFrequency
from components.processors.ClientReasonsFrequency import ClientReasonsFrequency
from components.processors.TechNotesFrequency import TechNotesFrequency
from components.processors.TechReasonsFrequency import TechReasonsFrequency
from components.helpers.Plotter import Plotter
from components.bases.RunnerBase import RunnerBase
from components.helpers.Logger import Logger
import sys


class Runner(RunnerBase):

    def __init__(self, input_file, should_plot, quick_run):
        self._input_file = input_file
        self.should_plot = should_plot
        self.quick_run = quick_run
        self._df = None


    def _get_df(self):
        Logger.log_message(Logger.INFO, f"Getting dataframe")
        file_reader = FileIO(self._input_file)
        file_reader.clean_df()
        df = file_reader.df
        self._df = df


    @staticmethod
    def clean_helper(instance):
        instance.add_custom_stopwords()
        instance.clean()

    
    def bigram_helper(self, instance):
        instance.get_notes_bigrams()
        instance.write_file(instance.sorted_bigrams, "frequency_by_agent_notes_bigrams")
        if self.should_plot:
            self._plot(instance.sorted_bigrams, "Common Bigrams in Technician Notes", "Bigram", quick_run=self.quick_run, display_number=10)


    @staticmethod
    def _plot(*args, **kwargs):
        Logger.log_message(Logger.INFO, f"Plotting results for {args[1]} ")
        p = Plotter(*args,**kwargs)
        p.plot()


    def main(self):
        self._get_df()
        # self.ngram("tech reasons", TechReasonsFrequency, "frequency_by_tech", "Tech Reasons Freq", "Reason for visit", quick_run=self.quick_run)

        self.ngram("department", DepartmentsFrequency, "frequency_by_department", "VOH Usage by Department", "Department Name", quick_run=self.quick_run)
        self.ngram("client reason", ClientReasonsFrequency, "frequency_by_client_reasons", "Clients' Reason for Visit", "Reason", quick_run=self.quick_run)
        self.ngram("agent notes", TechNotesFrequency, "frequency_by_agent_notes", "Agent Terms in VOH Notes", "Agent Terms", quick_run=self.quick_run, clean_helper=self.clean_helper, multigram=self.bigram_helper)


if __name__ == "__main__":
    Logger.log_message(Logger.INFO, f"Starting FAQ creator...")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-plot', action="store_true", default=False)
    parser.add_argument('-input', action="store")
    parser.add_argument('-quick', action="store_true", default=False)
    results = parser.parse_args()

    input_file, should_plot, quick_run = results.input, results.plot, results.quick

    if quick_run:
        runner = Runner("test_VOH_CSV.csv", True, quick_run)
        runner.main()

    else:     
        if input_file is None or input_file[-4:] != ".csv": 
            Logger.log_message(Logger.ERROR, "You must provide an input csv file as an argument.  Example: python main.py -input myFile.csv")
            sys.exit(1)
        
        runner = Runner(input_file, should_plot, quick_run)
        runner.main()
