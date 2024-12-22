import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt



def violin():
   
      if len(return_df()) > 0 :

              plt.violinplot(return_df())
              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")