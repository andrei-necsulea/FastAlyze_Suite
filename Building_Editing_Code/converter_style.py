import tkinter as tk
from tabula_converter_functions import convert_csv, convert_html, convert_json, convert_odf, convert_pdf, convert_text, convert_xls, convert_xml 

# For the next update ... Hope so :)))
# convert_orc , convert_pkl, convert_sas, convert_spss, convert_stata ,

from tkinter.filedialog import askopenfilename 
from tkinter import *
import subprocess
import os
from tkinter import ttk


def converter():

 main_window = tk.Tk()

 main_window.geometry('550x500')

 main_window.title("FastAlyze TO_EXCEL Converting Tool")

 main_window.iconbitmap("document_convert.ico")

 main_window.config(bg="lightgray")

 main_window.resizable(0 , 0)
 
 menubar = tk.Menu(main_window)
 file1 = tk.Menu(menubar, tearoff=0, background='#ffcc99', foreground='black')  
 menubar.add_cascade(label="File", menu=file1) 

 def exit_f():
  main_window.destroy()
 file1.add_command(label="Exit", command=exit_f )  

 main_window.config(menu = menubar)

 cmb_var = tk.StringVar()
 cmb = ttk.Combobox(main_window , width = 27 , textvariable = cmb_var )


 # For the next update 
 #  , "orc" , "stata(dta)" , "sas(xpt , sas7bdat)" , "spss(sav)" , "pkl"


 cmb['values'] = ('Choose type of file you opened' , "csv" , "pdf" , "txt" , "xls" , "html" , "htm" , "ods" , "xml" , "json")
 cmb.current(0)
 cmb['state'] = "readonly"
 cmb.place(relx = .5 , rely = .6 , anchor = CENTER)
 cmb.configure(font=('Times' , 14))

 e1 = tk.Entry(main_window , width=35  )

 e1.place(relx=0.5 , rely=0.1  , height = 22 , anchor=CENTER )

 e1.config(font = ('Times' , 14))


 global filepath_copy
 filepath_copy = 0
 def open_f():

  global filepath,filepath_copy
  filepath = askopenfilename(
        filetypes=[("All Files", "*.*")]
    )
  e1.insert(0,filepath)


 btn = tk.Button(main_window , width = 25 , height=1 , text = "Open file to be converted" , command=open_f)

 btn.place(relx = .5 , rely =  .3 , anchor=CENTER)

 btn.config(font=("Times" , 12))

 def save():
    filepath = e1.get()

    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    def explore(path):
     path = os.path.normpath(path)
     if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
     elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])


    if filepath.endswith("csv") :
     convert_csv(filepath)
     answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
     if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)

    if filepath.endswith("pdf") :
     convert_pdf(filepath)
     answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
     if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)

    if filepath.endswith("txt") :
      convert_text(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)

    if filepath.endswith("xls") :
      convert_xls(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)

    if filepath.endswith("html") or filepath.endswith("htm") :
      convert_html(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)
    
    if filepath.endswith("ods") :
      convert_odf(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath)

    if filepath.endswith("xml") :
      convert_xml(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 

    if filepath.endswith("json") :
      convert_json(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 
    
    # For the next update ... Hope so :)))
    '''
    if filepath.endswith("orc") :
      convert_orc(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 

    if filepath.endswith("dta") :
      convert_stata(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 

    if filepath.endswith("xpt") or filepath.endswith("sas7bdat") :
      convert_sas(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 

    if filepath.endswith("sav") :
      convert_spss(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 

    if filepath.endswith("pkl") :
      convert_pkl(filepath)
      answer = tk.messagebox.askyesno("Answer", "Your file has been converted successfully ! \n Open file location ?")
      if answer :
         t = filepath.rindex("/")
         x = ""
         for i in range(t+1 , len(filepath)):
           x = x + filepath[i]
         filepath = filepath.removesuffix(x)
         explore(filepath) 
    '''
    

 btn_converter = tk.Button(main_window , width = 30 , height = 1 , text = "Convert to Excel" , command=save)

 btn_converter.place(relx = 0.5 , rely = 0.8 , anchor=CENTER )
 
 btn_converter.config(font = ("Times" , 12))

 main_window.mainloop()