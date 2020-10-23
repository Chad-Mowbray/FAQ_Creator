import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, data, title, x_label, y_label="Frequency", display_number=5):
        self.data = data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.display_number = display_number
        self.label_max_len = 12


    def plot(self):
        x = [str(x[0][:self.label_max_len]) for x in self.data[:self.display_number]]
        y = [x[1] for x in self.data[:self.display_number]]

        plt.bar(x,y,align='center')
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        # for i in range(len(y)):    # add a horizontal line for easier comparison
        #     plt.hlines(y[i],0,x[i]) 
        plt.show()
