import tkinter as tk
from File_Reader.import_excel import return_df
from File_Reader.import_excel import return_df_angle_spectrum
import matplotlib.pyplot as plt



def psd():

      if len(return_df()) > 0 :

              r = return_df_angle_spectrum()
              for i in range(len(r)) :
               plt.psd( r[i] )
              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")