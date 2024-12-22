import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt



def hexbin():
   
      if len(return_df_stacked_plot()) == 2 or len(return_df_stacked_plot()) == 3 :
              if len(return_df_stacked_plot()) == 2 :
                 x = list(return_df_stacked_plot())
                 plt.hexbin(x[0] , x[1])
              #changing icon from chart window (it was the matplotlib icon)
                 thismanager = plt.get_current_fig_manager()
                 thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
              # ending of the setting
                 plt.show()
              if len(return_df_stacked_plot()) == 3 :
                 x = list(return_df_stacked_plot())
                 plt.hexbin(x[0] , x[1] , x[2])
              #changing icon from chart window (it was the matplotlib icon)
                 thismanager = plt.get_current_fig_manager()
                 thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
              # ending of the setting
                 plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")