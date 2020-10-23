from components.FileIO import FileIO
from components.DepartmentsFrequency import DepartmentsFrequency
from components.ClientReasonsFrequency import ClientReasonsFrequency
from components.TechNotesFrequency import TechNotesFrequency
from components.Plotter import Plotter
from components.baseClasses.RunnerBase import RunnerBase


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


    def agent_notes(self):
        print("processing agent notes info...")
        notes = TechNotesFrequency(self.df)
        notes.add_custom_stopwords()
        notes.clean()

        notes.get_sorted_fdist()
        notes.write_file(notes.sorted_freqs, "frequency_by_agent_notes")

        notes.get_notes_bigrams()
        notes.write_file(notes.sorted_bigrams, "frequency_by_agent_notes_bigrams")

        # notes.get_notes_trigrams()  TODO: add deduplicated trigrams

        if self.should_plot:
            self.plot(notes.sorted_bigrams,"Common Bigrams in Technician Notes", "Bigram", display_number=10)


    @staticmethod
    def plot(*args, **kwargs):
        print("plotting...")
        p = Plotter(*args,**kwargs)
        p.plot()


    def main(self):
        self.get_df()
        self.monogram("department", DepartmentsFrequency, "frequency_by_department", "VOH Usage by Department", "Department Name")
        self.monogram("client reason", ClientReasonsFrequency, "frequency_by_client_reasons", "Clients' Reason for Visit", "Reason")
        self.agent_notes()


if __name__ == "__main__":
    print('starting.....')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-plot', action="store_true", default=False)
    parser.add_argument('-input', action="store")
    results = parser.parse_args()

    input_file, should_plot = results.input, results.plot
    if input_file is None or input_file[-4:] != ".csv": raise Exception("You must provide an input csv file as an argument:  -input myFile.csv")

    runner = Runner(input_file, should_plot)
    runner.main()
