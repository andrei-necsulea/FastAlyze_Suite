# Creating this file is actually not that hard as I am thinkin' of it
'''
Firstly , I have to import all the libraries from line_plot.py

After that , calling plt.plot(whatever excel file)

Introduce the properties for the chart which will kinda impossible cause I might verify all the entries if are empty or have somethin'
in it and it means to make myself harakiri but I'll got there sooner or later ... anyaway

Finally calling the plt.show() and that's it

In a few words seems such a easy job but these few words are converting to a titanic work for more than a year ... i'll be still here 

I hope :((

'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

prlanguage = 0
def create_file() :
    global prlanguage
    window = tk.Tk() 
    window.title('Choose') 
    window.geometry('300x300')
    window.iconbitmap("chart.ico")
    window.config(bg = "#9fb49f")
  
    n = tk.StringVar() 
    prlanguage = ttk.Combobox(window, width = 27, textvariable = n) 
    prlanguage['values'] = ("Python" , "R" , "MATLAB")
  
    prlanguage.grid(column = 3, row = 6 , pady = 100 , padx = 35) 



    btn = tk.Button(window , text = "Create file" , width = 12 , command = selected)
    btn.config(font = ("Times" , 10) , bg = "lightgray")
    btn.grid(row = 7 , column = 3 , padx = 35)

    window.mainloop()


def selected() :
     text = prlanguage.get()
     print(text)


     



MsgBox = tk.messagebox.askquestion ('File creator','Do you want to create a file with the chart code ?')
if MsgBox == 'yes':
      create_file()
      selected()
else:
    tk.messagebox.showinfo('Return to chart','You will now be returned to your chart')
