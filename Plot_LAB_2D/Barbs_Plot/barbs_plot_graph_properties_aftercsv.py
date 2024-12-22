import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt



def barbs_csv():
   
      if len(return_df_stacked_plot_csv()) > 0 :
        
         list_ret_df_stk_csv = list(return_df_stacked_plot_csv())

         if len(return_df_stacked_plot_csv()) >= 2 and len(return_df_stacked_plot_csv()) <= 5 :

           if len(return_df_stacked_plot_csv()) == 2 :
               plt.barbs(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
           
           if len(return_df_stacked_plot_csv()) == 3 :
               plt.barbs(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(return_df_stacked_plot_csv()) == 4 :
               plt.barbs(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2] , list_ret_df_stk_csv[3])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(return_df_stacked_plot_csv()) == 5 :
               plt.barbs(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2] , list_ret_df_stk_csv[3] , list_ret_df_stk_csv[4])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

         else:
            tk.messagebox.showerror("showerror", "Something went wrong !")