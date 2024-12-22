import tkinter as tk
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt



def triplot():
   
      if len(return_df_stacked_plot()) == 2 :
                 x = list(return_df_stacked_plot())
                 plt.triplot(x[0] , x[1])
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")