from abc import ABC, abstractmethod

class NGramBase(ABC):
    """
    NGramBase
    """

    def __init__(self):
        self.quick_run = None
        self.should_plot = None


    @abstractmethod
    def ngram(self, *args, **kwargs):
        pass


    def _plot(self, *args, **kwargs):
        pass


    @staticmethod
    def clean_helper(instance):
        """
        clean_helper
        """
        instance.add_custom_stopwords()
        instance.clean()


    def bigram_helper(self, instance):
        """
        bigram_helper
        """
        instance.get_notes_bigrams()
        instance.write_file(instance.sorted_bigrams, "frequency_by_technician_notes_bigrams")
        if self.should_plot:
            self._plot(
                instance.sorted_bigrams,
                "Common Bigrams in Technician Notes",
                "Bigram",
                quick_run=self.quick_run,
                display_number=10
                )


    def trigram_helper(self, instance):
        """
        trigram_helper
        """
        instance.get_notes_trigrams()
        instance.write_file(instance.sorted_trigrams, "frequency_by_technician_notes_trigrams")
        if self.should_plot:
            self._plot(
                instance.sorted_trigrams,
                "Common Trigrams in Technician Notes",
                "Trigram",
                quick_run=self.quick_run,
                display_number=5
                )
