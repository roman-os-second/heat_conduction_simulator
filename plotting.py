import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
from data_manager import sim_data, sim_state
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui_parameters import params
import time
from decimal import Decimal

def plot_epsilon():
    chosen_file = filedialog.askopenfilename(title="Choose a file",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    
    if chosen_file:
        with open(chosen_file, 'r') as file:
            lines = file.readlines()

        data = [line.strip().split(",") for line in lines[5:]]  # skip header and split to columns

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

    plt.close(fig)

    return fig, ax, im, canvas

def update_simulation(im, canvas, simulation_speed_entry, window, sim_time_entry, weld_temp):

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

    # for time rounding in time_entry
    rounding_num = Decimal(str(params.delta_tau))
    rounding_digits = abs(rounding_num.as_tuple().exponent)

    # update Time and Weld temp. entry boxes
    sim_time_entry.configure(state="normal")
    sim_time_entry.delete(0, "end")
    sim_time_entry.insert(0, str(round(sim_state.current_step * params.delta_tau, rounding_digits)))
    sim_time_entry.configure(state='disabled')

    weld_temp.configure(state="normal")
    weld_temp.delete(0, "end")
    weld_temp.insert(0, temperatures[int(np.ceil(params.num_node/2))])
    weld_temp.configure(state='disabled')

    # interpolation
    x = np.arange(len(temperatures))
    x_smooth = np.linspace(0, len(temperatures) - 1, 200)
    y_smooth = np.interp(x_smooth, x, temperatures)

    heatmap = np.tile(y_smooth, (100, 1))

    # update plot
    im.set_data(heatmap)
    canvas.draw()

    # sim_state.current_step += 1

    # speed control
    # speed = float(simulation_speed_entry.get())
    # delay = int(1000 / speed)   # ms

    # elapsed_real = time.time() - sim_state.start_time
    # sim_time = elapsed_real * speed

    # sim_state.current_step = int(sim_time / params.delta_tau)    

    now = time.time()
    dt = now - sim_state.last_update_time
    sim_state.last_update_time = now

    speed = float(simulation_speed_entry.get())

    sim_state.sim_time += dt * speed

    sim_state.current_step = int(sim_state.sim_time / params.delta_tau)

    window.after(50, lambda: update_simulation(im, canvas, simulation_speed_entry, window, sim_time_entry, weld_temp))

def start_simulation(im, canvas, simulation_speed_entry, window, sim_time_entry, weld_temp):
    sim_state.is_running = True
    sim_state.start_time = time.time()
    sim_state.sim_time = 0
    sim_state.last_update_time = time.time()
    update_simulation(im, canvas, simulation_speed_entry, window, sim_time_entry, weld_temp)

def pause_simulation():
    sim_state.is_running = False

def stop_simulation(im, canvas, sim_time_entry, weld_temp):
    sim_time_entry.configure(state="normal")
    sim_time_entry.delete(0, "end")
    sim_time_entry.configure(state='disabled')
    weld_temp.configure(state="normal")
    weld_temp.delete(0, "end")
    weld_temp.configure(state='disabled')    
    sim_state.is_running = False
    sim_state.current_step = 0      
    empty_heatmap = np.zeros((100, 200))
    im.set_data(empty_heatmap)
    canvas.draw()