import pandas as pd
from tkinter import filedialog , ttk
import tkinter as tk
import numpy as np


import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

df_list_1 = []

df = 0

df_list_scatter_x = []

df_list_scatter_y = []

excel_filepath = 0


def import_excel_file() :
     

     def verify_integer_list(lista):
       if all( isinstance(item , int) for item in lista) or all( isinstance(item , float) for item in lista) or all( isinstance(item , complex) for item in lista) :
         return True
       else:
         return False
     
     global df_list_1 , df , counter 
     global df_list_scatter_x , df_list_scatter_y , excel_filepath

     df_list_1 = []

     df_list_scatter_x = []

     df_list_scatter_y = []

     df = 0

     excel_filepath = filedialog.askopenfilename(initialdir = "/" , title = "Select a File" , filetypes = (("Excel worksheet" , "*.xlsx*" ) , ("all files","*.*") ))
     
     sheet_window = tk.Tk()
     sheet_window.title("Choose Sheet")
     sheet_window.iconbitmap(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\File_Reader\chart.ico")
     sheet_window.geometry("280x220")
     sheet_window.config(bg = "#9fb49f")

     df_1 = pd.read_excel(excel_filepath , None)
     sheet_names = list(df_1.keys())

     cmb_sheet_var = tk.StringVar()
     cmb_sheet = ttk.Combobox(sheet_window , textvariable=cmb_sheet_var , state= "readonly")

     cmb_sheet['values'] = tuple(list(cmb_sheet['values']) + ["Choose sheet"])
     for x in sheet_names:
      cmb_sheet['values'] = tuple(list(cmb_sheet['values']) + [str(x)])
     cmb_sheet.place(relx = 0.5 , rely = 0.5 , anchor=tk.CENTER)


     def cmb_function(event):
      global df , df_list_1 , df_list_scatter_x , df_list_scatter_y
      if cmb_sheet.get() != "Choose sheet" :
         df = pd.read_excel(excel_filepath , sheet_name=cmb_sheet.get())

         remove_names = []

         for i in range(len(list(df[df.columns]))) :
             aux = list(df[df.columns[i]])
             if verify_integer_list(aux) == False :
                       remove_names.append(df.columns[i])

     
         for j in remove_names:
          df.drop(j , inplace=True, axis=1)

         df_list_1 = df[df.columns].to_numpy()
    
         if len(list(df.columns)) == 2 :
           df_list_scatter_x = list(df[df.columns[0]])
           df_list_scatter_y = list(df[df.columns[1]])

         sheet_window.destroy()
       
         
     cmb_sheet.current(0)
     cmb_sheet.bind("<<ComboboxSelected>>" , cmb_function)
     sheet_window.mainloop()


def return_df() :
     return df_list_1

def return_df_scatter_x():
     return df_list_scatter_x


def return_df_scatter_y() :
    return df_list_scatter_y


def return_df_stacked_plot():
     return_stk_plt = []
     for i in range(len(list(df.columns))) :
       if list(df[df.columns[i]]) :
          return_stk_plt.append(list(df[df.columns[i]]))
     return return_stk_plt

def return_df_stairs_plot():
     r = []
     for i in range(len(df.columns)) :
       if list(df[df.columns[i]]) :
          r.append(list(df[df.columns[i]]))
     return r 

def return_df_angle_spectrum():
     r = []
     for i in range(len(df.columns)):
       if list(df[df.columns[i]]) :
          r.append(list(df[df.columns[i]]))
     return r

def return_df_stream_plot():
     r = []
     for i in range(len(df.columns)):
       if list(df[df.columns[i]]) :
          r.append(list(df[df.columns[i]]))
     return r 