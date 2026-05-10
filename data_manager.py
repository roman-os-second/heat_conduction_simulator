import numpy as np
from tkinter import filedialog

def load_data(sim_data):

    chosen_file = filedialog.askopenfilename(
        title="Choose a file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if not chosen_file:
        return

    sim_data.load_from_file(chosen_file)

class SimulationData:
    def __init__(self):
        self.data = None

    def load_from_file(self, file_path):
        self.data = np.loadtxt(file_path, delimiter=",", skiprows=5)

    def is_loaded(self):
        return self.data is not None

    def get_last_row(self):
        if self.data is None:
            return None
        return self.data[-1][1:]  
    
    def get_temperatures(self, step):
        return self.data[step][1:]

class SimulationState:
    def __init__(self):
        self.current_step = 0
        self.is_running = False
        self.start_time = None
        self.sim_time = 0
        self.last_update_time = None

sim_data = SimulationData()
sim_state = SimulationState()