import pandas as pd
from .Logger import Logger
import sys


class FileIO:
    
    def __init__(self, filename):
        self._input_file = filename
        self.df = self._read_raw_csv()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    def _read_raw_csv(self):
        try: 
            return pd.read_csv(f'files/input/{self._input_file}')
        except:
            Logger.log_message(Logger.ERROR, f"Failed to convert csv file {self._input_file} to dataframe")
            sys.exit(1)
        

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
        Logger.log_message(Logger.INFO, f"Writing file {filename}")
        try:
            with open(f'files/output/{filename}.txt', 'w') as file:
                for pair in data:
                    file.write(str(pair) + "\n")
        except:
            Logger.log_message(Logger.ERROR, f"Failed to write file {filename} to output directory")


    @staticmethod
    def get_custom_stopwords():
        try:
            custom_stopwords = []
            with open('components/utils/extra_stopwords.txt', 'r') as file:
                for line in file.readlines():
                    custom_stopwords.append(line.strip('\n'))

            assert len(custom_stopwords) > 0
            return custom_stopwords
        except:
            Logger.log_message(Logger.ERROR, f"Failed to read custom stopwords")
            sys.exit(1)
