import tkinter as tk
from File_Reader.import_csv import return_df2
from File_Reader.import_csv import return_df_angle_spectrum_csv
import matplotlib.pyplot as plt


 
def magnitude_csv():
    
      if len(return_df2()) > 0 :

               r = return_df_angle_spectrum_csv()
               for i in range(len(r)) :
                  plt.magnitude_spectrum( r[i] )
               plt.show()
      else:
        tk.messagebox.showerror("Something went wrong !")