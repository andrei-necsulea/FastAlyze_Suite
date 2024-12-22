import pandas as pd
from tkinter import filedialog, ttk, messagebox
import tkinter as tk
import numpy as np
import h5py
from pyhdf.SD import SD, SDC
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

df_list_1 = []
df = 0
df_list_scatter_x = []
df_list_scatter_y = []
hdf_filepath = 0

def import_hdf_file():
    def verify_integer_list(lista):
        if all(isinstance(item, int) for item in lista) or all(isinstance(item, float) for item in lista) or all(isinstance(item, complex) for item in lista):
            return True
        else:
            return False

    global df_list_1, df, df_list_scatter_x, df_list_scatter_y, hdf_filepath

    df_list_1 = []
    df_list_scatter_x = []
    df_list_scatter_y = []
    df = 0

    hdf_filepath = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("HDF Files", "*.hdf*;*.h4*;*.h5*"), ("all files", "*.*")))

    if not hdf_filepath:
        return

    dataset_names = []
    try:
        with h5py.File(hdf_filepath, "r") as f:
            dataset_names = list(f.keys())
    except (OSError, IOError):
        try:
            hdf_file = SD(hdf_filepath, SDC.READ)
            dataset_names = hdf_file.datasets().keys()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file: {e}")
            return

    sheet_window = tk.Tk()
    sheet_window.title("Choose Dataset")
    sheet_window.geometry("280x220")
    sheet_window.config(bg="#9fb49f")

    cmb_dataset_var = tk.StringVar()
    cmb_dataset = ttk.Combobox(sheet_window, textvariable=cmb_dataset_var, state="readonly")

    cmb_dataset['values'] = tuple(["Choose dataset"] + list(dataset_names))
    cmb_dataset.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def cmb_function(event):
        global df, df_list_1, df_list_scatter_x, df_list_scatter_y
        if cmb_dataset.get() != "Choose dataset":
            dataset_name = cmb_dataset.get()
            try:
                with h5py.File(hdf_filepath, "r") as f:
                    dataset = f[dataset_name]
                    if isinstance(dataset, h5py.Dataset):
                        data = dataset[()]
                        if data.ndim == 1:
                            data = data.reshape(-1, 1)
                        if data.ndim == 2:
                            df = pd.DataFrame(data)
            except (OSError, IOError):
                try:
                    hdf_file = SD(hdf_filepath, SDC.READ)
                    dataset = hdf_file.select(dataset_name)
                    data = dataset.get()
                    if data.ndim == 1:
                        data = data.reshape(-1, 1)
                    if data.ndim == 2:
                        df = pd.DataFrame(data)
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to read dataset: {e}")
                    return

            remove_names = []
            for i in range(len(df.columns)):
                aux = list(df[df.columns[i]])
                if not verify_integer_list(aux):
                    remove_names.append(df.columns[i])

            for j in remove_names:
                df.drop(j, inplace=True, axis=1)

            df_list_1 = df[df.columns].to_numpy()

            if len(df.columns) == 2:
                df_list_scatter_x = list(df[df.columns[0]])
                df_list_scatter_y = list(df[df.columns[1]])

            sheet_window.destroy()

    cmb_dataset.current(0)
    cmb_dataset.bind("<<ComboboxSelected>>", cmb_function)
    sheet_window.mainloop()

def return_df():
    return df_list_1

def return_df_scatter_x():
    return df_list_scatter_x

def return_df_scatter_y():
    return df_list_scatter_y

def return_df_stacked_plot():
    return_stk_plt = []
    for i in range(len(df.columns)):
        if list(df[df.columns[i]]):
            return_stk_plt.append(list(df[df.columns[i]]))
    return return_stk_plt

def return_df_stairs_plot():
    r = []
    for i in range(len(df.columns)):
        if list(df[df.columns[i]]):
            r.append(list(df[df.columns[i]]))
    return r 

def return_df_angle_spectrum():
    r = []
    for i in range(len(df.columns)):
        if list(df[df.columns[i]]):
            r.append(list(df[df.columns[i]]))
    return r

def return_df_stream_plot():
    r = []
    for i in range(len(df.columns)):
        if list(df[df.columns[i]]):
            r.append(list(df[df.columns[i]]))
    return r


import_hdf_file()