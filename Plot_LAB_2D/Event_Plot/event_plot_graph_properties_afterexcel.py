import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt



def event():
      
      if len(return_df()) > 0 :

              plt.eventplot(return_df())
              

              #changing icon from chart window (it was the matplotlib icon)

              thismanager = plt.get_current_fig_manager()
              thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))

              # ending of the setting

              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")