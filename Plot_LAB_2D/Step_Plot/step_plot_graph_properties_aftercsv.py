import tkinter as tk
from File_Reader.import_csv import return_df_scatter_x_csv_f , return_df_scatter_y_csv_f
import matplotlib.pyplot as plt



def step_csv():

      if len(return_df_scatter_x_csv_f()) > 0 and len(return_df_scatter_y_csv_f()) > 0 :

               plt.step(return_df_scatter_x_csv_f() , return_df_scatter_y_csv_f())
               plt.show()
      else:
           tk.messagebox.showerror("showerror", "Something went wrong !")