import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt



def box_csv() :

      if len(return_df2()) > 0 :

               plt.boxplot(return_df2())
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")