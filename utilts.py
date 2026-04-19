from tkinter import filedialog
from config import params
from calculations import explicit, implicit

def choose_folder(text_box):
    folder_path = filedialog.askdirectory()

    if folder_path:
        text_box.insert("end", f"\nThe folder for saving data has been selected: {folder_path}")
        params.folder_path = folder_path
    
def save_name_txt(text_box, entry_box):
    file_name = entry_box.get()
    text_box.insert("end", f"\nnazwa pliku: {file_name}")
    params.file_name = file_name

def calc_method(combo_box, text_box):
    chosen = combo_box.get()
    file_name_epsilon = str(params.file_name+"_epsilon.txt")
    file = str(params.file_name+".txt")

    if chosen == "Explicit":
        explicit(params.folder_path, file, text_box)

    elif chosen == "Implicit":
        implicit(params.folder_path, file, text_box)

def clear_text(text_box):
    text_box.delete('1.0', 'end')