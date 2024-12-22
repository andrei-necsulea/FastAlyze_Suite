import tkinter as tk
from tkinter import CENTER, font
from tkinter import ttk
import manual_input_data_editor
import opening_a_file
from subplot_properties_support import main , destroy_window

import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

global increment
increment = 0

def subplots_properties() :

 global increment
 global w
  
 try:
    if w.state() == "normal": 
            w.focus()
 except :
  w = tk.Tk()

  def on_closing():
    if tk.messagebox.askokcancel("Quit Subplot Properties", "Do you want to quit?"):
        w.destroy()

  w.protocol("WM_DELETE_WINDOW", on_closing)

  w.title("Subplot properties")

  w.resizable(0 , 0)

  w.iconbitmap(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Plot_LAB_2D\chart.ico")

  w.attributes('-alpha', 0.895)

  w.config(bg = "#9fb49f")
  
  w.geometry("500x500")

  w.grid_columnconfigure(2 , weight=1)
  w.grid_columnconfigure(5 , weight=1)
  w.grid_rowconfigure(1 , weight = 1)
  
  #Principal frame

  w_frame_1 = w.winfo_width()

  h_frame_1 = w.winfo_height()

  frame_1 = tk.Frame(w , bg = "#9fb49f" , width = w_frame_1 , height = h_frame_1 )

  frame_1.pack(fill = "both" , expand = True)

  frame_1.configure( width= w_frame_1 , height = h_frame_1 , border = 0)


  # number of subplots

  nr_subplt = tk.Label(frame_1 , text = "Number of subplots : ")
  nr_subplt.place(relx = 0.35 , rely = 0.2 , anchor=CENTER)
  nr_subplt.config(font=("Times" , 12) , bg = "#9fb49f")

  entry_nr_subplt = tk.Entry(frame_1 , width = 15 )
  entry_nr_subplt.place(relx = 0.7 , rely = 0.2 , height = 25 , anchor=CENTER)
  

  def continue_btn_cmd():
   global increment , frame_x , plot_type

   if entry_nr_subplt.get() != "" and entry_nr_subplt.get().isnumeric() :

       frame_1.pack_forget()

       w_frame_1 = w.winfo_width()

       h_frame_1 = w.winfo_height()

       frame_x = tk.Frame(w , bg = "#9fb49f" , width = w_frame_1 , height = h_frame_1 )
       
       cmb_var = tk.StringVar()
       cmb = ttk.Combobox(frame_x , width = 30 , textvariable = cmb_var )
       cmb['values'] = ('Choose your input data mode' , "Manual" , "Opening a file")
       cmb.current(0)
       cmb['state'] = "readonly"
       cmb.place(relx = 0.5 , rely = 0.3 , anchor=CENTER )
       
       global cmb_vls , cmb_vls_final
       cmb_vls = []
       cmb_vls_final = []

       def get_cmb_value(event):
         global cmb_vls

         if cmb.get() == "Manual" :
           cmb_vls.append(cmb.get()) 
           manual_input_data_editor.manual_data_input_editor()
           

         if cmb.get() == "Opening a file" :
           cmb_vls.append(cmb.get())
           opening_a_file.open_file()
            
            

       cmb.bind("<<ComboboxSelected>>" , get_cmb_value)


       plot_type_var = tk.StringVar()
       plot_type = ttk.Combobox(frame_x , width = 30 , textvariable = plot_type_var )
       plot_type['values'] = ('Choose your plot type' , "Line Plot" , "Scatter Plot" , "Event Plot" ,
       "Box Plot" , "Stack Plot" , "Stem Plot" , "Step Plot",
       "Stairs Plot" , "Angle Spectrum" , "Magnitude Spectrum" ,
       "Phase Spectrum" , "Errorbar Plot" , "P.S.D. Plot",
       "Violin Plot" , "Stream Plot" , "Spy Plot",
       "Imshow Plot" , "Matshow Plot" , "Fillbetween Plot" , 
       "Fillbetweenx Plot" , "Pcolor Plot" , "Pcolormesh Plot",
       "Contour Plot" , "Contourf Plot" , "Tricontour Plot",
       "Tricontourf Plot" , "Quiver Plot" , "Quiverkey Plot",
       "Tripcolor Plot" , "Triplot Plot" , "Hexbin Plot","Barbs Plot" , "Clustered Bar" , "Clustered Column" , "Stacked Bar" , "Stacked Column",
       "Sample Pie" , "Pie of Pie" , "Bar of Pie" , "Doughnut Pie" , "Sample Histogram" , "2D Histogram" , "Pareto Histogram"
       )
       plot_type.current(0)
       plot_type["state"] = "readonly" 
       plot_type.place(relx = 0.5 , rely = 0.45 , anchor=CENTER )

       global list_subplot_type , increment , list_subplot_type_temporary, comb_vls
       list_subplot_type = []
       list_subplot_type_temporary = []
       comb_vls = []

       def get_plot_type(event):
                      global list_subplot_type , increment , list_subplot_type_temporary , comb_vls

                      comb_vls = ["Line Plot" , "Scatter Plot" , "Event Plot" ,
       "Box Plot" , "Stack Plot" , "Stem Plot" , "Step Plot",
       "Stairs Plot" , "Angle Spectrum" , "Magnitude Spectrum" ,
       "Phase Spectrum" , "Errorbar Plot" , "P.S.D. Plot",
       "Violin Plot" , "Stream Plot" , "Spy Plot",
       "Imshow Plot" , "Matshow Plot" , "Fillbetween Plot" , 
       "Fillbetweenx Plot" , "Pcolor Plot" , "Pcolormesh Plot",
       "Contour Plot" , "Contourf Plot" , "Tricontour Plot",
       "Tricontourf Plot" , "Quiver Plot" , "Quiverkey Plot",
       "Tripcolor Plot" , "Triplot Plot" , "Hexbin Plot","Barbs Plot" , "Clustered Bar" , "Clustered Column" , "Stacked Bar" , "Stacked Column",
       "Sample Pie" , "Pie of Pie" , "Bar of Pie" , "Doughnut Pie" , "Sample Histogram" , "2D Histogram" , "Pareto Histogram"]

                      if plot_type.get() in comb_vls :
                            list_subplot_type_temporary.append(plot_type.get())             
                      
       plot_type.bind("<<ComboboxSelected>>" , get_plot_type)
       
       string_1 = "Subplot {} properties"
       string_1 = string_1.format(1)
       plot_x_label = tk.Label(frame_x , text = string_1 )
       plot_x_label.config(font = ("Times" , 16) , bg = "#9fb49f")
       plot_x_label.place(relx = 0.5 , rely = 0.05 , anchor=tk.CENTER)
       

       global x , y
       x = 0 
       
       def count_till_lastone():
            global x
            x += 1
       def return_counting():
            global x
            return x

       global continue_btn_plot_1
       continue_btn_plot_1 = 0


       def next_frame() :

          global list_subplot_type , list_subplot_type_temporary , increment , cmb_vls , comb_vls , cmb_vls , cmb_vls_final
      
          def both_lists():
            global list_subplot_type_temporary , cmb_vls_final
            list_subplot_type.append(list_subplot_type_temporary[len(list_subplot_type_temporary)-1])
            list_subplot_type_temporary = []

            cmb_vls_final.append(cmb_vls[len(cmb_vls)-1])
            cmb_vls_final = []


          try :
            
            both_lists()            

            destroy_window()

            increment += 1

            global y
            count_till_lastone()
            y = return_counting()
            string_1 = "Subplot {} properties"
            string_1 = string_1.format(y+1)

            plot_x_label = tk.Label(frame_x, text=string_1)
            plot_x_label.config(font=("Times", 16), bg="#9fb49f")
            plot_x_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

            if y < int(entry_nr_subplt.get()) :
                   cmb.current(0)
                   plot_type.current(0)

            if y == int(entry_nr_subplt.get()) :
                   if type(continue_btn_plot_1) != int :
                        continue_btn_plot_1.destroy()

                   def generate_fig():
                       print(list_subplot_type)
                       print(cmb_vls_final)
                        

                   str_plot = "        Generate Figure        "
                   continue_btn_plot = tk.Button(frame_x , text = str_plot , command = generate_fig  )
                   continue_btn_plot.place(relx = 0.5 , rely = 0.70 , anchor = CENTER  )
                   continue_btn_plot['font'] = font.Font(family="Times" , size=11)

                   subplots_properties_btn.destroy()

            if y+1 == int(entry_nr_subplt.get()) + 1 :
                plot_x_label.destroy()
           
          except: 

           if len(cmb_vls_final) == 0 or 'Choose your input data mode' in cmb_vls_final :
                     tk.messagebox.showerror("Error" , " Please select a data method !")

           if IndexError or len(list_subplot_type_temporary) == 0 :
              tk.messagebox.showerror("Error" , " Something went wrong !\n Please choose a plot type !")

           if len(list_subplot_type_temporary) < increment + 1 or len(list_subplot_type_temporary) > increment + 1 and increment >= 1 :
            tk.messagebox.showerror("Error" , " Please choose valid plot type every subplot completion !")
          

       str_plot = "      Continue to next Subplot Properties      "
       continue_btn_plot_1 = tk.Button(frame_x , text = str_plot , command = next_frame , width = 30)
       continue_btn_plot_1.place(relx = 0.5 , rely = 0.7 , anchor=CENTER )
       continue_btn_plot_1['font'] = font.Font(family="Times" , size=11)

       subplots_properties_btn = tk.Button(frame_x , text = "Subplot Properties" , width = 30 , command = main)
       subplots_properties_btn.place(relx = 0.5 , anchor=CENTER , rely = 0.8)
       subplots_properties_btn['font'] = font.Font(family="Times" , size=11)  

       frame_x.pack(fill = "both" , expand = True)
       frame_x.configure( width= w_frame_1 , height = h_frame_1 , border = 0)
       frame_x.mainloop()        

   else:
          tk.messagebox.showerror("Error" , "Please enter how many subplots you want !\nNOTE : Enter integer numbers !") 

  
  continue_btn = tk.Button(frame_1 , text = "         Continue         " , command = continue_btn_cmd )
  continue_btn.place(relx = 0.5 , rely = 0.7 , anchor = CENTER  )
  continue_btn['font'] = font.Font(family="Times" , size=11)
  
  w.mainloop()
  
  
  #_______________________________________________________________________________
  frame_1.mainloop()

#subplots_properties()