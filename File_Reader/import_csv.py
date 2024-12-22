import pandas as pd
from tkinter import filedialog


#______________________________________________________________________________________

df_list_2 = []

df = 0

df_list_scatter_x_csv = []

df_list_scatter_y_csv = []

csv_filepath = 0

counter = 0


def import_csv_file() :

    global df_list_2 , df , csv , csv_filepath , counter
    global df_list_scatter_x_csv , df_list_scatter_y_csv
    
    df_list_2 = []

    df_list_scatter_x_csv = []

    df_list_scatter_y_csv = []

    csv_filepath = filedialog.askopenfilename(initialdir = "/" , title = "Select a File" , filetypes = (("CSV File" , "*.csv*" ) , ("all files","*.*") ))

    def verify_integer_list(lista):
     if all( isinstance(item , int) for item in lista) or all( isinstance(item , float) for item in lista) or all( isinstance(item , complex) for item in lista) :
      return True
     else:
      return False
    

    df = pd.read_csv(csv_filepath)

    remove_names = []
    columns_names = list(df.head())
    
    for x in columns_names :
             aux = list(df[x])
             if verify_integer_list(aux) == False :
                       remove_names.append(x)

     
    for j in remove_names:
          df.drop(j , inplace=True, axis=1)


    df_list_2 = df[df.columns].to_numpy() 

    if len(list(df.columns)) == 2 :
           df_list_scatter_x_csv = list(df[df.columns[0]])
           df_list_scatter_y_csv = list(df[df.columns[1]])

def return_df2() :
     return df_list_2

def return_df_scatter_x_csv_f():
     return df_list_scatter_x_csv


def return_df_scatter_y_csv_f() :
    return df_list_scatter_y_csv


def return_df_stacked_plot_csv():
     return_stk_plt_csv = []
     for i in range(len(df.columns)) :
       if list(df[df.columns[i]]) :
          return_stk_plt_csv.append(list(df[df.columns[i]]))
     return return_stk_plt_csv


def return_df_stairs_plot_csv():
     r_csv = []
     for i in range(len(df.columns)) :
        if list(df[df.columns[i]]) :
          r_csv.append(list(df[df.columns[i]]))
     return r_csv 

def return_df_angle_spectrum_csv():
     r_csv = []
     for i in range(len(df.columns)) :
       if list(df[df.columns[i]]) :
          r_csv.append(list(df[df.columns[i]]))
     return r_csv 

def return_df_stream_plot_csv():
     r_csv = []
     for i in range(len(df.columns)):
       if list(df[df.columns[i]]) :
          r_csv.append(list(df[df.columns[i]]))
     return r_csv