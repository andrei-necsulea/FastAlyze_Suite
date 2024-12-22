import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_scatter_x_csv_f , return_df_scatter_y_csv_f
import matplotlib.pyplot as plt



def errorbar_csv():
   
      if len(return_df_scatter_x_csv_f()) > 0 and len(return_df_scatter_y_csv_f()) > 0 :

               plt.errorbar(return_df_scatter_x_csv_f() , return_df_scatter_y_csv_f())
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

      else:
        tk.messagebox.showerror("showerror", "Something went wrong !")