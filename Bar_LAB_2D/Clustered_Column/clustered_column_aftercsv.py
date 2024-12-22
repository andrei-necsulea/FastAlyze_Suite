import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt
import pandas as pd

def clustered_column_csv():
 
 if len(return_df_stacked_plot_csv()) >= 2 :
  big_list = list(return_df_stacked_plot_csv())
  l_combined=[]
  intermediation_list = []

  for i in range(0 , len(big_list[0])):
   for j in range(0 , len(big_list)):
    intermediation_list.append(big_list[j][i])
   l_combined.append(intermediation_list)
   intermediation_list=[]
  
  df = pd.DataFrame(l_combined)
  thismanager = plt.get_current_fig_manager()
  thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
  ax = df.plot.bar()
  plt.show()

 else:
  tk.messagebox.showerror("showerror", "Something went wrong !")