import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt
from File_Reader.import_excel import return_df_stacked_plot



def stack():
      if len(return_df()) > 0 :

              stk_exc = return_df_stacked_plot()
              plt.stackplot( range(len(stk_exc[0])) , stk_exc[slice(len(stk_exc))] )
              plt.show()

      else:
         tk.messagebox.showerror("showerror", "Something went wrong !")