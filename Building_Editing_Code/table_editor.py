from tkinter import *
from pandastable import Table 


def table_editor():

  root = Toplevel()

  root.geometry('600x400+200+100')
  root.title('FastAlyze Table Editor')
  root.iconbitmap("table_editor.ico")

  class TestApp(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.table = Table(self, showtoolbar=True, showstatusbar=True)
        self.table.show()

  app = TestApp(root)
  app.pack(fill=BOTH, expand=1)

  root.mainloop()