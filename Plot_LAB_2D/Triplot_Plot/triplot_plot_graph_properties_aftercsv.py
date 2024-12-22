import tkinter as tk
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt



def triplot_csv():
   
      if len(return_df_stacked_plot_csv()) == 2 :
                 x = list(return_df_stacked_plot_csv())
                 plt.triplot(x[0] , x[1])
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")