import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt
from File_Reader.import_csv import return_df_stream_plot_csv
import numpy as np



def quiver_csv():

      if len(return_df2()) > 0 :

               r_csv = return_df_stream_plot_csv()
               if len(r_csv) == 2 :
                if len(r_csv[1]) == len(r_csv[0]) :
                 x = np.array(r_csv[0])
                 y = np.array(r_csv[1])
                 u = []
                 v = []
                 for i in range( 2 , len(r_csv[0])+2 ) :
                     u.append(r_csv[i])
                 for j in range(len(r_csv[0])+2 , len(r_csv)) :
                     v.append(r_csv[j])
                 u_cpy = u
                 v_cpy = v
                 if len(u) == len(v) and len(u[0]) == len(u) and len(v[0]) == len(v) and len(r_csv[0]) == len(u[0]) and len(r_csv[0]) == len(v[0]) :
                      u = np.array(u_cpy)
                      v = np.array(v_cpy)
                      plt.quiver(x , y , u , v)
                 plt.show()

               else:
                 tk.messagebox.showerror("showerror", "Something went wrong !")