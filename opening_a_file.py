import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
import pandas as pd
from tkinter import CENTER, ttk

def open_file():
 main = tk.Tk()
 main.geometry("500x500")
 #main.iconbitmap("chart.ico")
 main.resizable(0,0)
 main.title("File Properties")
 main.config(bg = "#9fb49f")

 e1 = tk.Entry(main , width=40)
 e1.place(relx = 0.5 , rely = 0.27 , anchor = tk.CENTER )
 e1.config(font = ("Times" , 12))


 def b2_click():
  os.startfile("table_editor_original.exe")


 def b3_click():
  filepath = askopenfilename(
        filetypes=[ ("CSV Files", "*.csv*") , ("Excel Files", "*.xlsx*") , ("All Files", "*.*")]
    )
   
  e1.insert(0 , filepath)
  
  if filepath.endswith("xlsx"):

    sheet_window = tk.Tk()
    sheet_window.title("Choose Sheet")
    #sheet_window.iconbitmap("chart.ico")
    sheet_window.geometry("280x220")
    sheet_window.config(bg = "#9fb49f")

    df = pd.read_excel(filepath , None)
    sheet_names = list(df.keys())

    cmb_sheet_var = tk.StringVar()
    cmb_sheet = ttk.Combobox(sheet_window , textvariable=cmb_sheet_var , state= "readonly")

    cmb_sheet['values'] = tuple(list(cmb_sheet['values']) + ["Choose sheet"])
    for x in sheet_names:
      cmb_sheet['values'] = tuple(list(cmb_sheet['values']) + [str(x)])
    cmb_sheet.place(relx = 0.5 , rely = 0.5 , anchor=CENTER)
  
  
    def verify_integer_list(lista):
     if all( isinstance(item , int) for item in lista) or all( isinstance(item , float) for item in lista) :
      return True
     else:
      return False

    def cmb_function(event):
     if cmb_sheet.get() != "Choose sheet" :
         df = pd.read_excel(filepath , sheet_name=cmb_sheet.get())
       
         columns_contents = []
         column_names = []

         for i in list(df[df.columns]) :
          column_names.append(i)

         for j in range(len(column_names)):
          columns_contents.append(list(df[column_names[j]]))

         i = 0
         while(i < len(columns_contents)):
          if verify_integer_list(columns_contents[i]) == False :
              columns_contents.remove(columns_contents[i])
          i += 1
         
         

    cmb_sheet.current(0)
    cmb_sheet.bind("<<ComboboxSelected>>" , cmb_function)
    sheet_window.mainloop() 

  if filepath.endswith("csv") :
         df = pd.read_csv(filepath)

         def verify_integer_list(lista):
           if all( isinstance(item , int) for item in lista) or all( isinstance(item , float) for item in lista) or all( isinstance(item , complex) for item in lista) :
            return True
           else:
            return False

         columns_contents = []
         column_names = []

         for i in list(df[df.columns]) :
          column_names.append(i)

         for j in range(len(column_names)):
          columns_contents.append(list(df[column_names[j]]))

         i = 0
         while(i < len(columns_contents)):
          if verify_integer_list(columns_contents[i]) == False :
              columns_contents.remove(columns_contents[i])
          i += 1
        

 b2 = tk.Button(main , width = 30 , text = "EDIT TABLE" , command=b2_click)
 b2.place(relx = 0.5 , rely = 0.57 , anchor=tk.CENTER)

 b3 = tk.Button(main , width = 30 , text = "TABLE DATA TO PLOT" , command=b3_click )
 b3.place(relx = 0.5 , rely = 0.72 , anchor = tk.CENTER)


 main.mainloop()