import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_angle_spectrum
import matplotlib.pyplot as plt



def angle():
      
      if len(return_df_angle_spectrum()) > 0 :

              r = return_df_angle_spectrum()
              for i in range(len(r)) :
               plt.angle_spectrum( r[i] )
              

              #changing icon from chart window (it was the matplotlib icon)

              thismanager = plt.get_current_fig_manager()
              thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))

              # ending of the setting

              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")