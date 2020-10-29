from components.helpers.Logger import Logger


class NGramBase:

    def ngram(self):
        pass

    @staticmethod
    def clean_helper(instance):
        """
        Takes an initialized class in RunnerBase.ngram()
        Cleans text content
        """
        instance.add_custom_stopwords()
        instance.clean()


    def bigram_helper(self, instance):
        """
        Takes an initialized class in RunnerBase.ngram()
        Controls execution of code to create bigrams
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
        Takes an initialized class in RunnerBase.ngram()
        Controls execution of code to create trigrams
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