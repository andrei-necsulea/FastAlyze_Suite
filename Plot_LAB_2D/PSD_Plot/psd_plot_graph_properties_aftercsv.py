import tkinter as tk
from File_Reader.import_csv import return_df2
from File_Reader.import_csv import return_df_angle_spectrum_csv
import matplotlib.pyplot as plt



def psd_csv():

      if len(return_df2()) > 0 :

               r = return_df_angle_spectrum_csv()
               for i in range(len(r)) :
                  plt.psd( r[i] )
               plt.show()

      else:
        tk.messagebox.showerror("showerror", "Something went wrong !")