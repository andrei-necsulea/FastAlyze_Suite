import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt
import pandas as pd

def stacked_bar():
 
 if len(return_df_stacked_plot()) >= 2 :
  big_list = list(return_df_stacked_plot())
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
  ax = df.plot.barh(stacked = True)
  plt.show()

 else:
  tk.messagebox.showerror("showerror", "Something went wrong !")