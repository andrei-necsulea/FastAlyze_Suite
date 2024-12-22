import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt
from File_Reader.import_excel import return_df_stream_plot



def spy():
   
      if len(return_df()) > 0 :
         r = return_df_stream_plot()
         def verify_same_len(x):
                ok = 1
                for i in range(0 , len(x)-1):
                 for j in range(i+1 , len(x)):
                  if len(x[i]) != len(x[j]) :
                       ok = 0
                return ok

         if verify_same_len(r) == 1 :
          plt.spy(r  , markersize = len(r)*len(r) , precision=len(r))
          plt.show()
         else:
          tk.messagebox.showerror("showerror", "Verify if all columns of your table have the same length !")


      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")