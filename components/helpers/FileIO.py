import sys
import pandas as pd
from .Logger import Logger



class FileIO:
    """
    Reads from input csv and custom stopwords list
    Converts to dataframe
    Renames columns
    Cleans dates
    writes files
    """

    START_DATE = "03/16/2020"

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
            Logger.log_message(
                Logger.ERROR,
                f"Failed to convert csv file {self._input_file} to dataframe"
                )
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

        # clean date and time fields
        self.df["date2"] = [date if len(str(date).split('/')[0]) == 2 else f"0{date}" for date in self.df["date2"] ]
        month_day_year_clean = []
        for date in self.df["date2"]:
            if date != "0nan":
                if len(str(date).split('/')[1]) == 2:
                    month_day_year_clean.append(f"{date[:6]}20{date[6:8]}")
                else:
                    month_day_year_clean.append(f"{date[:3]}0{date[3:5]}20{date[5:7]}")
            else:
                month_day_year_clean.append("0nan")
        self.df["MDY"] = month_day_year_clean

        time_clean = []
        for date in self.df["date2"]:
            if date != "0nan":
                time = str(date).split(' ')[1]
                hours, minutes = time.split(":")
                if len(hours) < 2: hours = f"0{hours}"
                if len(minutes) < 2: minutes = f"0{minutes}"
                time_clean.append(f"{hours}:{minutes}")
            else:
                time_clean.append("0nan")
        self.df["time_of_day"] = time_clean

        # drop date nulls
        null_dates = self.df[ self.df['MDY'] == "0nan" ].index
        self.df.drop(null_dates , inplace=True)

        # convert cleaned date strings into date objects
        self.df['MDY'] = pd.to_datetime(self.df['MDY'], format="%m/%d/%Y")

        # drop rows before cutoff date
        cutoff_indexes = self.df[ self.df['MDY'] < self.START_DATE ].index
        self.df.drop(cutoff_indexes , inplace=True)



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
            Logger.log_message(Logger.ERROR, "Failed to read custom stopwords")
            sys.exit(1)
