import tkinter as tk
import customtkinter as ctk
from config import params

def open_parameters_window():

    entries = {} # dictionary to store parameters

    aux_entries = {} # dictionary to store aux parameters

    def apply_params():
        int_params = {"num_node"}
        try:
            for name, entry in entries.items():
                value = entry.get()

                if name in int_params:
                    setattr(params, name, int(value))
                else:
                    setattr(params, name, float(value))
                    
        except ValueError:
            tk.messagebox.showwarning(
                "Input error",
                "All parameters must be numbers, Node number must be integer"
            )
        
    def clear_params():
        for name, entry in entries.items():
            entry.delete(0, "end")
            setattr(params, name, None)

    def load_parameters():
        for name, entry in entries.items():
            value = getattr(params, name)
            entry.insert(0, str(value))

    def aux_values():
            
        delta_xe = 2 * params.a / params.num_node
        delta_xe_lew = params.a / params.num_node
        delta_xw = 2 * params.a / params.num_node
        delta_xw_praw = params.a / params.num_node
        delta_x = 2 * params.a / params.num_node

        delta_v = params.a_area * delta_x

        params.ae = params.k * params.a_area / delta_xe
        params.ae6 = params.k * params.a_area / delta_xe_lew
        params.aw = params.k * params.a_area / delta_xw
        params.aw2 = params.k * params.a_area / delta_xw_praw

        params.w = params.ro * delta_v * params.c / params.delta_tau

        for name, entry in aux_entries.items():
            entry.configure(state='normal')
            entry.delete(0, "end")
            value = getattr(params, name)
            entry.insert(0, round(value, 2))
            entry.configure(state='disabled')

    new_window = ctk.CTkToplevel()
    new_window.grab_set()
    new_window.focus_force()
    new_window.geometry("800x500")
    new_window.title("Parameters Configuration")

    label_parametry = ctk.CTkLabel(new_window,
                            text="Current parameters:\n",
                            font=("Arial",14))
    label_parametry.place(x=20, y=20)

    label_t_weld = ctk.CTkLabel(new_window,
                          text="Weld temperature",
                          font=("Arial", 14))
    label_t_weld.place(x=50, y=50)    
    entries["t_weld"] = ctk.CTkEntry(new_window, width=80)
    entries["t_weld"].place(x=250, y=55)
    label_t_weld_units = ctk.CTkLabel(new_window,
                          text="°C",
                          font=("Arial", 14))
    label_t_weld_units.place(x=340, y=50)  

    label_t_press = ctk.CTkLabel(new_window,
                          text="Press temperature",
                          font=("Arial", 14))
    label_t_press.place(x=50, y=80)  
    entries["t_press"] = ctk.CTkEntry(new_window, width=80)
    entries["t_press"].place(x=250, y=85)
    label_t_press_units = ctk.CTkLabel(new_window,
                          text="°C",
                          font=("Arial", 14))
    label_t_press_units.place(x=340, y=80)  

    label_t_i = ctk.CTkLabel(new_window,
                      text="Initial temperature",
                      font=("Arial", 14))
    label_t_i.place(x=50, y=110)  
    entries["t_i"] = ctk.CTkEntry(new_window, width=80)
    entries["t_i"].place(x=250, y=115)
    label_t_i_units = ctk.CTkLabel(new_window,
                      text="°C",
                      font=("Arial", 14))
    label_t_i_units.place(x=340, y=110) 

    label_a = ctk.CTkLabel(new_window,
                    text="Plate thickness",
                    font=("Arial", 14))
    label_a.place(x=50, y=140)  
    entries["a"] = ctk.CTkEntry(new_window, width=80)
    entries["a"].place(x=250, y=145)
    label_a_units = ctk.CTkLabel(new_window,
                    text="m",
                    font=("Arial", 14))
    label_a_units.place(x=340, y=140)

    label_k = ctk.CTkLabel(new_window,
                    text="Thermal conductivity coef.",
                    font=("Arial", 14))
    label_k.place(x=50, y=170)  
    entries["k"] = ctk.CTkEntry(new_window, width=80)
    entries["k"].place(x=250, y=175)
    label_k_units = ctk.CTkLabel(new_window,
                    text="W/mK",
                    font=("Arial", 14))
    label_k_units.place(x=340, y=170)  

    label_c = ctk.CTkLabel(new_window,
                    text="Specific heat",
                    font=("Arial", 14))
    label_c.place(x=50, y=200)  
    entries["c"] = ctk.CTkEntry(new_window, width=80)
    entries["c"].place(x=250, y=205)
    label_c_units = ctk.CTkLabel(new_window,
                    text="J/kgK",
                    font=("Arial", 14))
    label_c_units.place(x=340, y=200)

    label_ro = ctk.CTkLabel(new_window,
                     text="Density",
                     font=("Arial", 14))
    label_ro.place(x=50, y=230)  
    entries["ro"] = ctk.CTkEntry(new_window, width=80)
    entries["ro"].place(x=250, y=235)
    label_ro_units = ctk.CTkLabel(new_window,
                     text="kg/m\u00b3",
                     font=("Arial", 14))
    label_ro_units.place(x=340, y=230)

    label_a_area = ctk.CTkLabel(new_window,
                         text="Plate surface area",
                         font=("Arial", 14))
    label_a_area.place(x=50, y=260)  
    entries["a_area"] = ctk.CTkEntry(new_window, width=80)
    entries["a_area"].place(x=250, y=265)
    label_a_area_units = ctk.CTkLabel(new_window,
                         text="m\u00b2",
                         font=("Arial", 14))
    label_a_area_units.place(x=340, y=260)

    label_num_node = ctk.CTkLabel(new_window,
                          text="Node number",
                          font=("Arial", 14))
    label_num_node.place(x=50, y=290)  
    entries["num_node"] = ctk.CTkEntry(new_window, width=80)
    entries["num_node"].place(x=250, y=295)

    label_delta_tau = ctk.CTkLabel(new_window,
                            text="Time step",
                            font=("Arial", 14))
    label_delta_tau.place(x=50, y=320)  
    entries["delta_tau"] = ctk.CTkEntry(new_window, width=80)
    entries["delta_tau"].place(x=250, y=325)
    label_delta_tau_units = ctk.CTkLabel(new_window,
                            text="sec.",
                            font=("Arial", 14))
    label_delta_tau_units.place(x=340, y=320)  

    label_epsilon = ctk.CTkLabel(new_window,
                          text="Epsilon",
                          font=("Arial", 14))
    label_epsilon.place(x=50, y=350)  
    entries["epsilon"] = ctk.CTkEntry(new_window, width=80)
    entries["epsilon"].place(x=250, y=355)

    button_apply_values = ctk.CTkButton(new_window,
                           text="Apply",
                           command=apply_params)
    button_apply_values.place(x=50, y=400)

    button_delete_values = ctk.CTkButton(new_window,
                           text="Clear",
                           command=clear_params)
    button_delete_values.place(x=250, y=400)

    label_aux_values = ctk.CTkLabel(new_window,
                             text="Aux. values:\n",
                             font=("Arial",14))
    label_aux_values.place(x=450, y=20)

    button_aux_values = ctk.CTkButton(new_window,
                               text="Calculate",
                               command=aux_values)
    button_aux_values.place(x=450, y=400)

    label_ae = ctk.CTkLabel(new_window,
                            text="Factor ae",
                            font=("Arial", 14))
    label_ae.place(x=480, y=50) 
    aux_entries["ae"] = ctk.CTkEntry(new_window, width=80, state="disabled", fg_color='gainsboro')
    aux_entries["ae"].place(x=580, y=50)

    label_ae6 = ctk.CTkLabel(new_window,
                    text="Factor ae6",
                    font=("Arial", 14))
    label_ae6.place(x=480, y=80)
    aux_entries["ae6"] = ctk.CTkEntry(new_window, width=80, state="disabled", fg_color='gainsboro')
    aux_entries["ae6"].place(x=580, y=80)

    label_aw = ctk.CTkLabel(new_window,
                    text="Factor aw",
                    font=("Arial", 14))
    label_aw.place(x=480, y=110)  
    aux_entries["aw"] = ctk.CTkEntry(new_window, width=80, state="disabled", fg_color='gainsboro')
    aux_entries["aw"].place(x=580, y=110)

    label_aw2 = ctk.CTkLabel(new_window,
                    text="Factor aw2",
                    font=("Arial", 14))
    label_aw2.place(x=480, y=140)
    aux_entries["aw2"] = ctk.CTkEntry(new_window, width=80, state="disabled", fg_color='gainsboro')
    aux_entries["aw2"].place(x=580, y=140)

    label_w = ctk.CTkLabel(new_window,
                    text="Factor w",
                    font=("Arial", 14))
    label_w.place(x=480, y=170)
    aux_entries["w"] = ctk.CTkEntry(new_window, width=80, state="disabled", fg_color='gainsboro')
    aux_entries["w"].place(x=580, y=170)

    load_parameters()