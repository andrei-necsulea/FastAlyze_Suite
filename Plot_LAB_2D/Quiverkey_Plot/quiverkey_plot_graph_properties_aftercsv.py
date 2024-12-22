import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt
from File_Reader.import_csv import return_df_stream_plot_csv
import numpy as np



def quiverkey_csv():

      if len(return_df2()) > 0 :

            r = return_df_stream_plot_csv()
            if len(r) == 2 :
             if len(r[1]) == len(r[0]) :
                 x = np.array(r[0])
                 y = np.array(r[1])
                 u = []
                 v = []
                 for i in range( 2 , len(r[0])+2 ) :
                     u.append(r[i])
                 for j in range(len(r[0])+2 , len(r)) :
                     v.append(r[j])
                 u_cpy = u
                 v_cpy = v
                 if len(u) == len(v) and len(u[0]) == len(u) and len(v[0]) == len(v) and len(r[0]) == len(u[0]) and len(r[0]) == len(v[0]) :
                      u = np.array(u_cpy)
                      v = np.array(v_cpy)
                      s = plt.quiver(x , y , u , v)
                      plt.quiverkey(s , 0.5 , 0.5 , 0.5 , label ='Quiver key')
                 plt.show()

            else:
                   tk.messagebox.showerror("showerror", "Something went wrong !")