import tkinter as tk                    
from tkinter import ttk
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Tab 1')
tabControl.add(tab2, text ='Tab 2')
tabControl.pack(expand = 1, fill ="both")
__thisTextArea=[]
__thisScrollBar=[]
__thisTextArea.append(Text(tab1, undo=True))
__thisTextArea.append(Text(tab2, undo=True))
__thisTextArea[tabControl.index(tabControl.select())].grid(sticky=N + E + S + W)
__thisScrollBar.append(Scrollbar(__thisTextArea[tabControl.index(tabControl.select())]))
def onclick(event):
    __thisTextArea[tabControl.index(tabControl.select())].grid(sticky=N + E + S + W)
    __thisScrollBar.append(Scrollbar(__thisTextArea[tabControl.index(tabControl.select())]))

tabControl.bind("<<NotebookTabChanged>>",onclick)
root.mainloop()