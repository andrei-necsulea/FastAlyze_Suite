import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt
from File_Reader.import_excel import return_df_stairs_plot



def stairs():
      
      if len(return_df()) > 0 :
              r = return_df_stairs_plot()
              for i in range(len(r)) :
               plt.stairs( r[i] )  
              plt.show()
      else:
          tk.messagebox.showerror("showerror", "Something went wrong !")