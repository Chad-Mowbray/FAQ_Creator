import pandas as pd


class FileIO:
    def __init__(self):
        self.df = self.read_raw_csv()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    def read_raw_csv(self):
        return pd.read_csv('input/VOH_CSV.csv')

    
    def clean_df(self):
        self.df.rename(columns={
                        "Title": "date",
                        "Date": "date2",
                        'Job Title': "job_title",
                        "Faculty Member or Instructor?": "is_faculty_instructor",
                        "Contact ID": "helper",
                        "Engagement Type": "engagement_type",
                        "Which Workshop": "workshop",
                        "Hear about Workshop": "workshop_ref",
                        "What Brings You In": "reason",
                        "Hear about Walk-Ins": "walkin_ref",
                        "Event Notes": "notes",
                        "Consultation Topic": "topic",
                        "How Did You Hear": "general_ref"
                        }, inplace=True)

        self.df.columns = [col.lower() for col in self.df]


    @staticmethod
    def write_file(data, filename):
        with open(f'output/{filename}.txt', 'w') as file:
            for pair in data:
                file.write(str(pair) + "\n")


    # @staticmethod
    # def write_dept_freqs(sorted_dept_freqs):
    #     with open('output/frequency_by_department.txt', 'w') as file:
    #         for pair in sorted_dept_freqs:
    #             file.write(str(pair) + "\n")

    # @staticmethod
    # def write_notes_freqs(sorted_notes_freqs):
    #     with open('output/frequency_by_notes.txt', 'w') as file:
    #         for pair in sorted_notes_freqs:
    #             file.write(str(pair) + "\n")

    # @staticmethod
    # def write_notes_bigrams_freqs(sorted_notes_bigrams_freqs):
    #     with open('output/frequency_by_notes_bigrams.txt', 'w') as file:
    #         for pair in sorted_notes_bigrams_freqs:
    #             file.write(str(pair) + "\n")

    # @staticmethod
    # def write_notes_trigrams_freqs(sorted_notes_trigrams_freqs):
    #     with open('output/frequency_by_notes_trigrams.txt', 'w') as file:
    #         for pair in sorted_notes_trigrams_freqs:
    #             file.write(str(pair) + "\n")
    
    # @staticmethod
    # def write_reason_freqs(sorted_reason_freqs):
    #     with open('output/frequency_by_client_reason.txt', 'w') as file:
    #         for pair in sorted_reason_freqs:
    #             file.write(str(pair) + "\n")

    @staticmethod
    def get_custom_stopwords():
        custom_stopwords = []
        with open('utils/extra_stopwords.txt', 'r') as file:
            for line in file.readlines():
                custom_stopwords.append(line.strip('\n'))
        return custom_stopwords