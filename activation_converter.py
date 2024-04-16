import tkinter as tk
from tkinter import *
from tkinter import font
import random as rd

def activate_converter():
   act_window = tk.Tk()
   act_window.geometry("300x250")
   act_window.resizable(0,0)
   act_window.title("Activation")
   act_window.iconbitmap("document_convert.ico")
   l_act = tk.Label(act_window , text = "   Activation key  ")
   l_act.place(relx = 0.5 , anchor = tk.CENTER , rely = 0.1 )
   l_act.config(font = ("Times" , 16))
   e_act = tk.Entry(act_window , width = 33)
   e_act.place(rely = 0.35 , relx = 0.5 , anchor=tk.CENTER )

   def activate_key():
      a_k = e_act.get()
      f = open("activated.txt")
      f.write(a_k)
      s = "!@#$%^&*~"
      for i in range(20 , len(a_k)):
          pass
      if len(a_k) == 24 and a_k[2] in s and a_k[12] in s and a_k[22] in s :
         tk.messagebox.showinfo("Info" , "Your program is successfully activated !")
         #menubar.entryconfig("Activation" , state = "disabled")


   btn_act = tk.Button(act_window ,text = "Activate" , width = 23 , command=activate_key )
   btn_act.place(rely = 0.7 , relx = 0.5 , anchor=tk.CENTER)
   act_window.mainloop()