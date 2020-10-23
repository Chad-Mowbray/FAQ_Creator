

class RunnerBase:



    def monogram(self, category, Cls, filename, x_label, y_label):
        print(f"processing {category} info...")
        instance = Cls(self.df)
        instance.get_sorted_fdist()
        instance.write_file(instance.sorted_freqs, filename)

        if self.should_plot:
            self.plot(instance.sorted_freqs, x_label, y_label)