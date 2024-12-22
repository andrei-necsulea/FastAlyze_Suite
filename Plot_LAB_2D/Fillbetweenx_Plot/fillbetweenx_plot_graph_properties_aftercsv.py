import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv
import matplotlib.pyplot as plt



def fillbetweenx_csv():
   
      if len(list(return_df_stacked_plot_csv())) > 0 :

         list_ret_df_stk_csv = list(return_df_stacked_plot_csv())

         if len(list_ret_df_stk_csv) >= 2 and len(list_ret_df_stk_csv) <= 6 :

           if len(list_ret_df_stk_csv) == 2 :
               plt.fill_betweenx(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
           
           if len(list_ret_df_stk_csv) == 3 :
               plt.fill_betweenx(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk_csv) == 4 :
               plt.fill_betweenx(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2] , list_ret_df_stk_csv[3])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk_csv) == 5 :
               plt.fill_betweenx(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2] , list_ret_df_stk_csv[3] , list_ret_df_stk_csv[4])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk_csv) == 6 :
               plt.fill_betweenx(list_ret_df_stk_csv[0] , list_ret_df_stk_csv[1] , list_ret_df_stk_csv[2] , list_ret_df_stk_csv[3] , list_ret_df_stk_csv[4] , list_ret_df_stk_csv[5])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
              
         else:
            tk.messagebox.showerror("showerror", "Something went wrong !")