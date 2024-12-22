import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt


def doughnut_pie():
 
 if len(return_df_stacked_plot()) >= 1 :

   big_list = list(return_df_stacked_plot())
   circle = plt.Circle((0, 0), 0.6, color='white')
   plt.pie(big_list[len(big_list)-1])
   thismanager = plt.get_current_fig_manager()
   thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
   p = plt.gcf()
   p.gca().add_artist(circle)
   plt.show()

 else:
  tk.messagebox.showerror("showerror", "Something went wrong !")