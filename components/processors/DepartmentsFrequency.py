from components.bases.FrequencyBase import FrequencyBase


class DepartmentsFrequency(FrequencyBase):
    """
    Process data related to departments
    """

    def __init__(self, df):
        super().__init__(df)
        self.sorted_freqs = None
        self.get_data("department")
