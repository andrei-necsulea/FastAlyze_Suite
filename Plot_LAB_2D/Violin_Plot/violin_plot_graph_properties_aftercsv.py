import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt



def violin_csv():
   
      if len(return_df2()) > 0 :

               plt.violinplot(return_df2())
               plt.show()
      else:
        tk.messagebox.showerror("showerror", "Something went wrong !")