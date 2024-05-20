# JotPad - Text Editor Application using tkinter

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, VERTICAL, RIDGE, RIGHT, BOTTOM, Y, X, BOTH, END, SOLID, SUNKEN, GROOVE
from tkinter.ttk import Combobox
import pygments.lexers
import ttkbootstrap as ttk
# import customtkinter as ctk # USE CTK LATER
from ctypes import windll
import os
from dark_mode_util import set_dark_title_bar, set_light_title_bar

import pygments

import subprocess
import platform
import CTkMenuBar as ctkmenu
import customtkinter as ctk

# from chlorophyll import CodeView
# from components import CodeView

# from components import language_pairs

from components import CodeView, language_pairs
# from pygments.formatters import TkinterFormatter

# from pygments import highlight

# window = ttk.Window(themename='cyborg')
is_window_min = True

window = ctk.CTk()
ctk.set_appearance_mode("dark")

# window.overrideredirect(True)

ver = 1.1

set_dark_title_bar(window)
# set_dark_menubar(window)

windll.shcore.SetProcessDpiAwareness(1)

try:
    window.iconbitmap(default='icon.ico')
except tk.TclError:
    pass  # Handle the case where the icon file is not found or cannot be set

window.geometry("900x700")
dark_bg = "#212121"
window.config(bg=dark_bg)  

# FIXED, added in codeblock
# #scroll bar
# scrollx = ttk.Scrollbar(window, orient=HORIZONTAL, bootstyle="light-round")
# scrolly = ttk.Scrollbar(window, orient=VERTICAL, bootstyle="light-round")
# scrolly.pack(side=RIGHT, fill=Y)
# scrollx.pack(side=BOTTOM, fill=X)

#CODE VIEW
# txt = tk.Text(window, font="consolas 16", wrap="none", xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=100)
window.rowconfigure(1, weight=1)


def openTerminal():
    print("OPEN TERMINAL")
    operating_system = platform.system()

    # Command to open the default terminal based on the operating system
    if operating_system == 'Windows':
        # Path to Windows Terminal executable
        windows_terminal_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'WindowsApps', 'wt.exe')
        subprocess.Popen([windows_terminal_path])
    elif operating_system == 'Linux':
        subprocess.Popen('xdg-terminal', shell=True)
    elif operating_system == 'Darwin':  # macOS
        subprocess.Popen('open -a Terminal', shell=True)
    else:
        print(f"Unsupported operating system: {operating_system}")

default_lang = "python"
selected_lexer = pygments.lexers.get_lexer_by_name(default_lang)


option_var = tk.StringVar(value="Language")
def print_selected_value():
    selected_value = option_var.get()
    print(selected_value)
    # selected_lexer = pygments.lexers.get_lexer_by_name(selected_value)
    new_lexer = pygments.lexers.get_lexer_by_name(selected_value)
    txt.config(lexer=new_lexer)
    txt.highlight_all()


# https://github.com/rdbende/chlorophyll/blob/main/chlorophyll/codeview.py

# txtData = tk.StringVar()
txt = CodeView(window, lexer=selected_lexer, font="consolas 13", wrap="none", color_scheme="ayu-dark")

txt.grid(row="1", column="0", sticky="nsew")
txt.focus()

# !FIXME enables undo functionality, but is rough
txt.config(undo=True)


txtwrap = tk.BooleanVar(window)
txtwrap.set(False)

# bottombar = ttk.Combobox(window)
# for option in ['Python', 'Rust', 'HTML']:
#     bottombar.insert('end', option)
# bottombar.pack(anchor="e")

bottom_bar = ctk.CTkFrame(master=window)



mb = ttk.Menubutton(master=bottom_bar, text="Language", textvariable=option_var,style='secondary.TMenubutton')
menu = tk.Menu(mb)
# add options

for label, value in language_pairs.items():
    menu.add_radiobutton(label=label, value=value,variable=option_var,command=print_selected_value)
# associate menu with menubutton
mb['menu'] = menu
mb.pack(side='right')


terminal_btn = ctk.CTkButton(master=bottom_bar,text="Open Terminal", corner_radius=0, fg_color=("#875AFB","#277DFF"), command=openTerminal, width=110)
terminal_btn.pack(side='left')

# !FIXME
theme_var = tk.StringVar()

