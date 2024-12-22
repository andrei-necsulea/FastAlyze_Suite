import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt
from File_Reader.import_csv import return_df_stairs_plot_csv



def stairs_csv():
   
      if len(return_df2()) > 0 :
               r_csv = return_df_stairs_plot_csv()
               for i in range(len(r_csv)) :
                plt.stairs( r_csv[i] )  
               plt.show()
      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")