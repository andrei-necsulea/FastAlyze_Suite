import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df_stacked_plot
import matplotlib.pyplot as plt



def fillbetweenx():
   
      if len(list(return_df_stacked_plot())) > 0 :
        
         list_ret_df_stk = list(return_df_stacked_plot())

         if len(list_ret_df_stk) >= 2 and len(list_ret_df_stk) <= 6 :

           if len(list_ret_df_stk) == 2 :
               plt.fill_betweenx(list_ret_df_stk[0] , list_ret_df_stk[1])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()
           
           if len(list_ret_df_stk) == 3 :
               plt.fill_betweenx(list_ret_df_stk[0] , list_ret_df_stk[1] , list_ret_df_stk[2])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk) == 4 :
               plt.fill_betweenx(list_ret_df_stk[0] , list_ret_df_stk[1] , list_ret_df_stk[2] , list_ret_df_stk[3])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk) == 5 :
               print(list_ret_df_stk[0])
               plt.fill_betweenx(list_ret_df_stk[0] , list_ret_df_stk[1] , list_ret_df_stk[2] , list_ret_df_stk[3] , list_ret_df_stk[4])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

           if len(list_ret_df_stk) == 6 :
               plt.fill_betweenx(list_ret_df_stk[0] , list_ret_df_stk[1] , list_ret_df_stk[2] , list_ret_df_stk[3] , list_ret_df_stk[4] , list_ret_df_stk[5])
               thismanager = plt.get_current_fig_manager()
               thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico'))
               plt.show()

         else:
            tk.messagebox.showerror("showerror", "Something went wrong !")