def set_theme():
    theme = theme_var.get()
    if theme == "light":
        txt.config(color_scheme="ayu-light")
        window.style.theme_use(themename='pulse')
        ctk.set_appearance_mode("dark")

    if theme == "dark":
        txt.config(color_scheme="ayu-dark")
        window.style.theme_use(themename='cyborg')
        ctk.set_appearance_mode("dark")


    else:
        pass

theme_menu_option = ttk.Menubutton(master=bottom_bar, text="Theme", style="secondary.TMenubutton")
theme_options = tk.Menu(theme_menu_option)
for theme in ['light', 'dark']:
    theme_options.add_radiobutton(label=theme, value=theme, variable=theme_var, command=set_theme)
theme_menu_option['menu'] = theme_options
theme_menu_option.pack(side='left')

bottom_bar.grid(row=2, column=0, sticky="nsew")

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

    font = ctk.CTkLabel(fontBox, text="Font:", font="constanta 12 bold").grid(row=0, column=0, padx=15, pady=5)
    fName = tk.StringVar(fontBox)
    fName.set(currFname)
    fontlist = sorted([i for i in tkfont.families() if i[0].isalpha()])
    fonts = Combobox(fontBox, textvariable=fName, values=fontlist, font=("", 10), state="readonly").grid(row=0, column=1)
    
    size = ctk.CTkLabel(fontBox, text="Size:", font="constanta 12 bold").grid(row=1, column=0, padx=15, pady=5)
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

            # !DEBUG
            print(newfont)

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
        # FIXME
        # scrollx.pack_forget()
    else:
        txt.pack_forget()
        txt.config(wrap="none")
        # FIXME
        # scrollx.pack(side=BOTTOM, fill=X) 
        txt.grid(column=1, row=0, sticky="nsew")


#HELP MENU OPTIONS

def about(*args):
    aboutbox = tk.Toplevel(window)
    aboutbox.transient(window)
    aboutbox.title("About JotPad")
    aboutbox.geometry("250x200")
    aboutbox.resizable(0, 0)
    aboutbox.iconbitmap("icon.ico")
    msg = f"JotPad \nVersion: {ver} \n\nDeveloped by: \nAnurag Chattopadhyay \nMandraSaptak Mandal"
    ctk.CTkLabel(aboutbox, text=msg, font=("", "11"), justify="left", pady=10).pack()
    aboutbox.focus()

    def okpress():
        aboutbox.destroy()
        aboutbox.update()

    tk.Button(aboutbox, text="OK", font=("", "10", "bold"), width=10, command=okpress).pack()
    


#menubar
# dark_bg = "#333333"
# dark_fg = "#ffffff"

# DEBUG: you cannot change the menubar bg in Windows or Mac, possible in linux
# menubar = ctkmenu.CTkMenuBar(window)
# menubar.grid(column=3)



menubar = ttk.Menu(window, tearoff=False)


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
# edit = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Edit", menu=edit)
# edit.add_command(label="Select All", font=("", 10), command=selectAll, accelerator="Ctrl+A")
# edit.add_command(label="Cut", font=("", 10), command=cut, accelerator="Ctrl+X")
# edit.add_command(label="Copy", font=("", 10), command=copy, accelerator="Ctrl+C")
# edit.add_command(label="Paste", font=("", 10), command=paste, accelerator="Ctrl+V")



#view menu
# view = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="View", menu=view)
# view.add_command(label="Font Settings", font=("", 10), command=fontSet)
# view.add_separator()
# view.add_checkbutton(label="Text Wrap", variable=txtwrap, command=txtwrapSet)

#help menu
# help = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Help", menu=help)
# help.add_command(label="About", font=("", 10), command=about)




#config
newfile()
# FIXME
# scrollx.config(command=txt.xview)
# scrolly.config(command=txt.yview)



# def close_window(event):
#     event.widget.quit()  # Close the window
window.bind_all("<Control-q>", confirmExit)

# Function to handle undo action
def undo_action(event=None):
    txt.edit_undo()
    print("UNDO")


# Function to handle redo action
def redo_action(event=None):
    txt.edit_redo()
    print("REDO")

window.bind('<Control-z>', undo_action)
window.bind('<Control-y>', redo_action)

# window.config(menu=menubar)
window.bind('<Control-n>', newfile)
window.bind('<Control-o>', openfile)
window.bind('<Control-S>', saveAs)
window.bind('<Control-s>', save)

window.protocol("WM_DELETE_WINDOW", confirmExit)
window.mainloop()


