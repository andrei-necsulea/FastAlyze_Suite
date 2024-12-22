import tkinter as tk
from File_Reader.import_excel import return_df_scatter_x , return_df_scatter_y 
import matplotlib.pyplot as plt



def stem():
      if len(return_df_scatter_x()) > 0 and len(return_df_scatter_y()) > 0 :

              plt.stem(return_df_scatter_x() , return_df_scatter_y())
              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")