import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt


def sample_pie_csv():
 
 if len(return_df_stacked_plot_csv()) >= 1 :

   big_list = list(return_df_stacked_plot_csv())
   plt.pie(big_list[len(big_list)-1])
   thismanager = plt.get_current_fig_manager()
   thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
   plt.show()

 else:
  tk.messagebox.showerror("showerror", "Something went wrong !")