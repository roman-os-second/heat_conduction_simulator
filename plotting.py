import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
from data_manager import sim_data, sim_state
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def plot_temperature_distribution(frame):
    # clear frame
    for widget in frame.winfo_children():
        widget.destroy()

    temperatures = sim_data.get_last_row()

    x = np.arange(len(temperatures))
    x_smooth = np.linspace(0, len(temperatures) - 1, 200)

    y_smooth = np.interp(x_smooth, x, temperatures)

    heatmap = np.tile(y_smooth, (100, 1))

    fig, ax = plt.subplots(figsize=(5.5, 4.6))

    im = ax.imshow(
        heatmap,
        cmap="jet",
        aspect="auto",
        origin="lower",
        vmin=0,
        vmax=260)

    fig.colorbar(im, ax=ax)
    ax.set_title("Temperature Distribution (°C)")
    ax.set_xticks([])
    ax.set_yticks([])

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def init_simulation_plot(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5.5, 4.6))

    # initial empty heatmap
    heatmap = np.zeros((100, 200))

    im = ax.imshow(
        heatmap,
        cmap="jet",
        aspect="auto",
        origin="lower",
        vmin=0,
        vmax=260
    )

    fig.colorbar(im, ax=ax)
    ax.set_title("Temperature Distribution (°C)")
    ax.set_xticks([])
    ax.set_yticks([])

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig, ax, im, canvas

def update_simulation(im, canvas, simulation_speed_entry, window):

    if not sim_state.is_running:
        return
    
    if sim_data is None:
        return

    if im is None or canvas is None:
        return

    if sim_state.current_step >= len(sim_data.data):
        sim_state.is_running = False
        return

    temperatures = sim_data.get_temperatures(sim_state.current_step)

    # interpolation
    x = np.arange(len(temperatures))
    x_smooth = np.linspace(0, len(temperatures) - 1, 200)
    y_smooth = np.interp(x_smooth, x, temperatures)

    heatmap = np.tile(y_smooth, (100, 1))

    # update plot
    im.set_data(heatmap)
    canvas.draw()

    sim_state.current_step += 1

    # speed control
    speed = float(simulation_speed_entry.get())
    delay = int(1000 / speed)   # ms

    window.after(delay, lambda: update_simulation(im, canvas, simulation_speed_entry, window))

def start_simulation(im, canvas, simulation_speed_entry, window):
    sim_state.is_running = True
    update_simulation(im, canvas, simulation_speed_entry, window)

def pause_simulation():
    sim_state.is_running = False

def stop_simulation(im, canvas):
    sim_state.is_running = False
    sim_state.current_step = 0      
    empty_heatmap = np.zeros((100, 200))
    im.set_data(empty_heatmap)
    canvas.draw()