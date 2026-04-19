import matplotlib.pyplot as plt
from tkinter import filedialog

def plot_epsilon():
    chosen_file = filedialog.askopenfilename(title="Choose a file",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    
    if chosen_file:
        with open(chosen_file, 'r') as file:
            lines = file.readlines()

        data = [line.split() for line in lines[5:]]  # skip header and split to columns

        iterations = [int(row[0]) for row in data]
        epsilon_values = [float(row[1]) for row in data]

        plt.figure(figsize=(10, 6))
        plt.plot(iterations, epsilon_values)
        plt.xlabel('Iteration number')
        plt.ylabel('Epsilon max. value')
        plt.title('Epsilon max. plot as a function of iteration')
        plt.grid(True)
        plt.show()


