import tkinter as tk


def create_user() : 
 global email , password , username
 main_window = tk.Tk()

 main_window.title("Create account")

 main_window.resizable(0 , 0)

 main_window.iconbitmap("create.ico")

 main_window.geometry("500x600")

 main_window.config(bg="#9fb49f")

 email_label = tk.Label(main_window , text="E-mail  :  " )

 email_label.config(font=("Times" , 12) , bg = "#9fb49f")

 email_label.place(relx = 0.15 , rely = 0.1935)

 email = tk.Entry(main_window , width=29 )

 email.place(relx = 0.4 , rely = 0.2 , height=20)

 password_label = tk.Label(main_window , text = "Password  :  ")

 password_label.config(font = ("Times" , 12) , bg = "#9fb49f")

 password_label.place(relx = 0.15 , rely = 0.42 )

 password = tk.Entry(main_window , width = 29 )

 password.place(relx = 0.4 , rely = 0.425 , height = 20 )

 username_label = tk.Label(main_window , text = "Username : ")

 username_label.config(font = ("Times" , 12) , bg = "#9fb49f")

 username_label.place( relx = 0.15 , rely = 0.65 )

 username = tk.Entry(main_window , width = 29)

 username.place(relx = 0.4 , rely = 0.655)

 btn_create_account = tk.Button(main_window , width = 23 , height = 1 , text = "   Create account   " )

 btn_create_account.place( relx = 0.25 , rely = 0.87 )

 btn_create_account.config(bg = "white" , fg = "black")

 main_window.mainloop()
