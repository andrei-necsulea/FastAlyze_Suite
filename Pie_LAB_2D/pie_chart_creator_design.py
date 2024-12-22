import os
import sys
import customtkinter as ctk
import tkinter as tk
from tkinter import font
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from File_Reader.import_excel import import_excel_file
from File_Reader.import_csv import import_csv_file
from File_Reader.import_word import import_word_file
from docs import open_docs 
import Pie_LAB_2D.pie_properties_support as pie_properties_support
from Building_Editing_Code.table_editor import table_editor
from Building_Editing_Code.converter_style import converter
import Building_Editing_Code.figure_to_code_support as figure_to_code_support
import Building_Editing_Code.analysis_code_to_python_support as analysis_code_to_python_support
import Building_Editing_Code.python_to_analysis_code_support as python_to_analysis_code_support
from Building_Editing_Code.csv_analyzer import csv_analyzer
from Building_Editing_Code.grain_shape_analyzer import grain_analyzer

# Main Window
main_window = ctk.CTk()

def on_closing():
    if tk.messagebox.askokcancel("Quit PIE LAB 2D", "Do you want to quit?"):
        main_window.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_closing)
main_window.resizable(0, 0)
main_window.geometry("750x520")
main_window.title("FastAlyze PIE LAB 2D")
main_window.iconbitmap(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\chart.ico")
main_window.config(bg="#9fb49f")

# Menu
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def Excel_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\counter.txt", "w") as f:
        f.write("Excel")

def Word_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\counter.txt", "w") as f:
        f.write("Word")

def CSV_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\counter.txt", "w") as f:
        f.write("CSV")

def sample_pie_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\pie_type_for_pie_properties.txt", "w") as f:
        f.write("sample pie")

def pie_of_pie_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\pie_type_for_pie_properties.txt", "w") as f:
        f.write("pie of pie")

def bar_of_pie_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\pie_type_for_pie_properties.txt", "w") as f:
        f.write("bar of pie")

def doughnut_pie_counter():
    with open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Pie_LAB_2D\pie_type_for_pie_properties.txt", "w") as f:
        f.write("doughnut pie")

menubar = tk.Menu(main_window)

file1 = tk.Menu(menubar, tearoff=0, fg='black')
file1.add_command(label="Open Excel File(.xlsx)-SHEET", command=combine_funcs(Excel_counter, import_excel_file))
file1.add_command(label="Open CSV File", command=combine_funcs(import_csv_file, CSV_counter))
file1.add_command(label="Open HDF File(.hdf)-TABLE")
file1.add_command(label="Open Word File(.docx)-TABLE", command=combine_funcs(import_word_file, Word_counter))
file1.add_command(label="Open HTML File(.html)-TABLE")
file1.add_command(label="Open JSON File(.json)")
file1.add_command(label="Open PDF File(.pdf)-TABLE")
file1.add_command(label="Open SQL Database(.sql or link)-TABLE")
file1.add_command(label="Exit", command=main_window.destroy)
menubar.add_cascade(label="File", menu=file1)

help1 = tk.Menu(menubar, tearoff=0, fg='black')
help1.add_command(label="Documentation", command=open_docs)
menubar.add_cascade(label="Help", menu=help1)

editors = tk.Menu(menubar, tearoff=0, fg='black')
editors.add_command(label="Table Editor", command=table_editor)
editors.add_command(label="CSV Editor", command=lambda: os.startfile("CSVBuddy.exe"))
editors.add_command(label="CSV Analyzer", command=csv_analyzer)
editors.add_command(label="Grain Shape Analyzer", command=grain_analyzer)
editors.add_command(label="HDF Editor", command=lambda: os.startfile("HDFView\\HDFView.exe"))
editors.add_command(label="Design Figure Editor", command=lambda: os.startfile("designer.exe"))
menubar.add_cascade(label="File Editors & Analyze Tools", menu=editors)

converters = tk.Menu(menubar, tearoff=0, fg='black')
converters.add_command(label="To Excel File Converter", command=converter)
converters.add_command(label="Figure To Code Converter", command=figure_to_code_support.main)
converters.add_command(label="Analysis code to Python", command=analysis_code_to_python_support.main)
converters.add_command(label="Python to analysis code", command=python_to_analysis_code_support.main)
menubar.add_cascade(label="Converters", menu=converters)

menubar.add_cascade(label="Scientific Calculator", command=lambda: os.startfile("scientific_calc.exe"))

main_window.config(menu=menubar)

# Main Frame
frame = tk.Frame(main_window , bg = "#c48282")
frame.pack(fill="both", expand=True)

frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(6, weight=1)
frame.grid_rowconfigure(9, weight=1)
frame.grid_rowconfigure(12, weight=1)

frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_columnconfigure(4, weight=1)

# Sample Pie Button
sample_pie_img = ctk.CTkImage(light_image=Image.open(os.path.join(os.path.dirname(__file__), '..', "Pie_LAB_2D", "Sample_Pie", "sample_pie_1.png")), size=(180, 150))
b1 = ctk.CTkButton(frame, image=sample_pie_img, border_width=1.5, border_color='lightgray', text="Sample Pie", command=combine_funcs(sample_pie_counter, pie_properties_support.main), fg_color="white", text_color="black", hover_color="white" , compound='top')
b1.grid(column=1, row=3,padx=65, pady=30 )

# Pie of Pie Button
pie_of_pie_img = ctk.CTkImage(light_image=Image.open(os.path.join(os.path.dirname(__file__), '..', "Pie_LAB_2D", "Pie_of_Pie", "pie_of_pie_1.png")), size=(180, 150))
b2 = ctk.CTkButton(frame, image=pie_of_pie_img, border_width=1.5, border_color='lightgray', text="Pie of Pie", command=combine_funcs(pie_of_pie_counter, pie_properties_support.main), fg_color="white", text_color="black", hover_color="white",compound='top')
b2.grid(column=3, row=3)

# Bar of Pie Button
bar_of_pie_img = ctk.CTkImage(light_image=Image.open(os.path.join(os.path.dirname(__file__), '..', "Pie_LAB_2D", "Bar_of_Pie", "bar_of_pie_1.png")), size=(180, 150))
b3 = ctk.CTkButton(frame, image=bar_of_pie_img, border_width=1.5, border_color='lightgray', text="Bar of Pie", command=combine_funcs(bar_of_pie_counter, pie_properties_support.main), fg_color="white", text_color="black", hover_color="white",compound='top')
b3.grid(column=1, row=6,padx=65, pady=30)

# Doughnut Pie Button
doughnut_pie_img = ctk.CTkImage(light_image=Image.open(os.path.join(os.path.dirname(__file__), '..', "Pie_LAB_2D", "Doughnut_Pie", "doughnut_pie_1.png")), size=(180, 150))
b4 = ctk.CTkButton(frame, image=doughnut_pie_img, border_width=1.5, border_color='lightgray', text="Doughnut Pie", command=combine_funcs(doughnut_pie_counter, pie_properties_support.main), fg_color="white", text_color="black", hover_color="white",compound='top')
b4.grid(column=3, row=6)

main_window.mainloop()
