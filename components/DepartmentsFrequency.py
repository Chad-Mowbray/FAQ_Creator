import nltk
from components.FrequencyBase import FrequencyBase


class DepartmentsFrequency(FrequencyBase):

    def __init__(self):
        self.departments = None
        self.sorted_dept_freqs = None


    def get_departments(self, df):
        self.departments = [dep for dep in df["department"].values if isinstance(dep, str)]


    def get_sorted_fdist(self):
        if self.departments is None: raise Exception("You must run get_departments first")
        fdist = nltk.FreqDist(self.departments)

        department_freqs = []
        for k,v in fdist.items():
            department_freqs.append((k,v))

        self.sorted_dept_freqs = sorted(department_freqs, key=lambda x: x[1], reverse=True)
