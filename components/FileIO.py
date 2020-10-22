import pandas as pd


class FileIO:
    def __init__(self, filename):
        self.input_file = filename
        self.df = self.read_raw_csv()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    def read_raw_csv(self):
        return pd.read_csv(f'input/{self.input_file}')

    
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

    @staticmethod
    def get_custom_stopwords():
        custom_stopwords = []
        with open('utils/extra_stopwords.txt', 'r') as file:
            for line in file.readlines():
                custom_stopwords.append(line.strip('\n'))
        return custom_stopwords