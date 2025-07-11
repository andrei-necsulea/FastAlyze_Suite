import tkinter as tk
import customtkinter as ctk
from tkinter import *
from tkinter import font
from ttkwidgets.frames import Tooltip
from PIL import Image
import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from File_Reader import import_excel , import_csv , import_word 
from Building_Editing_Code import analysis_code_to_python_support , python_to_analysis_code_support , figure_to_code_support , converter_style , table_editor , csv_analyzer , grain_shape_analyzer
from docs import open_docs 
from Line_Plot import line_plot_graph_properties_afterexcel



#____________________________________________________________________________________________________

main_window = Tk()

def on_closing():
    if tk.messagebox.askokcancel("Quit PLOT LAB 2D", "Do you want to quit?"):
        main_window.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_closing)


main_window.title("FastAlyze PLOT LAB 2D")

main_window.state('zoomed')

main_window.resizable(1 , 1)

main_window.iconbitmap( str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\chart.ico")

#main_window.attributes('-alpha', 0.895)

#_______________________________________________________________________________________________
####################################################################################################   

   # combining 2 functions for the button
def combine_funcs(*funcs):
       def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
       return combined_func


def Excel_counter():
   f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\counter.txt" , "w")
   f.write("Excel")

   
def CSV_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\counter.txt" , "w")
  f.write("CSV")

def Word_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\counter.txt" , "w")
  f.write("Word")



def line_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("line")

def scatter_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("scatter")

def event_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("event")

def box_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("box")

def stack_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("stack")

def stem_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("stem")

def step_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("step")

def stairs_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("stairs")

def angle_spectrum_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("angle")

def magnitude_spectrum_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("magnitude")

def phase_spectrum_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("phase")

def errorbar_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("errorbar")

def psd_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("psd")

def violin_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("violin")

def stream_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("stream")

def spy_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("spy")

def imshow_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("imshow")

def matshow_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("matshow")

def fillbetween_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("fillbetween")

def fillbetweenx_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("fillbetweenx")

def pcolor_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("pcolor")

def pcolormesh_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("pcolormesh")

def contour_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("contour")

def contourf_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("contourf")

def tricontour_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("tricontour")

def tricontourf_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("tricontourf")

def quiver_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("quiver")

def quiverkey_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("quiverkey")

def tripcolor_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("tripcolor")

def triplot_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("triplot")

def hexbin_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("hexbin")

def barbs_plot_counter():
  f = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\plot_type_for_plot_properties.txt" , "w")
  f.write("barbs")
      
####################################################################################################
# Menu starts here 

menubar = tk.Menu(main_window)  

file1 = tk.Menu(menubar, tearoff=0, background='white', foreground='black')  
file1.add_command(label="Open Excel File(.xlsx)-SHEET" , command = combine_funcs(Excel_counter , import_excel.import_excel_file) )  
file1.add_command(label="Open CSV File" , command = combine_funcs(import_csv.import_csv_file , CSV_counter)  ) 
file1.add_command(label="Open HDF File(.hdf)-TABLE") 
file1.add_command(label="Open Word File(.docx)-TABLE" , command = combine_funcs(import_word.import_word_file , Word_counter)) 
file1.add_command(label="Open HTML File(.html)-TABLE") 
file1.add_command(label="Open JSON File(.json)") 
file1.add_command(label="Open PDF File(.pdf)-TABLE") 
file1.add_command(label="Open SQL Database(.sql or link)-TABLE") 

def exit_f():
  main_window.destroy()

file1.add_command(label="Exit", command=exit_f )  

menubar.add_cascade(label="File", menu=file1) 

help1 = tk.Menu(menubar, tearoff=0 , background='white')  


def open_hdf_editor():
  os.startfile(r"HDFView\HDFView.exe")

def open_designer():
  os.startfile("designer.exe")

def open_csv_editor():
  os.startfile("CSVBuddy.exe")

editors = tk.Menu(menubar , tearoff=0 , background='white')
converters = tk.Menu(menubar , tearoff=0 , background="white")

editors.add_command(label = "Table Editor"  , command=table_editor)
editors.add_command(label = "CSV Editor" , command = open_csv_editor)
editors.add_command(label = "CSV Analyzer" , command = csv_analyzer)
editors.add_command(label = "Grain Shape Analyzer" , command = grain_shape_analyzer.grain_analyzer)
editors.add_command(label = "HDF Editor" , command=open_hdf_editor)
editors.add_command(label = "Design Figure Editor" , command=open_designer)
menubar.add_cascade(label = "File Editors & Analyze Tools" , menu = editors)

converters.add_command(label = "To Excel File Converter"  , command=converter_style.converter)
converters.add_command(label="Figure To Code Converter" , command=figure_to_code_support.main)
converters.add_command(label="Analysis code to Python" , command=analysis_code_to_python_support.main) 
converters.add_command(label="Python to analysis code" , command=python_to_analysis_code_support.main) 
menubar.add_cascade(label = "Converters" , menu = converters)

help1.add_command(label="Documentation" , command = open_docs)  
menubar.add_cascade(label="Help", menu=help1)


# Menu finished

#__________________________________________________________________________________________________
##abdbe3
w_frame_1 = main_window.winfo_width()

h_frame_1 = main_window.winfo_height()

frame_1 = tk.Frame(main_window , bg = "#D8E7EF" , width = w_frame_1 , height = h_frame_1 )

frame_1.pack(fill = "both" , expand = True)


# Scrollbar here

frame_1.grid_rowconfigure(3, weight=1)
frame_1.grid_rowconfigure(6, weight=1)
frame_1.grid_rowconfigure(9, weight=1)
frame_1.grid_rowconfigure(12, weight=1)

frame_1.grid_columnconfigure(1, weight=1)
frame_1.grid_columnconfigure(2, weight=1)
frame_1.grid_columnconfigure(3, weight=1)
frame_1.grid_columnconfigure(4, weight=1)


#_______________________________________________________________

# Line Plot button
#bg="#bda72a"
#border=0.15
line_plot_img = ctk.CTkImage(light_image= Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Line_Plot\Line_Plot_1.png") , size=(110,110))

b1 = ctk.CTkButton(frame_1 , image = line_plot_img , border_color='lightgray'  , border_width = 1.5 , command = combine_funcs(line_plot_counter , line_plot_graph_properties_afterexcel.line) , compound = "top" , text = "Line Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b1.grid(column = 1 , row = 3 ,   pady = 1 , padx = 1)
#bf9319

# Line Plot button



# Scatter Plot btn

scatter_plot_img = ctk.CTkImage(light_image= Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Scatter_Plot\Scatter_Plot_1.png") , size = (110,110))

b2 = ctk.CTkButton(frame_1 , image = scatter_plot_img  , border_color='lightgray'  , border_width = 1.5 , command = scatter_plot_counter  ,  compound = "top" , text = "Scatter Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30  )

b2.grid(column = 2 , row = 3 , padx = 1)

# Scatter Plot btn



# Event Plot btn

event_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Event_Plot\Event_Plot_1.png") , size = (110,110))

b3 = ctk.CTkButton(frame_1 , image = event_plot_img , border_color='lightgray'  , border_width = 1.5, command = event_plot_counter , compound = "top" , text = "Event Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b3.grid(column = 3 , row = 3 , padx = 1)

# Event Plot btn




# Box Plot btn

box_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Box_Plot\Box_Plot_1.png") , size = (110,110))

b4 = ctk.CTkButton(frame_1 ,  image = box_plot_img  , border_color='lightgray'  , border_width = 1.5 , command = box_plot_counter , compound = "top" , text = "Box Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b4.grid(row = 3 , column = 4 , padx = 1)

# Box Plot btn



# Stacked Plot btn

stacked_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Stacked_plot\Stacked_Plot_1.png") , size = (110,110))

b5 = ctk.CTkButton(frame_1, image = stacked_plot_img , border_color='lightgray'  , border_width = 1.5, command = stack_plot_counter , compound = "top" , text = "Stack Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b5.grid(column = 1 , row = 6 , padx = 1 , pady = 1)

# Stacked Plot btn



# Stem Plot btn

stem_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Stem_Plot\Stem_Plot_1.png") , size = (110,110))

b6 = ctk.CTkButton(frame_1 , image = stem_plot_img ,  border_color='lightgray'  , border_width = 1.5 , command = stem_plot_counter , compound = "top" , text = "Stem Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30)
b6.grid(column = 2 , padx = 1 , row = 6)

# Stem Plot btn



# Step Plot btn

step_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Step_Plot\Step_Plot_1.png") , size = (110,110))

b7 = ctk.CTkButton(frame_1 , image = step_plot_img , border_color='lightgray'  , border_width = 1.5 , command = step_plot_counter, compound = "top" , text = "Step Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b7.grid(column = 3  , padx = 1 , row = 6)

# Step Plot btn



# Stairs Plot btn

stairs_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Stairs_Plot\Stairs_Plot_1.png") , size = (110,110))

b8 = ctk.CTkButton(frame_1 , image = stairs_plot_img , border_color='lightgray'  , border_width = 1.5 , command = stairs_plot_counter , compound = "top" , text = "Stairs Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b8.grid(column = 4  , row = 6 , padx = 1)

# Stairs Plot btn



# Angle spectrum

angle_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Angle_Spectrum\Angel_Spectrum_1.png") , size = (110,110))

b9 = ctk.CTkButton(frame_1 , image = angle_plot_img , border_color='lightgray'  , border_width = 1.5 , command = angle_spectrum_counter, compound = "top" , text = "Angle Spectrum" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b9.grid(column = 1 , padx = 1 , row = 9 , pady = 1)

# Angle Spectrum



# Magnitude spectrum

magnitude_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Magnitude_Spectrum\Magnitude_Spectrum_1.png") , size = (110,110))

b10 = ctk.CTkButton(frame_1 , image = magnitude_plot_img , border_color='lightgray'  , border_width = 1.5 , command = magnitude_spectrum_counter , compound = "top" , text = "Magnitude Spectrum" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b10.grid(column = 2 , padx = 1 , row = 9)

# Magnitude spectrum



# Phase spectrum

phase_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Phase_Spectrum\Phase_Spectrum_1.png") , size = (110,110))

b11 = ctk.CTkButton(frame_1 , image = phase_plot_img , border_color='lightgray'  , border_width = 1.5 , command = phase_spectrum_counter , compound = "top" , text = "Phase Spectrum" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30)

b11.grid(column = 3 , padx = 1 , row = 9)

# Phase spectrum



# Errorbar plot

errorbar_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Errorbar_Plot\Errorbar_Plot_1.png") , size = (110,110))

b12 = ctk.CTkButton(frame_1 , image = errorbar_plot_img , border_color='lightgray'  , border_width = 1.5 , command = errorbar_plot_counter , compound = "top" , text = "Errorbar Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b12.grid(column = 4 , padx = 1 , row = 9)

# Errorbar plot




# PSD Plot

psd_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\PSD_Plot\PSD_Plot_1.png") , size = (110,110))

b13 = ctk.CTkButton(frame_1 , image = psd_plot_img , border_color='lightgray'  , border_width = 1.5, command = psd_plot_counter , compound = "top" , text = "P.S.D. Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b13.grid(column = 1 , padx = 1 , row = 12 , pady = 1)

# PSD Plot



# Violin Plot

violin_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Violin_Plot\Violin_Plot_1.png") , size = (110,110))

b14 = ctk.CTkButton(frame_1 , image = violin_plot_img , border_color='lightgray'  , border_width = 1.5 , command = violin_plot_counter , compound = "top" , text = "Violin Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b14.grid(column = 2 , padx = 1 , row = 12)

# Violin Plot



# Stream Plot

stream_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Stream_Plot\Stream_Plot_1.png") , size = (110,110))

b15 = ctk.CTkButton(frame_1 , image = stream_plot_img , border_color='lightgray'  , border_width = 1.5, command = stream_plot_counter , compound = "top" , text = "Stream Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30  )

b15.grid(column = 3 , padx = 1 , row = 12)

# Stream Plot



# Spy Plot

spy_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Spy_Plot\Spy_Plot_1.png") , size = (110,110))

b16 = ctk.CTkButton(frame_1 , image = spy_plot_img , border_color='lightgray'  , border_width = 1.5, command = spy_plot_counter , compound = "top" , text = "Spy Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30 )

b16.grid(column = 4 , padx = 1 , row = 12)



# Spy Plot


# Buttons finished 

#________________________________________________________________________________________________________________________________________-

w_frame = main_window.winfo_width()

h_frame = main_window.winfo_height()

frame = tk.Frame(main_window , bg = "#6da897" , width= w_frame , height = h_frame )
#frame.grid(column = 0 , row = 0 )
#frame.pack(fill = "both" , expand = True)

# Scrollbar here

frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(6, weight=1)
frame.grid_rowconfigure(9, weight=1)
frame.grid_rowconfigure(12, weight=1)

frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_columnconfigure(4, weight=1)

'''
main_window.grid_rowconfigure(3, weight=1)
main_window.grid_rowconfigure(6, weight=1)
main_window.grid_rowconfigure(7 , weight=1)
main_window.grid_rowconfigure(9, weight=1)
main_window.grid_rowconfigure(12, weight=1)

main_window.grid_columnconfigure(1, weight=1)
main_window.grid_columnconfigure(2, weight=1)
main_window.grid_columnconfigure(3, weight=1)
main_window.grid_columnconfigure(4, weight=1)
'''

# Scrollbar finished




#___________________________________________________________________________________________________________________________________________


  
# Imshow Plot button
 
imshow_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Imshow_Plot\Imshow_Plot_1.png") , size = (110,110))

b1_1 = ctk.CTkButton(frame, image = imshow_plot_img , border_color='lightgray'  , border_width = 1.5, command = imshow_plot_counter , compound = "top" , text = "Imshow Plot" , font = ctk.CTkFont(weight="bold", size = 14 , family = "Times")  , fg_color = "white" , text_color="black" , hover_color="white" , corner_radius=30)

b1_1.grid(column = 1 , row = 3 ,   pady = 1 , padx = 1)

# Imshow Plot button




# Matshow Plot btn
 
matshow_plot_img = ctk.CTkImage(light_image = Image.open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + r"\Plot_LAB_2D\Matshow_Plot\Matshow_Plot_1.png") , size = (110,110))
  
b2_1 = ctk.CTkButton(frame , image = matshow_plot_img  , border_width = 1.5 , border_color='lightgray' , compound = "top" , text = "Matshow Plot" , font = ctk.CTkFont( weight="bold" , size = 12 , family = "Times") , command = matshow_plot_counter , fg_color="white" , text_color="black", hover_color="white" , corner_radius=30  )

b2_1.grid(column = 2 , row = 3 , padx = 1)

# Matshow Plot btn


# Fillbetween Plot btn
fillbetween_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Fillbetween_Plot", "Fillbetween_Plot_1.png"))), size=(110, 110))
b3_1 = ctk.CTkButton(frame, image=fillbetween_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Fillbetween Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = fillbetween_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b3_1.grid(column=3, row=3, padx=1)

# Fillbetweenx Plot btn
fillbetweenx_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Fillbetweenx_Plot", "Fillbetweenx_Plot_1.png"))), size=(110, 110))
b4_1 = ctk.CTkButton(frame, image=fillbetweenx_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Fillbetweenx Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = fillbetweenx_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b4_1.grid(row=3, column=4, padx=1)

# Pcolor Plot btn
pcolor_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Pcolor_Plot", "Pcolor_Plot_1.png"))), size=(110, 110))
b5_1 = ctk.CTkButton(frame, image=pcolor_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Pcolor Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = pcolor_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b5_1.grid(column=1, row=6, padx=1, pady=1)

# Pcolormesh Plot btn
pcolormesh_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Pcolormesh_Plot", "Pcolormesh_Plot_1.png"))), size=(110, 110))
b6_1 = ctk.CTkButton(frame, image=pcolormesh_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Pcolormesh Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = pcolormesh_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b6_1.grid(column=2, padx=1, row=6)

# Contour Plot btn
contour_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Contour_Plot", "Contour_Plot_1.png"))), size=(110, 110))
b7_1 = ctk.CTkButton(frame, image=contour_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Contour Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = contour_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b7_1.grid(column=3, padx=1, row=6)

# Contourf Plot btn
contourf_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Contourf_Plot", "Contourf_Plot_1.png"))), size=(110, 110))
b8_1 = ctk.CTkButton(frame, image=contourf_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Contourf Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = contourf_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b8_1.grid(column=4, row=6, padx=1)

# Tricontour Plot btn
tricontour_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Tricontour_Plot", "Tricontour_Plot_1.png"))), size=(110, 110))
b9_1 = ctk.CTkButton(frame, image=tricontour_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Tricontour Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = tricontour_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b9_1.grid(column=1, padx=1, row=9, pady=1)

# Tricontourf Plot btn
tricontourf_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Tricontourf_Plot", "Tricontourf_Plot_1.png"))), size=(110, 110))
b10_1 = ctk.CTkButton(frame, image=tricontourf_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Tricontourf Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = tricontourf_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b10_1.grid(column=2, padx=1, row=9)

# Quiver Plot btn
quiver_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Quiver_Plot", "Quiver_Plot_1.png"))), size=(110, 110))
b11_1 = ctk.CTkButton(frame, image=quiver_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Quiver Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = quiver_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b11_1.grid(column=3, padx=1, row=9)

# Quiverkey Plot btn
quiverkey_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Quiverkey_Plot", "Quiverkey_Plot_1.png"))), size=(110, 110))
b12_1 = ctk.CTkButton(frame, image=quiverkey_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Quiverkey Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command = quiverkey_plot_counter, fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b12_1.grid(column=4, padx=1, row=9)

# Tripcolor Plot btn
tripcolor_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Tripcolor_Plot", "Tripcolor_Plot_1.png"))), size=(110, 110))
b13_1 = ctk.CTkButton(frame, image=tripcolor_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Tripcolor Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command= tripcolor_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b13_1.grid(column=1, padx=1, row=12, pady=1)

# Triplot Plot btn
triplot_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Triplot_Plot", "Triplot_Plot_1.png"))), size=(110, 110))
b14_1 = ctk.CTkButton(frame, image=triplot_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Triplot Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command= triplot_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b14_1.grid(column=2, padx=1, row=12)

# Hexbin Plot btn
hexbin_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Hexbin_Plot", "Hexbin_Plot_1.png"))), size=(110, 110))
b15_1 = ctk.CTkButton(frame, image=hexbin_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Hexbin Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command=hexbin_plot_counter , fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b15_1.grid(column=3, padx=1, row=12)

# Barbs Plot btn
barbs_plot_img = ctk.CTkImage(light_image=Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plot_LAB_2D", "Barbs_Plot", "Barbs_Plot_1.png"))), size=(110, 110))
b16_1 = ctk.CTkButton(frame, image=barbs_plot_img, border_width=1.5, border_color='lightgray', compound="top", text="Barbs Plot", font=ctk.CTkFont(weight="bold", size=12, family="Times"), command=barbs_plot_counter, fg_color="white", text_color="black", hover_color="white", corner_radius=30)
b16_1.grid(column=4, padx=1, row=12)



#______________________________________________________________________________________________________________________

def PrevPage():
  frame.pack_forget()
  frame_1.pack(fill = "both" , expand = True)
  frame_1.configure( width= w_frame_1 , height = h_frame_1 , border = 0)

#_______________________________________________________________________________________________________________________

def NextPage():
  frame_1.pack_forget()
  frame.pack(fill = "both" , expand = True)
  frame.configure( width= w_frame , height = h_frame , border = 0)
  

slide_arrow_button = tk.Button(frame_1 , text = "\u2192" , border=0 , bg = "#D8E7EF", fg = "black" , activebackground="#D8E7EF" , activeforeground="yellow" , command = NextPage )
slide_arrow_button['font'] = font.Font(family="Times" , size = 28 , weight="bold")
slide_arrow_button.grid(column = 6 , row = 6)


tip = Tooltip(slide_arrow_button , text="Slide to Page 2" )


slide_arrow_button_1 = tk.Button(frame , text = "\u2190" , border=0 , bg = "#6da897", fg = "black" , activebackground="#6da897" , activeforeground="yellow" , command=PrevPage )
slide_arrow_button_1['font'] = font.Font(family="Times" , size = 28 , weight="bold")
slide_arrow_button_1.grid(column = 0 , row = 6)



tip_1 = Tooltip(slide_arrow_button_1 , text = "Slide to Page 1")


# Barbs Plot

#_______________________________________________________________________________________________________________________


main_window.config(bg = "#9fb49f" , menu = menubar )
frame.configure(width = w_frame , height = h_frame , border=0 )
frame_1.configure( width= w_frame_1 , height = h_frame_1 , border = 0)

# #9fb49f
# #6da897
#
frame.mainloop()
frame_1.mainloop()
main_window.mainloop()