import tkinter as tk
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt



def tricontourf_csv():
   
      if len(return_df_stacked_plot_csv()) == 3 or len(return_df_stacked_plot_csv()) == 4 :
              if len(return_df_stacked_plot_csv()) == 3 :
                 x = list(return_df_stacked_plot_csv())
                 plt.tricontourf(x[0] , x[1] , x[2])
                 plt.show()
              if len(return_df_stacked_plot_csv()) == 4 :
                 x = list(return_df_stacked_plot_csv())
                 plt.tricontourf(x[0] , x[1] , x[2] , x[3])
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")