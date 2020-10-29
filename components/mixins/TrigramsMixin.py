import itertools
from nltk import FreqDist, trigrams


class TrigramsMixin:
    """
    A mixin to handle bigram processing
    """

    FALSE_HITS = [('virtual', 'office', 'hours')]

    def __init__(self):
        self.trigrams_fdist = None
        self.sorted_trigrams = None

    def get_notes_trigrams(self):
        # run after self.clean
        trigrams_list = list(trigrams(self._data))
        trigrams_fdist = FreqDist(trigrams_list)
        trigram_freqs = []
        for k,v in trigrams_fdist.items():
            trigram_freqs.append((k,v))

        sorted_trigram_freqs = sorted(trigram_freqs, key=lambda x: x[1], reverse=True)

        temp_dict = {}
        for trigram in sorted_trigram_freqs:
            if trigram[0] in temp_dict:
                temp_dict[trigram[0]] += int(trigram[1])
            else:
                temp_dict[trigram[0]] = int(trigram[1])

        new_dict = {}

        # There has to be a better way...
        for i,first in enumerate(temp_dict):
            for j,perms in enumerate(list(itertools.permutations(first))):
                for k, second in enumerate(temp_dict):
                    if perms == second and second != first:
                        if first not in new_dict:
                            new_dict[first] = temp_dict[first] + temp_dict[second]
                        else:
                            new_dict[first] = new_dict[first] + temp_dict[second]
                    else:
                        if first not in new_dict:
                            new_dict[first] = temp_dict[first]

        copy_dict = new_dict.copy()

        for i,item in enumerate(new_dict):
            arr = []
            for j,item2 in enumerate(new_dict):
                if j <= i: continue
                if item2 in list(itertools.permutations(item)) and item != item2:
                    if item2 in copy_dict and item2 not in arr:
                        del copy_dict[item2]
                        arr.append(item2)

        mod_trigram_freqs = []
        for k,v in copy_dict.items():
            mod_trigram_freqs.append((k,v))

        for item in mod_trigram_freqs:
            if item[0] in self.FALSE_HITS: mod_trigram_freqs.remove(item)

        mod_sorted_trigram_freqs = sorted(mod_trigram_freqs, key=lambda x: x[1], reverse=True)
        self.sorted_trigrams = mod_sorted_trigram_freqs
