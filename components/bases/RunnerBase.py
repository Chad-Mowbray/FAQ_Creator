class RunnerBase:

    def ngram(self, category, Cls, filename, x_label, y_label, clean_helper=None, multigram=None):
        print(f"processing {category} info...")
        instance = Cls(self._df)

        if clean_helper: clean_helper(instance)

        instance.get_sorted_fdist()
        instance.write_file(instance.sorted_freqs, filename)

        if multigram: multigram(instance)

        if self.should_plot:
            self._plot(instance.sorted_freqs, x_label, y_label)