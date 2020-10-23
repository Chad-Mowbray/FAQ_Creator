from components.FileIO import FileIO
from components.DepartmentsFrequency import DepartmentsFrequency
from components.ClientReasonsFrequency import ClientReasonsFrequency
from components.TechNotesFrequency import TechNotesFrequency
from components.Plotter import Plotter


class Runner:

    def __init__(self, filename, should_plot):
        self.input_file = filename
        self.should_plot = should_plot
        self.df = None

    def get_df(self):
        print("getting df...")
        file_reader = FileIO(self.input_file)
        file_reader.clean_df()
        df = file_reader.df
        self.df = df
        # return df

    def departments(self):
        print("processing department info...")
        deps = DepartmentsFrequency(self.df)
        # deps.get_data(self.df)
        deps.get_sorted_fdist()
        deps.write_file(deps.sorted_dept_freqs, "frequency_by_department")

        if self.should_plot:
            self.plot(deps.sorted_dept_freqs,"VOH Usage by Department", "Department Name")


    def client_reasons(self):
        print("processing client reason info...")
        reasons = ClientReasonsFrequency(self.df)
        # reasons.get_data(self.df)
        reasons.get_sorted_fdist()
        reasons.write_file(reasons.sorted_reason_freqs, "frequency_by_client_reasons")
        
        if self.should_plot:
            self.plot(reasons.sorted_reason_freqs,"Clients' Reason for Visit", "Reason")


    def agent_notes(self):
        print("processing agent notes info...")
        notes = TechNotesFrequency(self.df)
        # notes.get_data(self.df)
        notes.add_custom_stopwords()
        notes.clean()

        notes.get_sorted_fdist()
        notes.write_file(notes.sorted_notes_freqs, "frequency_by_agent_notes")

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
        self.departments()
        self.client_reasons()
        self.agent_notes()


if __name__ == "__main__":
    print('starting.....')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-plot', action="store_true", default=False)
    parser.add_argument('-input', action="store")
    results = parser.parse_args()

    filename, should_plot = results.input, results.plot
    if filename is None or filename[-4:] != ".csv": raise Exception("You must provide an input csv file as an argument:  -input myFile.csv")

    runner = Runner(filename, should_plot)
    runner.main()
