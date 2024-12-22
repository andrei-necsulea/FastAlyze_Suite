import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt

def sample_pie():
 
 if len(return_df_stacked_plot()) >= 1 :

   big_list = list(return_df_stacked_plot())
   plt.pie(big_list[len(big_list)-1])
   thismanager = plt.get_current_fig_manager()
   thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
   plt.show()

 else:
  tk.messagebox.showerror("showerror", "Something went wrong !")