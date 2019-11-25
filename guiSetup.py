import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import regexModule
import pyperclip
import time

class gui(tk.Frame):
    #Initiates the GUI
    def __init__(self, master=None):
        #Sets the master of the frame as the one used to create the object
        super().__init__(master)
        self.master = master
        #Packs it into the master
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #Destroys all the widgets in the object
        for widget in self.winfo_children():
            widget.destroy()
        #This is for the start up menu, puts it in a grid arrayment
        self.menu0 = tk.Button(self, text = "Enter Regex", command=self.menu0, bg="grey", fg="blue")
        self.menu0.grid(row=0, sticky="ew")
        self.menu1 = tk.Button(self, text = "More Clipboard Space", command=self.menu1, bg="grey", fg="blue")
        self.menu1.grid(row=1, sticky="ew")
        self.menu2 = tk.Button(self, text = "Save all your clipboards to a file", command=self.menu2, bg="grey", fg="blue")
        self.menu2.grid(row=2, sticky="ew")
        self.menu3 = tk.Button(self, text = "Load your clipboards", command=self.menu3, bg="grey", fg="blue")
        self.menu3.grid(row=3, sticky="ew")
        self.quit = tk.Button(self, text = "Quit!", command = self.master.destroy, bg="black", fg="red")
        self.quit.grid(row=4,sticky="ew")

    def menu0(self):
        print("This will find all emails and phone numbers in the text in your clipboard")
        for widget in self.winfo_children():
            widget.destroy()
        self.copyToClip = tk.Label(self, text = "Do you want to copy the result to the clipboard?")
        self.copyToClip.grid(row=0, columnspan=2)
        #These buttons run regex functions
        self.buttonYes = tk.Button(self, text = "Yes", command = self.regexWithCopy)
        self.buttonYes.grid(row=1)
        self.buttonNo = tk.Button(self, text = "No", command = self.regexWithoutCopy)
        self.buttonNo.grid(row=1, column=1)

    def menu1(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.enterName = tk.Label(self, text = "Enter a name for your clipboard")
        self.enterName.grid(row=0, columnspan=3)
        self.nameInput = tk.Entry(self)
        self.nameInput.grid(row=1, columnspan=2)
        self.nameButton = tk.Button(self, text = "Send Input", command=self.addToDict)
        self.nameButton.grid(row=1, column = 2)
        self.enterKey = tk.Label(self, text = "Enter a key to copy to your clipboard")
        self.enterKey.grid(row=2, columnspan=3)
        self.keyInput = tk.Entry(self)
        self.keyInput.grid(row=3, columnspan=2)
        self.keyButton = tk.Button(self, text = "Send Input", command=self.copyFromDict)
        self.keyButton.grid(row=3, column=2)
        self.goBack = tk.Button(text = "Back to menu?", command=self.restart)
        self.goBack.pack(side="bottom")
        
        #This adds a label for each key in the clipboardDict, to help the user remember what they'd entered into it
        self.rowNum = 4
        for key in clipboardDict:
            keyLabel = tk.Label(self, text = key)
            keyLabel.grid(row=self.rowNum)
            self.rowNum += 1

    def menu2(self):

        filename = filedialog.askopenfilename(filetypes = (("Text Files", "*.txt"),
                                                          ("All Files", "*.*")))
        if filename:
            try:
                f = open(filename, "w+")
                for key in clipboardDict:
                    #The [KEY] and [SEPARATOR] are an attempt to differentiate them for when I need them back
                    f.write("\n[KEY]" + key + ":\n[SEPARATOR]" + clipboardDict[key] + "\n")
                f.close()   
            except Exception as e:
                messagebox.showerror("Open source file", "Failed to read file\n'%s'" %filename)
                print(e)

    def menu3(self):
        messagebox.showwarning("Incomplete", "This is incomplete and doesn't work as intended")
        for widget in self.winfo_children():
            widget.destroy()
        
        self.CWD = tk.StringVar()
        self.CWD.set(os.getcwd())
        self.adrLabel = tk.Label(self, text = "Enter the file address of the clipboard")
        self.adrLabel.grid(row=0, columnspan=3)
        self.enterAdr = tk.Entry(self, textvariable=self.CWD)
        self.enterAdr.grid(row=1, columnspan=2)
        self.getAdr = tk.Button(self, text="Enter", command=self.getAdrFromEntry)
        self.getAdr.grid(row=1, column=2)
        self.browse = tk.Button(self, text="Browse", command=self.askForAdr)
        self.browse.grid(row=2)

    def regexWithCopy(self):
        for widget in self.winfo_children():
            widget.destroy()
        results = regexModule.regex(True)
        iterationNo = 0
        for text in results:
            self.label = tk.Label(self, text=text)
            self.label.grid(row=iterationNo)
            iterationNo += 1
        self.goBack = tk.Button(text = "Back to menu?", command=self.restart)
        self.goBack.pack()

    def regexWithoutCopy(self):
        for widget in self.winfo_children():
            widget.destroy()
        results = regexModule.regex(False)
        iterationNo = 0
        for text in results:
            self.label = tk.Label(self, text=text)
            self.label.grid(row=iterationNo)
            iterationNo += 1
        self.goBack = tk.Button(text = "Back to menu?", command=self.restart)
        self.goBack.pack()

    def addToDict(self): 
        clipboardDict[self.nameInput.get()] = pyperclip.paste()
        label = tk.Label(self, text=self.nameInput.get())
        label.grid(row=self.rowNum)
        self.rowNum += 1
        self.nameInput.delete(0, tk.END)

    def copyFromDict(self): 
        pyperclip.copy(clipboardDict[self.keyInput.get()])
        self.keyInput.delete(0, tk.END)

    def askForAdr(self):
        self.CWD.set(filedialog.askopenfilename(filetypes = (("Text Files", "*.txt"), ("All Files", "*.*"))))

    def getAdrFromEntry(self):
        self.filename = self.enterAdr.get()
        messagebox.showinfo("Interesting Title", "This is to say that something happened!")
        self.setClipboard()

    def setClipboard(self):
            try:
                f = open(self.filename, "r")
                file = f.read()
                isKey = True
                key = "Error"
                for value in file.split("[KEY]"):
                    for item in value.split("[SEPARATOR]"):
                        if isKey:
                            key = item
                            isKey = False
                        else:
                            clipboardDict[key] = item
                            isKey = True
                messagebox.showinfo("Success!", "Successfully loaded your clipboard!")
                for key in clipboardDict:
                    print(key + ": " + clipboardDict[key])
            except Exception as e:
                messagebox.showerror("Open source file", "Failed to read file\n'%s'" %self.filename)
                print(e)
            self.restart()
    def restart(self):
        self.destroy()
        self.goBack.destroy()
        start()

root = tk.Tk()

clipboardDict = {}

def start():
    gui(root)
    root.mainloop()