import tkinter as tk

from File_Reader.import_csv import return_df_angle_spectrum_csv
import matplotlib.pyplot as plt
from PyQt5 import QtGui



def angle_csv():
   
      if len(return_df_angle_spectrum_csv()) > 0 :

               r = return_df_angle_spectrum_csv()
               for i in range(len(r)) :
                  plt.angle_spectrum( r[i] )

               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
      else:
        tk.messagebox.showerror("showerror", "Something went wrong !")