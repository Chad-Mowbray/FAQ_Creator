from components.bases.FrequencyBase import FrequencyBase


class TechReasonsFrequency(FrequencyBase):
    """
    Process data related to technician's stated reason for client visit
    """

    def __init__(self, df):
        super().__init__(df)
        self.sorted_freqs = None
        self.get_data("topic")


    def get_sorted_fdist(self):

        if self._data is None: raise Exception("You must run get_data first")

        cleaned_data = []
        for line in self._data:
            clean = [letter if letter not in ["[", "]", "\'", "\"",  ] else '' for letter in line]
            split = ''.join(clean).split(',')
            for item in split:
                cleaned_data.append(item)

        topic_dict = {}

        for topic in cleaned_data:
            if topic not in topic_dict:
                topic_dict[topic] = 1
            else:
                topic_dict[topic] += 1

        topic_dict.pop(" etc.)", None)

        sorted_topics_dict = {}
        srt = sorted(topic_dict.items(), key=lambda x : x[1], reverse=True)
        for pair in srt:
            sorted_topics_dict[pair[0]] = pair[1]

        sorted_tuples = []
        for k,v in sorted_topics_dict.items():
            sorted_tuples.append((k,v))

        self.sorted_freqs = sorted_tuples
