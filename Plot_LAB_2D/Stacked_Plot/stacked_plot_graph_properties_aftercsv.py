import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt
from File_Reader.import_csv import return_df_stacked_plot_csv



def stack_csv():
   
      if len(return_df2()) > 0 :
               
               stk_csv = return_df_stacked_plot_csv()
               plt.stackplot( range(len(stk_csv[0])) , stk_csv[slice(len(stk_csv))] )
               plt.show()
      else:
          tk.messagebox.showerror("showerror", "Something went wrong !")