import tkinter as tk
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt



def tricontour():

      if len(return_df_stacked_plot()) == 3 or len(return_df_stacked_plot()) == 4 :
              if len(return_df_stacked_plot()) == 3 :
                 x = list(return_df_stacked_plot())
                 plt.tricontour(x[0] , x[1] , x[2])
                 plt.show()
              if len(return_df_stacked_plot()) == 4 :
                 x = list(return_df_stacked_plot())
                 plt.tricontour(x[0] , x[1] , x[2] , x[3])
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")