from components.FileIO import FileIO
from components.DepartmentsFrequency import DepartmentsFrequency
from components.ClientReasonsFrequency import ClientReasonsFrequency
from components.TechNotesFrequency import TechNotesFrequency
from components.Plotter import Plotter


def get_df():
    print("getting df...")
    file_reader = FileIO()
    file_reader.clean_df()
    df = file_reader.df
    return df

def departments(df):
    print("processing department info...")
    deps = DepartmentsFrequency()
    deps.get_departments(df)
    deps.get_sorted_fdist()
    deps.write_file(deps.sorted_dept_freqs, "frequency_by_department")

    plot(deps.sorted_dept_freqs,"VOH Usage by Department", "Department Name")


def client_reasons(df):
    print("processing client reason info...")
    reasons = ClientReasonsFrequency()
    reasons.get_reasons(df)
    reasons.get_sorted_fdist()
    reasons.write_file(reasons.sorted_reason_freqs, "frequency_by_client_reasons")

    plot(reasons.sorted_reason_freqs,"Clients' Reason for Visit", "Reason")


def agent_notes(df):
    print("processing agent notes info...")
    notes = TechNotesFrequency()
    notes.get_notes(df)
    notes.add_custom_stopwords()
    notes.clean()

    notes.get_sorted_fdist()
    notes.write_file(notes.sorted_notes_freqs, "frequency_by_agent_notes")

    notes.get_notes_bigrams()
    notes.write_file(notes.sorted_bigrams, "frequency_by_agent_notes_bigrams")

    # notes.get_notes_trigrams()  TODO: add deduplicated trigrams

    plot(notes.sorted_bigrams,"Common Bigrams in Technician Notes", "Bigram", display_number=10)


def plot(*args, **kwargs):
    print("plotting...")
    p = Plotter(*args,**kwargs)
    p.plot()


def main():
    df = get_df()

    departments(df)
    client_reasons(df)
    agent_notes(df)


if __name__ == "__main__":
    print('starting.....')
    main()