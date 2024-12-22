import tabula as tb
import pandas as pd
import os
from html2excel import ExcelParser
import json


def convert_csv(filepath):#VERIFIED
  df_new = pd.read_csv(filepath)
  savedfilepath = filepath.replace("csv" , "xlsx")
  GFG = pd.ExcelWriter(savedfilepath)
  df_new.to_excel(GFG, index=False)
  GFG.save()

def convert_pdf(filepath):#VERIFIED
  df = pd.DataFrame()
  x = tb.read_pdf(filepath , pages = "all" , multiple_tables=True)
  savedfilepath = filepath.replace("pdf" , "xlsx")
  df = pd.DataFrame()
  for i in x:
    df_table = pd.DataFrame(i)
    df = df.append(df_table)
  df.to_excel(savedfilepath , index=False)

def convert_text(filepath):#VERIFIED
  df = pd.read_csv(filepath)# red the text file
  savedfilepath = filepath.replace("txt" , "csv")#configuring new path for the upcoming csv file
  df_2 = df.to_csv(savedfilepath , index = False)#converting text into csv
  df_2 = pd.read_csv(savedfilepath)#reading the csv file
  savedfilepath = savedfilepath.replace("csv" , "xlsx")#configuring new path for the upcoming xlsx file
  df_2.to_excel(savedfilepath , index=False)#finally save the excel file
  savedfilepath = savedfilepath.replace("xlsx" , "csv")
  os.remove(savedfilepath)

def convert_xls(filepath):# VERIFIED
  df = pd.read_excel(filepath)
  savedfilepath = filepath.replace("xls" , "xlsx")
  df.to_excel(savedfilepath , index = False)

def convert_html(filepath):#VERIFIED
  if filepath.endswith("html") :
   parser_1 = ExcelParser(filepath)
   savedfilepath = filepath.replace("html" , "xlsx")
   parser_1.to_excel(savedfilepath)
  if filepath.endswith("htm"):
   parser_1 = ExcelParser(filepath)
   savedfilepath = filepath.replace("htm" , "xlsx")
   parser_1.to_excel(savedfilepath)

def convert_odf(filepath):#VERIFIED
  df = pd.read_excel(filepath , engine="odf")
  savedfilepath = filepath.replace("ods" , "xlsx")
  df.to_excel(savedfilepath , index = False)

def convert_xml(filepath):#VERIFIED
  df = pd.read_xml(filepath)
  savedfilepath = filepath.replace("xml" , "xlsx")
  df.to_excel(savedfilepath , index = False)

def convert_json(filepath):#VERIFIED
  with open(filepath) as json_file:
    data = json.load(json_file)
  df = pd.json_normalize(data)
  savedfilepath = filepath.replace("json" , "xlsx")
  df.to_excel(savedfilepath , index = False)


# This is for the next update ... Hope so :))))
'''
def convert_orc(filepath):
  df = pd.read_orc(filepath)
  savedfilepath = filepath.replace("orc" , "xlsx")
  df.to_excel(savedfilepath , index = False)

def convert_stata(filepath):
  df = pd.read_stata(filepath)
  savedfilepath = filepath.replace("dta" , "xlsx")
  df.to_excel(savedfilepath , index=False)

def convert_sas(filepath):
  df = pd.read_sas(filepath)
  if filepath.endswith("xpt"):
    savedfilepath = filepath.replace("xpt" , "xlsx")
    df.to_excel(savedfilepath , index=False)
  if filepath.endswith("sas7bdat"):
    savedfilepath = filepath.replace("sas7bdat" , "xlsx")
    df.to_excel(savedfilepath , index=False)

def convert_spss(filepath):
  df = pd.read_spss(filepath)
  if filepath.endswith("sav"):
    savedfilepath = filepath.replace("sav" , "xlsx")
    df.to_excel(savedfilepath , index=False)
  if filepath.endswith("zsav"):
    savedfilepath = filepath.replace("zsav" , "xlsx")
    df.to_excel(savedfilepath , index=False)

def convert_pkl(filepath):
  df = pd.read_pickle(filepath)
  if filepath.endswith("pkl"):
    savedfilepath = filepath.replace("pkl" , "xlsx")
    df.to_excel(savedfilepath , index=False)
'''