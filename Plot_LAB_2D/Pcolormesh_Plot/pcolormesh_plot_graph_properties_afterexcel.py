import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt



def pcolormesh():
   
      if len(return_df()) > 0 :
              plt.pcolormesh(return_df())
              plt.show()
      else:
            tk.messagebox.showerror("showerror", "Something went wrong !")