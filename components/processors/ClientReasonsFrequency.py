from components.bases.FrequencyBase import FrequencyBase


class ClientReasonsFrequency(FrequencyBase):

    def __init__(self, df):
        super().__init__(df)
        self.sorted_freqs = None
        self.get_data("reason")


    def get_sorted_fdist(self):
        if self._data == None: raise Exception("You must run get_reasons first")
        canvas = 'anvas'
        organize = 'rganiz'
        migration = 'igrat'
        publish = 'ublish'

        reasons_dict = {
            "canvas": 0,
            "organizing": 0,
            "migration": 0,
            "publish": 0
        }

        for reason in self._data:
            split_r = reason.split(",")
            for r in split_r:
                if r.find(canvas) != -1:
                    reasons_dict["canvas"] += 1
                elif r.find(organize) != -1:
                    reasons_dict["organizing"] += 1
                elif r.find(migration) != -1:
                    reasons_dict["migration"] += 1
                elif r.find(publish) != -1:
                    reasons_dict["publish"] += 1

        sorted_reasons_dict = {}

        srt = sorted(reasons_dict.items(), key=lambda x : x[1], reverse=True)
        for pair in srt:
            sorted_reasons_dict[pair[0]] = pair[1]
        
        sorted_tuples = []
        for k,v in sorted_reasons_dict.items():
            sorted_tuples.append((k,v))

        self.sorted_freqs = sorted_tuples
