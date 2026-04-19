import tkinter as tk
import customtkinter as ctk
from ui_parameters import open_parameters_window
from utilts import calc_method, choose_folder, save_name_txt, clear_text
from plotting import plot_epsilon

def create_main_window():
    ctk.set_appearance_mode('light')
    window = ctk.CTk()
    window.geometry("520x490")
    window.title("Heat Conduction Simulation 1D")

    combobox_frame = ctk.CTkFrame(window)
    combobox_frame.pack()

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

    data_text = ctk.CTkTextbox(combobox_frame, height=200, width=400)
    data_text.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

    clear_button = ctk.CTkButton(combobox_frame, text="Clear text", command=lambda: clear_text(data_text))
    clear_button.grid(row=5, column=0, padx=10, pady=10)

    plot_button = ctk.CTkButton(combobox_frame, text="Plot Epsilon", command=plot_epsilon)
    plot_button.grid(row=3, column=1, padx=10, pady=10)

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    parameters_menu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Parameters",
                        menu=parameters_menu)
    parameters_menu.add_command(label="Change",
                            command=open_parameters_window)
    


    window.mainloop()