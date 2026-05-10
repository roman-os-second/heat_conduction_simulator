import tkinter as tk
import customtkinter as ctk
from ui_parameters import open_parameters_window
from utils import calc_method, choose_folder, save_name_txt, clear_text
from plotting import plot_epsilon, plot_temperature_distribution, init_simulation_plot, start_simulation, pause_simulation, stop_simulation
from data_manager import sim_data, load_data

def create_main_window():

    ctk.set_appearance_mode('light')
    window = ctk.CTk()
    window.geometry("1010x515")
    window.title("Heat Conduction Simulation 1D")

    combobox_frame = ctk.CTkFrame(window)
    combobox_frame.grid(row=0, column=0, padx=5, pady=5)

    combobox_label = ctk.CTkLabel(combobox_frame, text="Choose method:")
    combobox_label.grid(row=0, column=0)

    options = ["Explicit", "Implicit"]
    combobox = ctk.CTkComboBox(combobox_frame, values=options, state="readonly")
    combobox.grid(row=0, column=1, padx=10, pady=10)
    combobox.set("Explicit")  # default value (explicit method)

    button_choose = ctk.CTkButton(combobox_frame, text="Calculate", command=lambda: calc_method(combobox, data_text))
    button_choose.grid(row=3, column=0, padx=10, pady=10)

    select_folder_label = ctk.CTkLabel(combobox_frame, text="Choose folder to save results")
    select_folder_label.grid(row=1, column=0, padx=10, pady=10)

    folder_button = ctk.CTkButton(combobox_frame, text="Select folder", command=lambda: choose_folder(data_text))
    folder_button.grid(row=1, column=1, padx=10, pady=10)
    # Choose folder to save results

    combobox_label_name = ctk.CTkLabel(combobox_frame, text="Choose file name")
    combobox_label_name.grid(row=2, column=0, padx=10, pady=10)

    entry_file_name = ctk.CTkEntry(combobox_frame)
    entry_file_name.grid(row=2, column=1, padx=10, pady=10)

    button_save_name = ctk.CTkButton(combobox_frame, text="Save file name", command=lambda: save_name_txt(data_text, entry_file_name))
    button_save_name.grid(row=2, column=2, padx=10, pady=10)

    data_text = ctk.CTkTextbox(combobox_frame, height=215, width=400)
    data_text.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

    clear_button = ctk.CTkButton(combobox_frame, text="Clear text", command=lambda: clear_text(data_text))
    clear_button.grid(row=5, column=0, padx=10, pady=10)

    load_button = ctk.CTkButton(combobox_frame, text="Load file", command=lambda: load_data(sim_data))
    load_button.grid(row=5, column=1, padx=10, pady=10)

    plot_button = ctk.CTkButton(combobox_frame, text="Plot Epsilon", command=lambda: plot_epsilon())
    plot_button.grid(row=3, column=1, padx=10, pady=10)

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    parameters_menu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Parameters",
                        menu=parameters_menu)
    parameters_menu.add_command(label="Change",
                            command=open_parameters_window)

    tabview = ctk.CTkTabview(window, width=484, height=504)
    tabview.grid(row=0, column=1, padx=5)

    tab_static = tabview.add("Static Plot")
    tab_simulation = tabview.add("Simulation")  

    static_frame = ctk.CTkFrame(tab_static)
    static_frame.pack(fill="both", expand=True)

    # frame for static plot
    plot_frame_static = ctk.CTkFrame(static_frame, width=450, height=365)
    plot_frame_static.grid(row=0, column=0, padx=10, pady=10)

    static_plot_button = ctk.CTkButton(static_frame, text="Create plot", command=lambda: plot_temperature_distribution(plot_frame_static))
    static_plot_button.place(x=10, y=390)

    simulation_frame = ctk.CTkFrame(tab_simulation)
    simulation_frame.pack(fill="both", expand=True)

    # frame for simulation plot
    plot_frame_simulation = ctk.CTkFrame(simulation_frame, width=450, height=365)
    plot_frame_simulation.grid(row=0, column=0, padx=10, pady=10)
    fig, ax, im, canvas = init_simulation_plot(plot_frame_simulation)

    simulation_run_button = ctk.CTkButton(simulation_frame, text="Run", width=90)
    simulation_run_button.place(x=10, y=390)

    simulation_pause_button = ctk.CTkButton(simulation_frame, text="Pause", width=90)
    simulation_pause_button.place(x=120, y=390)

    simulation_stop_button = ctk.CTkButton(simulation_frame, text="Stop", width=90)
    simulation_stop_button.place(x=230, y=390)

    simulation_speed_entry = ctk.CTkEntry(simulation_frame, width=90)
    simulation_speed_entry.insert(0, "1")
    simulation_speed_entry.place(x=340, y=390)

    simulation_time_label = ctk.CTkLabel(simulation_frame, text="Time")
    simulation_time_label.place(x=40, y=425)

    simulation_time_value = ctk.CTkEntry(simulation_frame, width=90, state="disabled", fg_color='gainsboro')
    simulation_time_value.place(x=120, y=425)

    simulation_run_button3 = ctk.CTkLabel(simulation_frame, text="Weld temp.", width=90)
    simulation_run_button3.place(x=230, y=425)

    simulation_weldtemp_value = ctk.CTkEntry(simulation_frame, width=90, state="disabled", fg_color='gainsboro')
    simulation_weldtemp_value.place(x=340, y=425)

    simulation_run_button.configure(command=lambda: start_simulation(im, canvas, simulation_speed_entry, window, simulation_time_value, simulation_weldtemp_value))
    simulation_pause_button.configure(command=pause_simulation)
    simulation_stop_button.configure(command=lambda: stop_simulation(im, canvas, simulation_time_value, simulation_weldtemp_value))

    window.mainloop()