import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_scatter_x , return_df_scatter_y 
import matplotlib.pyplot as plt



def errorbar():
         
      if len(return_df_scatter_x()) > 0 and len(return_df_scatter_y()) > 0 :

              plt.errorbar(return_df_scatter_x() , return_df_scatter_y())
              

              #changing icon from chart window (it was the matplotlib icon)

              thismanager = plt.get_current_fig_manager()
              thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))

              # ending of the setting

              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")