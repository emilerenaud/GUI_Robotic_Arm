import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox

import time
from datetime import datetime

class GUI():
    def __init__(self):

        self.app = tk.Tk()
        self.app.geometry('1280x800')     # Set size of the frame + place it at 0,0 in the screen
        self.app.configure(bg='white')    # set background
        self.app.title('GUI Robotic Arm') # set window's title

        # STYLE
        self.style = ttk.Style()
        self.style.configure('TFrame',background='white')
        self.style.configure('TLabel',foreground='black',background='white')
        self.style.configure('TCheckbutton',foreground='black',background='white')
        self.style.configure('TRadiobutton',foreground='black',background='white')

        # TAB
        self.tab_parent = ttk.Notebook(self.app)
        self.tab_parent.pack(expand=True,fill=tk.BOTH)
        self.main_tab = ttk.Frame(self.tab_parent)
        self.debug_tab = ttk.Frame(self.tab_parent)
        self.tab_parent.add(self.main_tab,text="Main")
        self.tab_parent.add(self.debug_tab,text="Debug")


        # TAB DEBUG
        # Main Frame
        self.GUI_COM_FRAME = ttk.Frame(self.app)
        self.GUI_DRIVER_FRAME = ttk.Frame(self.app)
        self.GUI_FUNCTION_FRAME = ttk.Frame(self.app)



app = GUI()
app.app.mainloop()