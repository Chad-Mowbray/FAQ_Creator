import pandas as pd
from components.bases.DataFrameCreatorBase import DataFrameCreatorBase


class DataFrameCreatorEngagement(DataFrameCreatorBase):
    """
    DataFrameCreatorEngagement
    """

    def __init__(self, input_file):
        super().__init__(input_file)
        self._clean_df()


    def _clean_df(self):
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
        self.df["date2"] = [date
                            if len(str(date).split('/')[0]) == 2
                            else f"0{date}"
                            for date in self.df["date2"]]
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