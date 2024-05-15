# JotPad - Text Editor Application using tkinter

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, VERTICAL, RIDGE, RIGHT, BOTTOM, Y, X, BOTH, END
from tkinter.ttk import Combobox
import ttkbootstrap as ttk
from ctypes import windll
import os

window = ttk.Window()
windll.shcore.SetProcessDpiAwareness(1)
window.iconbitmap("icon.ico")
window.geometry("600x700")


#scroll bar
scrollx = tk.Scrollbar(window, orient=HORIZONTAL, activerelief=RIDGE)
scrolly = tk.Scrollbar(window, orient=VERTICAL, activerelief=RIDGE)
scrolly.pack(side=RIGHT, fill=Y)
scrollx.pack(side=BOTTOM, fill=X)


#text box
txt = tk.Text(window, font="consolas 16", wrap="none", xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
txt.pack(expand=True, fill=BOTH)
txt.focus()
txtwrap = tk.BooleanVar(window)

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
    textarea_val = txt.get(1.0, "end-1c")
    if not textarea_val:
        window.destroy()
    else:
        msg = "Do you really want to close JotPad?"
        # FIXME
        val = messagebox.askyesno("Close JotPad", msg)
        if val:
            window.destroy()


#FILE MENU OPTIONS

def confirmOpen():
    msg = "Do you really wish to open another file? \nYou will lose all the current content, unless already saved."
    content = txt.get(1.0, "end-1c")
    if content:
        # FIXME
        x = messagebox.askyesno("File Warning", msg)
        if x:
            return True
        else:
            return False
    else:
        return True


def newfile(*args):
    if confirmOpen():
        txt.delete(0.0, END)
        window.title("Untitled - JotPad")
        global exist
        exist = 0


def openfile(*args):
    try:
        fl = filedialog.askopenfilename(parent=window, title="Open file")
        if fl and confirmOpen():
            txt.delete(0.0, END)
            with open (fl, "r") as f:
                window.title(os.path.basename(fl) + " - JotPad")
                txt.insert(1.0, f.read())
            global working_file
            working_file = fl
            global exist
            exist = 1
    except Exception:
        messagebox.showerror("Open file Error", "Error encountered!")


def saveAs(*args):
    try:
        fl = filedialog.asksaveasfilename(parent=window, title="Save as", defaultextension=".txt",
                               filetypes=[("Text files", ".txt"),
                                          ("All files", ".")])
        if fl:
            content = txt.get(1.0, "end-1c")
            with open(fl, "w") as f:
                window.title(os.path.basename(fl) + " - JotPad")
                f.write(content)
            global working_file
            working_file = fl
            global exist
            exist = 1
    except Exception:
        messagebox.showerror("Save as Error", "Error encountered!")


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
boldchk = tk.BooleanVar()
itlchk = tk.BooleanVar()
ulchk = tk.BooleanVar()
ovschk = tk.BooleanVar()

def fontSet(*args):
    fontBox = tk.Toplevel(window)
    fontBox.transient(window)
    fontBox.rowconfigure(6, weight=1)
    fontBox.columnconfigure(2, weight=1)
    fontBox.geometry("400x220")
    fontBox.iconbitmap("icon.ico")
    fontBox.resizable(0, 0)
    fontBox.title("Font Settings")

    font = tk.Label(fontBox, text="Font:", font="constanta 12 bold").grid(row=0, column=0, padx=15, pady=5)
    fName = tk.StringVar(fontBox)
    fName.set(currFname)
    fontlist = sorted([i for i in tkfont.families() if i[0].isalpha()])
    fonts = Combobox(fontBox, textvariable=fName, values=fontlist, font=("", 10), state="readonly").grid(row=0, column=1)
    
    size = tk.Label(fontBox, text="Size:", font="constanta 12 bold"). grid(row=1, column=0, padx=15, pady=5)
    fSize = tk.StringVar(fontBox)
    fSize.set(currFsize)
    sizelist = [i for i in range(8, 51, 2)]
    sizes = Combobox(fontBox, textvariable=fSize, values = sizelist, font=("", 10), state="readonly").grid(row=1, column=1)
    
    bold = tk.Checkbutton(fontBox, text="Bold", font="constanta 12 bold", variable=boldchk).grid(row=3, column=0, padx=15)
    itl = tk.Checkbutton(fontBox, text="Italic", font="constanta 12 italic", variable=itlchk).grid(row=3, column=1)
    ul = tk.Checkbutton(fontBox, text="Underline", font="constanta 12 underline", variable=ulchk).grid(row=3, column=2)
    ovs = tk.Checkbutton(fontBox, text="Overstrike", font="constanta 12 overstrike", variable=ovschk).grid(row=4, column=1, padx=15)

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
        

    tk.Button(fontBox, text="OK", width=10, background="lightgreen", font="constanta 10 bold", command=fsetok).grid(row=5, column=0, padx=12)
    tk.Button(fontBox, text="Cancel", width=10, background="red", font="constanta 10 bold", command=fsetcancel).grid(row=5, column=1)
    tk.Button(fontBox, text="Apply", width=10, background="lightblue", font="constanta 10 bold", command=fsetapply).grid(row=5, column=2)
    tk.Button(fontBox, text="Reset to Default", width=16, background="lightgrey", font="constanta 10 bold", command=freset).grid(row=6, column=1)
    fontBox.focus()
    





def txtwrapSet(*args):
    val = txtwrap.get()
    if val:
        txt.config(wrap="word")
        scrollx.pack_forget()
    else:
        txt.pack_forget()
        txt.config(wrap="none")
        # FIXME
        scrollx.pack(side=BOTTOM, fill=X)
        txt.pack(expand=True, fill=BOTH)


#HELP MENU OPTIONS

def about(*args):
    aboutbox = tk.Toplevel(window)
    aboutbox.transient(window)
    aboutbox.title("About JotPad")
    aboutbox.geometry("250x200")
    aboutbox.resizable(0, 0)
    aboutbox.iconbitmap("icon.ico")
    msg = "JotPad \nVersion: 1.0 \n\nDeveloped by: \nAnurag Chattopadhyay"
    tk.Label(aboutbox, text=msg, font=("", "11"), justify="left", pady=10).pack()
    aboutbox.focus()

    def okpress():
        aboutbox.destroy()
        aboutbox.update()

    tk.Button(aboutbox, text="OK", font=("", "10", "bold"), width=10, command=okpress).pack()
    


#menubar
menubar = tk.Menu(window)

#file menu
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="New File", font=("", 10), command=newfile, accelerator="Ctrl+N")
file.add_command(label="Open File", font=("", 10), command=openfile, accelerator="Ctrl+O")
file.add_command(label="Save", font=("", 10), command=save, accelerator="Ctrl+S")
file.add_command(label="Save as", font=("", 10), command=saveAs, accelerator="Ctrl+Shift+S")
file.add_separator()
file.add_command(label="Close", font=("", 10), command=confirmExit)


#edit menu
edit = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Select All", font=("", 10), command=selectAll, accelerator="Ctrl+A")
edit.add_command(label="Cut", font=("", 10), command=cut, accelerator="Ctrl+X")
edit.add_command(label="Copy", font=("", 10), command=copy, accelerator="Ctrl+C")
edit.add_command(label="Paste", font=("", 10), command=paste, accelerator="Ctrl+V")



#view menu
view = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=view)
view.add_command(label="Font Settings", font=("", 10), command=fontSet)
view.add_separator()
view.add_checkbutton(label="Text Wrap", variable=txtwrap, command=txtwrapSet)

#help menu
help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help)
help.add_command(label="About", font=("", 10), command=about)




#config
newfile()
scrollx.config(command=txt.xview)
scrolly.config(command=txt.yview)
window.config(menu=menubar)
window.bind('<Control-n>', newfile)
window.bind('<Control-o>', openfile)
window.bind('<Control-S>', saveAs)
window.bind('<Control-s>', save)


window.protocol("WM_DELETE_WINDOW", confirmExit)
window.mainloop()


