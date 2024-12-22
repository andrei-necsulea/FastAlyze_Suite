'''
Line2D(xdata, ydata, linewidth=None, linestyle=None, color=None, marker=None, markersize=None, markeredgewidth=None, markeredgecolor=None, markerfacecolor=None, markerfacecoloralt ='none', fillstyle=None, antialiased=None, dash_capstyle=None, solid_capstyle=None, dash_joinstyle=None, solid_joinstyle=None, pickradius=5, drawstyle=None, markevery=None, **kwargs)
'''

import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt



def line_csv():            

      if len(return_df2()) > 0 :
               plt.plot(return_df2())
               plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")
               

      


