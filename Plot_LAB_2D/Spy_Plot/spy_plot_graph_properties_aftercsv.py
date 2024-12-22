import tkinter as tk
from File_Reader.import_csv import return_df2
import matplotlib.pyplot as plt
from File_Reader.import_csv import return_df_stream_plot_csv



def spy_csv():

      if len(return_df2()) > 0 :

               r_csv = return_df_stream_plot_csv()
               def verify_same_len(x):
                ok = 1
                for i in range(0 , len(x)-1):
                 for j in range(i+1 , len(x)):
                  if len(x[i]) != len(x[j]) :
                       ok = 0
                return ok

               if verify_same_len(r_csv) == 1 :
                plt.spy(r_csv  , markersize = len(r_csv)*len(r_csv) , precision=len(r_csv))
                plt.show()
               else:
                tk.messagebox.showerror("showerror", "Verify if all columns of your table have the same length !")
              
      else:
        tk.messagebox.showerror("showerror", "Something went wrong !")