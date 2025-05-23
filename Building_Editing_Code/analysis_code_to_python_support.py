#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.4
#  in conjunction with Tcl version 8.6
#    Jul 01, 2022 05:08:24 PM EEST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import Building_Editing_Code.analysis_code_to_python as analysis_code_to_python

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = analysis_code_to_python.Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    analysis_code_to_python.start_up()