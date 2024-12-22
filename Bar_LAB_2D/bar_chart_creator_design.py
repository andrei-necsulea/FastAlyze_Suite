import tkinter as tk
from tkinter import *
from tkinter import font
import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from File_Reader.import_excel import import_excel_file
from File_Reader.import_csv import import_csv_file
from File_Reader.import_word import import_word_file
from docs import open_docs 
import bar_properties_support
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
    if tk.messagebox.askokcancel("Quit BAR LAB 2D", "Do you want to quit?"):
        main_window.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_closing)

main_window.resizable(0,0)
main_window.geometry("750x520")
main_window.title("FastAlyze BAR LAB 2D")
main_window.iconbitmap(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\chart.ico")
main_window.attributes('-alpha', 0.895)
main_window.config(bg = "#9fb49f")
# Main Window


# Menu
def combine_funcs(*funcs):
       def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
       return combined_func



def Excel_counter():
   f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\counter.txt" , "w")
   f.write("Excel")

def CSV_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\counter.txt" , "w")
  f.write("CSV")

def Word_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\counter.txt" , "w")
  f.write("Word")




def clustered_bar_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\bar_type_for_bar_properties.txt" , "w")
  f.write("clustered bar")

def clustered_column_counter():
    f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\bar_type_for_bar_properties.txt" , "w")
    f.write("clustered column")

def stacked_bar_counter():
    f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\bar_type_for_bar_properties.txt" , "w")
    f.write("stacked bar")

def stacked_column_counter():
    f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\bar_type_for_bar_properties.txt" , "w")
    f.write("stacked column")


menubar = tk.Menu(main_window)  

file1 = tk.Menu(menubar, tearoff=0, background='#ffcc99', foreground='black')  
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



editors = tk.Menu(menubar , tearoff=0 , background='#ffcc99')
converters = tk.Menu(menubar , tearoff=0 , background="#ffcc99")

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
frame = tk.Frame(main_window , bg = "#628bcb" , width= w_frame , height = h_frame )
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


clustered_bar_img = PhotoImage(file = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\Clustered_Bar\clustered_bar_1.png")
b1 = tk.Button(frame , image = clustered_bar_img , borderwidth = 0  , command=combine_funcs(clustered_bar_counter , bar_properties_support.main) , compound = "top" , text = "Clustered Bar" , font = font.Font( weight="bold" , size = 12 , family = "Times")  , activebackground = "white" , bg="#bda72a" , border=0.15 )
b1.grid(column = 1 , row = 3 , padx = 65 , pady = 30 ) 


clustered_column_img = PhotoImage(file = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\Clustered_Column\clustered_column_1.png")
b2 = tk.Button(frame , image = clustered_column_img , borderwidth = 0  , command=combine_funcs(clustered_column_counter , bar_properties_support.main) , compound = "top" , text = "Clustered Column" , font = font.Font( weight="bold" , size = 12 , family = "Times")  , activebackground = "white" , bg="#bda72a" , border=0.15 )
b2.grid(column = 2 , row = 3)


stacked_bar_img = PhotoImage(file = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\Stacked_Bar\stacked_bar_1.png")
b3 = tk.Button(frame , image = stacked_bar_img , borderwidth = 0  , command=combine_funcs(stacked_bar_counter , bar_properties_support.main) , compound = "top" , text = "Stacked Bar" , font = font.Font( weight="bold" , size = 12 , family = "Times")  , activebackground = "white" , bg="#bda72a" , border=0.15 )
b3.grid(column = 1 , row = 6)


stacked_column_img = PhotoImage(file = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\Bar_LAB_2D\Stacked_Column\stacked_column_1.png")
b4 = tk.Button(frame , image = stacked_column_img , borderwidth = 0  , command=combine_funcs(stacked_column_counter , bar_properties_support.main) , compound = "top" , text = "Stacked Column" , font = font.Font( weight="bold" , size = 12 , family = "Times")  , activebackground = "white" , bg="#bda72a" , border=0.15 )
b4.grid(column = 2 , row = 6)


# Main Frame


main_window.config(menu=menubar)
frame.mainloop()
main_window.mainloop()