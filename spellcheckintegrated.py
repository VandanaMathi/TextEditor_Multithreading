import tkinter 
import os	
from tkinter.simpledialog import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import threading
from rake_nltk import Rake

#for performance measurement 
import tracemalloc
import pandas as pd
import dask.dataframe as dd
import time

dictionary=set()
appl_closed=0
switch="ON"

def read_dictionary_file():
	global dictionary
	if dictionary:
		return
	
	with open("words.txt", "r") as f:
		contents = f.read()        
	
	dictionary = set(
	word.lower()
	for word in contents.splitlines()
	)

class Notepad:

	__root = Tk()

	# default window width and height
	__thisWidth = 300
	__thisHeight = 300
	__thisTextArea = Text(__root,undo=True)
	__thisMenuBar = Menu(__root)
	__thisFileMenu = Menu(__thisMenuBar, tearoff=0)
	__thisEditMenu = Menu(__thisMenuBar, tearoff=0)
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
	__thisWordMenu = Menu(__thisMenuBar, tearoff=0)
	status = StringVar()
	
	
	# To add scrollbar
	__thisScrollBar = Scrollbar(__thisTextArea)	
	__file = None

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
	
		# Declaring Status variable
    	
		self.statusbar = Label(master = self.__thisTextArea,textvariable=self.status,font=("consolas",8),state="active",justify='left') 
		self.statusbar.pack(side = BOTTOM,fill=X )
		
		# To make the textarea auto resizable
		self.__root.grid_rowconfigure(0, weight=1) 
		self.__root.grid_columnconfigure(0, weight=1)

		# Add controls (widget)
		self.__thisTextArea.grid(sticky = N + E + S + W)
		
		# To open new file
		self.__thisFileMenu.add_command(label="New", accelerator="Ctrl+N",command=self.__newFile)	
		
		# To open a already existing file
		self.__thisFileMenu.add_command(label="Open",accelerator="Ctrl+O",
										command=self.__openFile)
		
		# To save current file
		self.__thisFileMenu.add_command(label="Save",accelerator="Ctrl+S",
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
		self.__thisEditMenu.add_command(label="Undo",command=self.__thisTextArea.edit_undo,accelerator="Ctrl+Z")
		
		# To give a feautre of redo
		self.__thisEditMenu.add_command(label="Redo",command=self.__thisTextArea.edit_redo)
		
		# To give a feature of cut
		self.__thisEditMenu.add_command(label="Cut", accelerator="Ctrl+X",
										command=self.__cut)			
	
		# to give a feature of copy	
		self.__thisEditMenu.add_command(label="Copy",accelerator="Ctrl+C",
										command=self.__copy)		
		
		# To give a feature of paste
		self.__thisEditMenu.add_command(label="Paste",accelerator="Ctrl+V",
										command=self.__paste)		
		
		# To give a feature to select all
		self.__thisEditMenu.add_command(label="Select all",command=self.__selectall)
		#self.__thisEditMenu.add_command(label="Find",accelerator="Ctrl+F",command=self.find)
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

		self.__thisScrollBar.pack(side=RIGHT,fill=Y)	

		#To create a word count feature in menu Bar 
		self.__thisMenuBar.add_cascade(label="Text analysis",menu=self.__thisWordMenu)
		self.__thisWordMenu.add_cascade(label= "Total Words",accelerator= "Ctrl+W", command = self.__wordCount)
		self.__thisWordMenu.add_cascade(label= "Keywords", accelerator= "Ctrl+K",command = self.__keyWord)
		self.__thisWordMenu.add_command(label="Spell check",accelerator="Ctrl+P",command=self.is_spelled_correctly)
		
		# Scrollbar will adjust automatically according to the content	
		self.__thisScrollBar.config(command=self.__thisTextArea.yview)	
		self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

		#binding all shortcuts 
		#edit menu
		self.__root.bind_all("<Control-C>", self.__copy)
		self.__root.bind_all("<Control-V>", self.__paste)
		self.__root.bind_all("<Control-X>", self.__cut)
		self.__root.bind_all("<Control-P>", self.is_spelled_correctly)
		#__root.bind_all("<Control-F>", self.find)
		self.__root.bind_all("<Control-Z>", self.__thisTextArea.edit_undo)

		#FileMenu 
		self.__root.bind_all("<Control-S>", self.__saveFile)
		self.__root.bind_all("<Control-N>", self.__newFile)
		self.__root.bind_all("<Control-O>", self.__openFile)

		#Word menu

		self.__root.bind_all("<Control-P>", self.is_spelled_correctly)
		self.__root.bind_all("<Control-W>", self.__wordCount)
		self.__root.bind_all("<Control-K>", self.__keyWord)
		
		threading.Thread(target=self.is_spelled_correctly).start()
		threading.Thread(target=self.__wordCount).start()
		
		
		
		
	def __quitApplication(self):
		if tkinter.messagebox.askokcancel("Quit","Do you want to Quit?"):
			threading.Thread(target=self.is_spelled_correctly).join()
			threading.Thread(target=self.__wordCount).join()
			appl_closed=1
			tracing_mem()

			self.__root.destroy()
		else:
			return
		# exit()

	def __showAbout(self):
		showinfo("Notepad",'''Easy to use notepad with spellchecker, word count and keywords display\n 
		Ctrl+P - spell checker\n
		Ctrl+W - total word count\n
		Ctrl+K - Keywords display''')

	def __openFile(self):
		global switch
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
			self.__thisTextArea.delete(1.0,END)

			file = open(self.__file,"r")

			self.__thisTextArea.insert(1.0,file.read())

			file.close()
			switch="ON"
		
	def __newFile(self):
		global switch
		self.__root.title("Untitled - Notepad")
		self.__file = None
		self.__thisTextArea.delete(1.0,END)
		switch="ON"

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
				file.write(self.__thisTextArea.get(1.0,END))
				file.close()
				
				# Change the window title
				self.__root.title(os.path.basename(self.__file) + " - Notepad")
				
			
		else:
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()

	def __saveasFile(self):
		self.__file = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		if self.__file == "":
			self.__file = None
		else:
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()
		self.__root.title(os.path.basename(self.__file) + " - Notepad")
    
	def __reset(self):
			count=1.0        
			if self.__file==None:
				self.__thisTextArea.delete(count,END)
			else:               
				file = open(self.__file,"r")
				for i in file.read():
					if i=='\n':
						count+=1
				self.__thisTextArea.delete(count,END)
				file.close()
		
	def __selectall(self):
			self.__thisTextArea.tag_add('sel','1.0','end')
	def __cut(self):
		self.__thisTextArea.event_generate("<<Cut>>")

	def __copy(self):
		self.__thisTextArea.event_generate("<<Copy>>")

	def __paste(self):
		self.__thisTextArea.event_generate("<<Paste>>")                   
		            
	def __StopStartspellcheck(self):
		global switch
		if switch=="ON":
			switch="OFF"
		elif switch=="OFF":
			switch="ON"
		return
		
        
	def is_spelled_correctly(self):
		global switch
		self.__thisTextArea.tag_remove("Error","1.0","end") 
		if switch=="ON":
			#print("In is spelled correctly")          
			text_spellcheck = self.__thisTextArea.get(1.0,END)
			list_lines=text_spellcheck.split("\n")
			for line in list_lines:
				list_word=line.split(" ")
				count=0
				for word in list_word:
					word_cpy=word                    
					read_dictionary_file()
					if ',' in word:
						word_cpy=word.replace(',','')
					if '.' in word:
						word_cpy=word.replace('.','')
					if '?' in word:
						word_cpy=word.replace('?','')
					if '!' in word:
						word_cpy=word.replace('!','')
					check=word_cpy.lower() in dictionary                    
					if check==False:
						linepos=list_lines.index(line)+1
						wordpos=list_word.index(word)
						#print(linepos,wordpos,count,len(word))
						start_decimal_index=count+wordpos
						end_decimal_index=count+wordpos+len(word)
						start=str(linepos)+'.'+str(start_decimal_index)
						end=str(linepos)+'.'+str(end_decimal_index)
						#print(start,end)
						self.__thisTextArea.tag_add("Error",str(start),str(end))
						self.__thisTextArea.tag_config("Error",background="yellow",foreground="red")
					count+=len(word)
		self.__root.after(1,self.is_spelled_correctly)
		
	
	#method to find the number of words in the file 
	def __wordCount(self): 
		self.__thisTextArea.tag_remove("Error","1.0","end")
		if switch=="ON":
			
			#word count is found 
			data = self.__thisTextArea.get(1.0,END)
			words = data.split()

			#no of words stored in noWords 
			noWords = len(words)
			self.status.set(str(noWords)+ " words")
			self.__root.after(10,self.__wordCount)

	#method to find the keywords in the text 
	def __keyWord(self):
		self.__thisTextArea.tag_remove("Error","1.0","end")
		data = self.__thisTextArea.get(1.0,END)
		#preprocessing the data to remove blank spaces 
		l = data.split(" ")
		x= list()
		for i in l:
			if i!='': x.append(i)
	
		data = " ".join(x)
		r = Rake()
		#extract the keywords 
		r.extract_keywords_from_text(data)
		#get the top 3 keywords 
		keywordsList = r.get_ranked_phrases()[:3]
		#Converting list to string for output 
		#print(keywordsList)
		keywordsStr = str(keywordsList)[1:-2]
		tkinter.messagebox.showinfo("Keywords", keywordsStr) 
	
	def run(self):
		# Run main application
		self.__root.mainloop()

'''	def find(self, *args):
		self.text.tag_remove('found', '1.0', END)
        target = askstring('Find','Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground='white', background='blue')

	
	'''
	
 


def tracing_start():
    tracemalloc.stop()
    print("nTracing Status : ", tracemalloc.is_tracing())
    tracemalloc.start()
    print("Tracing Status : ", tracemalloc.is_tracing())
def tracing_mem():
    first_size, first_peak = tracemalloc.get_traced_memory()
    peak = first_peak/(1024*1024)
    print("Peak Size in MB - ", peak)

# Run main application

notepad = Notepad(width=600,height=400)
tracing_start()
start = time.time()
notepad.run()
end = time.time()
print("time elapsed {} milli seconds".format((end-start)*1000))
tracing_mem()
