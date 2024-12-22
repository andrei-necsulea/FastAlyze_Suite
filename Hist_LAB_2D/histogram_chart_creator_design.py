import tkinter as tk
import customtkinter as ctk
from tkinter import *
from PIL import Image
from tkinter import font
import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from File_Reader.import_excel import import_excel_file
from File_Reader.import_csv import import_csv_file
from File_Reader.import_word import import_word_file
from docs import open_docs 
import hist_properties_support
from Building_Editing_Code.table_editor import table_editor
from Building_Editing_Code.converter_style import converter
import Building_Editing_Code.figure_to_code_support as figure_to_code_support
import Building_Editing_Code.analysis_code_to_python_support as analysis_code_to_python_support
import Building_Editing_Code.python_to_analysis_code_support as python_to_analysis_code_support
from Building_Editing_Code.csv_analyzer import csv_analyzer
from Building_Editing_Code.grain_shape_analyzer import grain_analyzer


# Main Window 
main_window = tk.Tk()

def on_closing():
    if tk.messagebox.askokcancel("Quit HIST LAB 2D", "Do you want to quit?"):
        main_window.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_closing)
main_window.resizable(0,0)
main_window.geometry("750x520")
main_window.title("FastAlyze HIST LAB 2D")
main_window.iconbitmap(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\chart.ico")
#main_window.attributes('-alpha', 0.895)
main_window.config(bg = "#9fb49f")
# Main Window


# Menu
def combine_funcs(*funcs):
       def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
       return combined_func



def Excel_counter():
   f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\counter.txt" , "w")
   f.write("Excel")
   
def CSV_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\counter.txt" , "w")
  f.write("CSV")

def Word_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\counter.txt" , "w")
  f.write("Word")



  
def hist_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\hist_type_for_hist_properties.txt" , "w")
  f.write("hist")

def hist_2d_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\hist_type_for_hist_properties.txt" , "w")
  f.write("hist 2d")

def pareto_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\hist_type_for_hist_properties.txt" , "w")
  f.write("pareto")

menubar = tk.Menu(main_window)  

file1 = tk.Menu(menubar, tearoff=0, background='white', foreground='black')  
file1.add_command(label="Open Excel File(.xlsx)-SHEET" , command = combine_funcs(Excel_counter , import_excel_file) )  
file1.add_command(label="Open CSV File" , command = combine_funcs(import_csv_file , CSV_counter)  ) 
file1.add_command(label="Open HDF File(.hdf)-TABLE") 
file1.add_command(label="Open Word File(.docx)-TABLE" , command = combine_funcs(import_word_file , Word_counter)) 
file1.add_command(label="Open HTML File(.html)-TABLE") 
file1.add_command(label="Open JSON File(.json)") 
file1.add_command(label="Open PDF File(.pdf)-TABLE") 
file1.add_command(label="Open SQL Database(.sql or link)-TABLE") 

def exit_f():
  main_window.destroy()

file1.add_command(label="Exit", command=exit_f )  

menubar.add_cascade(label="File", menu=file1) 

#account = tk.Menu(menubar , tearoff = 0 , background = "#ffcc99")
#account.add_command(label = "Create account" , command = create_user )
#account.add_command(label = "Log in" , command = login_user )

#menubar.add_cascade(label = "Account" , menu = account)
help1 = tk.Menu(menubar, tearoff=0 , background='#ffcc99')  


def open_hdf_editor():
  os.startfile("HDFView\HDFView.exe")

def open_designer():
  os.startfile("designer.exe")

def open_csv_editor():
  os.startfile("CSVBuddy.exe")



editors = tk.Menu(menubar , tearoff=0 , background='white')
converters = tk.Menu(menubar , tearoff=0 , background="white")

editors.add_command(label = "Table Editor"  , command=table_editor)
editors.add_command(label = "CSV Editor" , command = open_csv_editor)
editors.add_command(label = "CSV Analyzer" , command = csv_analyzer)
editors.add_command(label = "Grain Shape Analyzer" , command = grain_analyzer)
editors.add_command(label = "HDF Editor" , command=open_hdf_editor)
editors.add_command(label = "Design Figure Editor" , command=open_designer)
menubar.add_cascade(label = "File Editors & Analyze Tools" , menu = editors)

converters.add_command(label = "To Excel File Converter"  , command=converter)
converters.add_command(label="Figure To Code Converter" , command=figure_to_code_support.main)
converters.add_command(label="Analysis code to Python" , command=analysis_code_to_python_support.main) 
converters.add_command(label="Python to analysis code" , command=python_to_analysis_code_support.main) 
menubar.add_cascade(label = "Converters" , menu = converters)
def scy_calc():
  os.startfile("scientific_calc.exe")

menubar.add_cascade(label = "Scientific Calculator" , command=scy_calc)
help1.add_command(label="Documentation" , command = open_docs)  
menubar.add_cascade(label="Help", menu=help1)
# Menu

# Main Frame 
w_frame = main_window.winfo_width()
h_frame = main_window.winfo_height()
frame = tk.Frame(main_window , bg = "#9390c1" , width= w_frame , height = h_frame )
frame.configure(width = w_frame , height = h_frame , border=0 )
frame.pack(fill = "both" , expand = True)

frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(6, weight=1)
frame.grid_rowconfigure(9, weight=1)
frame.grid_rowconfigure(12, weight=1)

frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_columnconfigure(4, weight=1)


hist_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\Sample_Hist\histogram_1.png") , size=(170 , 150))
b1 = ctk.CTkButton(frame , image = hist_img , corner_radius = 30 , border_width = 1.5 , border_color="lightgray"  , command=combine_funcs(hist_counter,hist_properties_support.main) , compound = "top" , text = "Sample Histogram" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" )
b1.place(relx = 0.3 , rely = 0.25 , anchor = CENTER)


hist2d_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\TwoD_Hist\histogram2d_1.png"), size=(170 , 150))
b2 = ctk.CTkButton(frame , image = hist2d_img , corner_radius=30 ,border_width = 1.5  , command=combine_funcs(hist_2d_counter,hist_properties_support.main) , compound = "top" , text = "2D Histogram" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" )
b2.place(relx = 0.7 , rely = 0.25 , anchor=CENTER)


pareto_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Hist_LAB_2D\Pareto_Hist\pareto_1.png"), size=(170 , 150))
b3 = ctk.CTkButton(frame , image = pareto_img , corner_radius=30 ,border_width = 1.5  , command=combine_funcs(pareto_counter,hist_properties_support.main) , compound = "top" , text = "Pareto Histogram" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times") , fg_color = "white" , text_color="black" , hover_color="white" )
b3.place(anchor = CENTER , relx = 0.5 , rely = 0.73)


# Main Frame

main_window.config(menu=menubar)
frame.mainloop()
main_window.mainloop()