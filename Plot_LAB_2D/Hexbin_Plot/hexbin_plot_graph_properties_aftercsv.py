import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt



def hexbin_csv():
   
      if len(return_df_stacked_plot_csv()) == 2 or len(return_df_stacked_plot_csv()) == 3 :
              if len(return_df_stacked_plot_csv()) == 2 :
                 x = list(return_df_stacked_plot_csv())
                 plt.hexbin(x[0] , x[1])
              #changing icon from chart window (it was the matplotlib icon)
                 thismanager = plt.get_current_fig_manager()
                 thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
              # ending of the setting
                 plt.show()
              if len(return_df_stacked_plot_csv()) == 3 :
                 x = list(return_df_stacked_plot_csv())
                 plt.hexbin(x[0] , x[1] , x[2])
              #changing icon from chart window (it was the matplotlib icon)
                 thismanager = plt.get_current_fig_manager()
                 thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
              # ending of the setting
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")