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
        self.tab_parent.add(self.debug_tab,text="Debug")
        self.tab_parent.add(self.main_tab,text="Main")
        


        # TAB DEBUG
        # Main Frame
        self.GUI_LEFT_FRAME = ttk.Frame(self.debug_tab)
        self.GUI_RIGHT_FRAME = ttk.Frame(self.debug_tab)

        self.GUI_LEFT_FRAME.pack(side=tk.LEFT,fill=tk.BOTH)
        self.GUI_RIGHT_FRAME.pack(side=tk.RIGHT,fill=tk.BOTH)

        # Sub Frame
        self.GUI_COM_FRAME = ttk.Frame(self.GUI_LEFT_FRAME)
        self.GUI_DRIVER_FRAME = ttk.Frame(self.GUI_LEFT_FRAME)
        self.GUI_FUNCTION_FRAME = ttk.Frame(self.GUI_RIGHT_FRAME)

        self.GUI_COM_FRAME.pack(side=tk.TOP)
        self.GUI_DRIVER_FRAME.pack(side=tk.TOP,pady=5)
        self.GUI_FUNCTION_FRAME.pack(side=tk.TOP)

        # COM Frame Widgets
        self.COM_main_label = ttk.Label(self.GUI_COM_FRAME,text='COM')
        self.COM_selection = tk.StringVar()
        self.COM_windows_button = ttk.Radiobutton(self.GUI_COM_FRAME,text='Windows',variable=self.COM_selection,value='windows')
        self.COM_beaglebone_button = ttk.Radiobutton(self.GUI_COM_FRAME,text='BeagleBone',variable=self.COM_selection,value='beaglebone')
        self.COM_start_stop_button = ttk.Button(self.GUI_COM_FRAME,text='Start')

        self.COM_main_label.pack(side=tk.TOP,fill=tk.Y)
        self.COM_windows_button.pack(side=tk.TOP,fill=tk.Y,anchor=tk.W)
        self.COM_beaglebone_button.pack(side=tk.TOP,fill=tk.Y,anchor=tk.W)
        self.COM_start_stop_button.pack(side=tk.TOP,fill=tk.Y)

        # DRIVER Frame Widgets
        self.DRIVER_main_label = ttk.Label(self.GUI_DRIVER_FRAME,text='Driver Adress')
        self.DRIVER_main_label.grid(row=0,column=0,columnspan=3)

        self.DRIVER_label_list = list()
        self.DRIVER_entry_list = list()
        self.DRIVER_checkbox_list = list()
        self.DRIVER_checkbox_state_list = list()
        for i in range(6):
            self.DRIVER_label_list.append(ttk.Label(self.GUI_DRIVER_FRAME,text='#'+str(i+1)+' :'))
            self.DRIVER_label_list[i].grid(row=i+1,column=0)
            self.DRIVER_entry_list.append(ttk.Entry(self.GUI_DRIVER_FRAME,width=3))
            self.DRIVER_entry_list[i].grid(row=i+1,column=1,sticky=tk.W)
            self.DRIVER_checkbox_state_list.append(tk.BooleanVar())
            self.DRIVER_checkbox_list.append(ttk.Checkbutton(self.GUI_DRIVER_FRAME,variable=self.DRIVER_checkbox_state_list[i]))
            self.DRIVER_checkbox_list[i].grid(row=i+1,column=2)

        # FUNCTION Frame Widgets
        self.FUNC_driver_label = ttk.Label(self.GUI_FUNCTION_FRAME,text='Driver :')
        self.FUNC_driver_combo = ttk.Combobox(self.GUI_FUNCTION_FRAME,width=3)
        self.FUNC_driver_combo['values'] = ['#1','#2','#3','#4','#5','#6']
        self.FUNC_home_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Homing')
        


app = GUI()
app.app.mainloop()