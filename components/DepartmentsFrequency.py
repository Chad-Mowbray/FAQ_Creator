import nltk
from components.FrequencyBase import FrequencyBase


class DepartmentsFrequency(FrequencyBase):

    def __init__(self, df):
        super().__init__(df)
        self.sorted_dept_freqs = None
        self.get_data("department")


    def get_sorted_fdist(self):
        if self.data is None: raise Exception("You must run get_departments first")
        fdist = nltk.FreqDist(self.data)

        department_freqs = []
        for k,v in fdist.items():
            department_freqs.append((k,v))

        self.sorted_dept_freqs = sorted(department_freqs, key=lambda x: x[1], reverse=True)
