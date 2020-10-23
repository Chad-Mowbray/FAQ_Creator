from components.helpers.FileIO import FileIO
from components.processors.DepartmentsFrequency import DepartmentsFrequency
from components.processors.ClientReasonsFrequency import ClientReasonsFrequency
from components.processors.TechNotesFrequency import TechNotesFrequency
from components.helpers.Plotter import Plotter
from components.bases.RunnerBase import RunnerBase


class Runner(RunnerBase):

    def __init__(self, input_file, should_plot):
        self.input_file = input_file
        self.should_plot = should_plot
        self.df = None


    def get_df(self):
        print("getting df...")
        file_reader = FileIO(self.input_file)
        file_reader.clean_df()
        df = file_reader.df
        self.df = df


    @staticmethod
    def clean_helper(instance):
        instance.add_custom_stopwords()
        instance.clean()

    
    def bigram_helper(self, instance):
        instance.get_notes_bigrams()
        instance.write_file(instance.sorted_bigrams, "frequency_by_agent_notes_bigrams")
        if self.should_plot:
            self.plot(instance.sorted_bigrams, "Common Bigrams in Technician Notes", "Bigram", display_number=10)


    @staticmethod
    def plot(*args, **kwargs):
        print("plotting...")
        p = Plotter(*args,**kwargs)
        p.plot()


    def main(self):
        self.get_df()
        self.ngram("department", DepartmentsFrequency, "frequency_by_department", "VOH Usage by Department", "Department Name")
        self.ngram("client reason", ClientReasonsFrequency, "frequency_by_client_reasons", "Clients' Reason for Visit", "Reason")
        self.ngram("agent notes", TechNotesFrequency, "frequency_by_agent_notes", "Agent Terms in VOH Notes", "Agent Terms", clean_helper=self.clean_helper, multigram=self.bigram_helper)


if __name__ == "__main__":
    print('starting.....')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-plot', action="store_true", default=False)
    parser.add_argument('-input', action="store")
    results = parser.parse_args()

    input_file, should_plot = results.input, results.plot
    if input_file is None or input_file[-4:] != ".csv": raise Exception("You must provide an input csv file as an argument.  Example: python main.py -input myFile.csv")

    runner = Runner(input_file, should_plot)
    runner.main()
