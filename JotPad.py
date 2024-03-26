# JotPad - Text Editor Application using tkinter

from tkinter import *
from tkinter.ttk import Combobox
from tkinter.font import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from ctypes import windll
import os

root = Tk()
windll.shcore.SetProcessDpiAwareness(1)
root.iconbitmap("icon.ico")
root.geometry("600x700")


#scroll bar
scrollx = Scrollbar(root, orient=HORIZONTAL, activerelief=RIDGE)
scrolly = Scrollbar(root, orient=VERTICAL, activerelief=RIDGE)
scrolly.pack(side=RIGHT, fill=Y)
scrollx.pack(side=BOTTOM, fill=X)


#text box
txt = Text(root, font="consolas 16", wrap="none", xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
txt.pack(expand=True, fill=BOTH)
txt.focus()
txtwrap = BooleanVar(root)

txtwrap.set(False)

#saved status flag
saved=0


#existence status flag
exist = 0
working_file = ""

#change tracker
def changed(*args):
    pass


#closing dialog box
def confirmExit(*args):
    msg = "Do you really want to close JotPad?"
    val = askyesno("Close JotPad", msg)
    if val:
        root.destroy()


#FILE MENU OPTIONS

def confirmOpen():
    msg = "Do you really wish to open another file? \nYou will lose all the current content, unless already saved."
    content = txt.get(1.0, "end-1c")
    if content:
        x = askyesno("File Warning", msg)
        if x:
            return True
        else:
            return False
    else:
        return True


def newfile(*args):
    if confirmOpen():
        txt.delete(0.0, END)
        root.title("Untitled - JotPad")
        global exist
        exist = 0


def openfile(*args):
    try:
        fl = askopenfilename(parent=root, title="Open file")
        if fl and confirmOpen():
            txt.delete(0.0, END)
            with open (fl, "r") as f:
                root.title(os.path.basename(fl) + " - JotPad")
                txt.insert(1.0, f.read())
            global working_file
            working_file = fl
            global exist
            exist = 1
    except Exception:
        showerror("Open file Error", "Error encountered!")


def saveAs(*args):
    try:
        fl = asksaveasfilename(parent=root, title="Save as", defaultextension=".txt",
                               filetypes=[("Text files", ".txt"),
                                          ("All files", ".")])
        if fl:
            content = txt.get(1.0, "end-1c")
            with open(fl, "w") as f:
                root.title(os.path.basename(fl) + " - JotPad")
                f.write(content)
            global working_file
            working_file = fl
            global exist
            exist = 1
    except Exception:
        showerror("Save as Error", "Error encountered!")


def save(*args):
    global exist
    if exist == 0:
        saveAs()
    else:
        content = txt.get(1.0, "end-1c")
        with open(working_file, "w") as f:
            f.write(content)



#EDIT MENU OPTIONS

def selectAll(*args):
    txt.focus_get().event_generate("<Control-a>")

def cut(*args):
    txt.focus_get().event_generate("<<Cut>>")

def copy(*args):
    txt.focus_get().event_generate("<<Copy>>")

def paste(*args):
    txt.focus_get().event_generate("<<Paste>>")



#VIEW MENU OPTIONS

currFname = "Consolas"
currFsize = "16"
boldchk = BooleanVar()
itlchk = BooleanVar()
ulchk = BooleanVar()
ovschk = BooleanVar()

def fontSet(*args):
    fontBox = Toplevel(root)
    fontBox.transient(root)
    fontBox.rowconfigure(6, weight=1)
    fontBox.columnconfigure(2, weight=1)
    fontBox.geometry("400x220")
    fontBox.iconbitmap("icon.ico")
    fontBox.resizable(0, 0)
    fontBox.title("Font Settings")

    font = Label(fontBox, text="Font:", font="constanta 12 bold").grid(row=0, column=0, padx=15, pady=5)
    fName = StringVar(fontBox)
    fName.set(currFname)
    fontlist = sorted([i for i in families() if i[0].isalpha()])
    fonts = Combobox(fontBox, textvariable=fName, values=fontlist, font=("", 10), state="readonly").grid(row=0, column=1)
    
    size = Label(fontBox, text="Size:", font="constanta 12 bold"). grid(row=1, column=0, padx=15, pady=5)
    fSize = StringVar(fontBox)
    fSize.set(currFsize)
    sizelist = [i for i in range(8, 51, 2)]
    sizes = Combobox(fontBox, textvariable=fSize, values = sizelist, font=("", 10), state="readonly").grid(row=1, column=1)
    
    bold = Checkbutton(fontBox, text="Bold", font="constanta 12 bold", variable=boldchk).grid(row=3, column=0, padx=15)
    itl = Checkbutton(fontBox, text="Italic", font="constanta 12 italic", variable=itlchk).grid(row=3, column=1)
    ul = Checkbutton(fontBox, text="Underline", font="constanta 12 underline", variable=ulchk).grid(row=3, column=2)
    ovs = Checkbutton(fontBox, text="Overstrike", font="constanta 12 overstrike", variable=ovschk).grid(row=4, column=1, padx=15)

    def styleset():
        global boldval, itlval, ulval, ovsval

        if boldchk.get():
            boldval = " bold"
        else:
            boldval = ""

        if itlchk.get():
            itlval = " italic"
        else:
            itlval = ""

        if ulchk.get():
            ulval = " underline"
        else:
            ulval = ""

        if ovschk.get():
            ovsval = " overstrike"
        else:
            ovsval = ""


    def fsetapply():
        global currFname, currFsize
        styleset()
        newfn = fName.get().replace(" ", "")
        newfs = fSize.get()
        boldchk.set(boldchk.get())
        itlchk.set(itlchk.get())
        ulchk.set(ulchk.get())
        ovschk.set(ovschk.get())
        if newfn!="" and newfs!="":
            newfont = str(newfn+" "+newfs+boldval+itlval+ulval+ovsval)
            currFname = fName.get()
            currFsize = fSize.get()
            txt.config(font=newfont)

    
    def fsetok():
        fsetapply()
        fontBox.destroy()
        fontBox.update()


    def fsetcancel():
        fontBox.destroy()
        fontBox.update()


    def freset():
        fName.set("Consolas")
        fSize.set("16")
        boldchk.set(False)
        itlchk.set(False)
        ulchk.set(False)
        ovschk.set(False)
        fsetapply()
        

    Button(fontBox, text="OK", width=10, background="lightgreen", font="constanta 10 bold", command=fsetok).grid(row=5, column=0, padx=12)
    Button(fontBox, text="Cancel", width=10, background="red", font="constanta 10 bold", command=fsetcancel).grid(row=5, column=1)
    Button(fontBox, text="Apply", width=10, background="lightblue", font="constanta 10 bold", command=fsetapply).grid(row=5, column=2)
    Button(fontBox, text="Reset to Default", width=16, background="lightgrey", font="constanta 10 bold", command=freset).grid(row=6, column=1)
    fontBox.focus()
    





def txtwrapSet(*args):
    val = txtwrap.get()
    if val:
        txt.config(wrap="word")
        scrollx.pack_forget()
    else:
        txt.pack_forget()
        txt.config(wrap="none")
        scrollx.pack(side=BOTTOM, fill=X)
        txt.pack(expand=True, fill=BOTH)


#HELP MENU OPTIONS

def about(*args):
    aboutbox = Toplevel(root)
    aboutbox.transient(root)
    aboutbox.title("About JotPad")
    aboutbox.geometry("250x200")
    aboutbox.resizable(0, 0)
    aboutbox.iconbitmap("icon.ico")
    msg = "JotPad \nVersion: 1.0 \n\nDeveloped by: \nAnurag Chattopadhyay"
    Label(aboutbox, text=msg, font=("", "11"), justify="left", pady=10).pack()
    aboutbox.focus()

    def okpress():
        aboutbox.destroy()
        aboutbox.update()

    Button(aboutbox, text="OK", font=("", "10", "bold"), width=10, command=okpress).pack()
    


#menubar
menubar = Menu(root)

#file menu
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="New File", font=("", 10), command=newfile, accelerator="Ctrl+N")
file.add_command(label="Open File", font=("", 10), command=openfile, accelerator="Ctrl+O")
file.add_command(label="Save", font=("", 10), command=save, accelerator="Ctrl+S")
file.add_command(label="Save as", font=("", 10), command=saveAs, accelerator="Ctrl+Shift+S")
file.add_separator()
file.add_command(label="Close", font=("", 10), command=confirmExit)


#edit menu
edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Select All", font=("", 10), command=selectAll, accelerator="Ctrl+A")
edit.add_command(label="Cut", font=("", 10), command=cut, accelerator="Ctrl+X")
edit.add_command(label="Copy", font=("", 10), command=copy, accelerator="Ctrl+C")
edit.add_command(label="Paste", font=("", 10), command=paste, accelerator="Ctrl+V")



#view menu
view = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=view)
view.add_command(label="Font Settings", font=("", 10), command=fontSet)
view.add_separator()
view.add_checkbutton(label="Text Wrap", variable=txtwrap, command=txtwrapSet)

#help menu
help = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help)
help.add_command(label="About", font=("", 10), command=about)




#config
newfile()
scrollx.config(command=txt.xview)
scrolly.config(command=txt.yview)
root.config(menu=menubar)
root.bind('<Control-n>', newfile)
root.bind('<Control-o>', openfile)
root.bind('<Control-S>', saveAs)
root.bind('<Control-s>', save)


root.protocol("WM_DELETE_WINDOW", confirmExit)
root.mainloop()
