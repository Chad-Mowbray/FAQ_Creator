from components.helpers.Logger import Logger
from components.bases.NGramBase import NGramBase


class NGramProcessor(NGramBase):

    def ngram(
        self,
        category,
        Cls,
        filename,
        x_label,
        y_label,
        quick_run=False,
        clean_helper=None,
        bigram=None,
        trigram=None
        ):
        """
        processes data and graph
        """

        Logger.log_message(Logger.INFO, f"Processing {category} ngram")

        try:
            instance = Cls(self._df)

            if clean_helper: clean_helper(instance)

            instance.get_sorted_fdist()
            instance.write_file(instance.sorted_freqs, filename)

            if bigram: bigram(instance)
            if trigram: trigram(instance)

            if self.should_plot:
                self._plot(instance.sorted_freqs, x_label, y_label, quick_run)

        except:
            Logger.log_message(Logger.ERROR, f"Failed to generate ngram for {category}")
