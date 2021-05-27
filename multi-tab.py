import tkinter
import os	
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:  
    __root = Tk()

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = []
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    tabControl = ttk.Notebook(__root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text ='Tab 1')
    tabControl.add(tab2, text ='Tab 2')
    tabControl.pack(fill=BOTH,expand=1) 
    tab1.grid_rowconfigure(0,weight=1)
    tab1.grid_columnconfigure(0,weight=1)
    tab2.grid_rowconfigure(0,weight=1)
    tab2.grid_columnconfigure(0,weight=1)
    # To add scrollbar
    __thisScrollBar = []
    __file = None
    __thisTextArea.append(Text(tab1, undo=True))
    __thisTextArea.append(Text(tab2, undo=True))
    __thisScrollBar.append(Scrollbar(tab1))
    def __init__(self,**kwargs):

        # Set icon
        try:
                self.__root.wm_iconbitmap("Notepad.ico")
        except:
                pass

        # Set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Untitled - Notepad")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-alling
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        
        # For right-allign
        top = (screenHeight / 2) - (self.__thisHeight /2)
        
        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                            self.__thisHeight,
                                            left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        # Add controls (widget)
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].grid(sticky = N + E + S + W)
        
        # To open new file
        self.__thisFileMenu.add_command(label="New",
                                        command=self.__newFile)	
        
        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open",
                                        command=self.__openFile)
        
        # To save current file
        self.__thisFileMenu.add_command(label="Save",
                                        command=self.__saveFile)	
        
        # To save as current file
        self.__thisFileMenu.add_command(label="Save as",
                                        command=self.__saveasFile)

        # To create a line in the dialog		
        self.__thisFileMenu.add_separator()										
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
                                    menu=self.__thisFileMenu)	
        
        # To give a feautre of undo
        self.__thisEditMenu.add_command(label="Undo",command=self.__thisTextArea[self.tabControl.index(self.tabControl.select())].edit_undo)
        
        # To give a feautre of redo
        self.__thisEditMenu.add_command(label="Redo",command=self.__thisTextArea[self.tabControl.index(self.tabControl.select())].edit_redo)
        
        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut",
                                        command=self.__cut)			

        # to give a feature of copy	
        self.__thisEditMenu.add_command(label="Copy",
                                        command=self.__copy)		
        
        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste",
                                        command=self.__paste)		
        
        # To give a feature to select all
        self.__thisEditMenu.add_command(label="Select all",command=self.__selectall)
        
        self.__thisEditMenu.add_separator()
        
        # To give a feautre of Reset
        self.__thisEditMenu.add_command(label="Reset",command=self.__reset)
        
        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit",
                                    menu=self.__thisEditMenu)	
        
        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About Notepad",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",
                                    menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].grid(row=0,column=2,sticky=N+E+S+W)				
        
        # Scrollbar will adjust automatically according to the content		
        self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].config(command=self.__thisTextArea[self.tabControl.index(self.tabControl.select())].yview)	
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].config(yscrollcommand=self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].set)
        
        
    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __showAbout(self):
        showinfo("Notepad","Mrinal Verma")

    def __openFile(self):
        
        self.__file = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files","*.*"),
                                        ("Text Documents","*.txt")])

        if self.__file == "":
            
            # no file to open
            self.__file = None
        else:
            
            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea[self.tabControl.index(self.tabControl.select())].delete(1.0,END)

            file = open(self.__file,"r")

            self.__thisTextArea[self.tabControl.index(self.tabControl.select())].insert(1.0,file.read())

            file.close()

        
    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].delete(1.0,END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                
                # Try to save the file
                file = open(self.__file,"w")
                file.write(self.__thisTextArea[self.tabControl.index(self.tabControl.select())].get(1.0,END))
                file.close()
                
                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
                
            
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea[self.tabControl.index(self.tabControl.select())].get(1.0,END))
            file.close()

    def __saveasFile(self):
        self.__file = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea[self.tabControl.index(self.tabControl.select())].get(1.0,END))
            file.close()
        self.__root.title(os.path.basename(self.__file) + " - Notepad")

    def __reset(self):
            count=1.0        
            if self.__file==None:
                self.__thisTextArea[self.tabControl.index(self.tabControl.select())].delete(count,END)
            else:               
                file = open(self.__file,"r")
                for i in file.read():
                    if i=='\n':
                        count+=1
                self.__thisTextArea[self.tabControl.index(self.tabControl.select())].delete(count,END)
                file.close()
        
    def __selectall(self):
            self.__thisTextArea[self.tabControl.index(self.tabControl.select())].tag_add('sel','1.0','end')
    def __cut(self):
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea[self.tabControl.index(self.tabControl.select())].event_generate("<<Paste>>")        

    def onclick(self,event):
        try:
            k=self.__thisScrollBar[self.tabControl.index(self.tabControl.select())]
            print(self.tabControl.index(self.tabControl.select()))

        except:
            self.__thisTextArea[self.tabControl.index(self.tabControl.select())].grid(sticky=N + E + S + W)
            self.__thisScrollBar.append(Scrollbar(self.tab2))
            self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].grid(row=0,column=9,sticky=N+S+E)
            self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].config(command=self.__thisTextArea[self.tabControl.index(self.tabControl.select())].yview)	
            self.__thisTextArea[self.tabControl.index(self.tabControl.select())].config(yscrollcommand=self.__thisScrollBar[self.tabControl.index(self.tabControl.select())].set)    
    def run(self):

            # Run main application
            self.tabControl.bind("<<NotebookTabChanged>>",self.onclick)
            self.__root.mainloop()


# Run main application
notepad = Notepad(width=600,height=400)
notepad.run()

