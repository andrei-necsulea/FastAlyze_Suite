import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt
from File_Reader.import_excel import return_df_stream_plot
import numpy as np



def stream():

      if len(return_df()) > 0 :

         r = return_df_stream_plot()
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
                      plt.streamplot(x , y , u , v)
                 plt.show()

         else:
           tk.messagebox.showerror("showerror", "Something went wrong !")