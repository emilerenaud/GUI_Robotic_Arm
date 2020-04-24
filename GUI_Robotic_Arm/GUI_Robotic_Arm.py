import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
from array import array
import time
from datetime import datetime

import pyftdi.serialext
import serial





class GUI():
    def __init__(self):

        try:
            None
            #self.ser = serial.Serial('COM9')
            #if self.ser.isOpen:
            #    print(self.ser.name + 'Communication Open')

            #self.ser.bytesize = 8
            #self.ser.stopbits = 1
            #self.ser.baud = 9600
        except:
            print('serial error')

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
        self.GUI_RIGHT_FRAME.pack(side=tk.LEFT,fill=tk.BOTH)

        # Sub Frame
        self.GUI_COM_FRAME = ttk.Frame(self.GUI_LEFT_FRAME,borderwidth=2, relief=tk.GROOVE)
        self.GUI_DRIVER_FRAME = ttk.Frame(self.GUI_LEFT_FRAME, borderwidth=2, relief=tk.GROOVE)
        self.GUI_FUNCTION_FRAME = ttk.Frame(self.GUI_RIGHT_FRAME, borderwidth=2, relief=tk.GROOVE)

        self.GUI_COM_FRAME.pack(side=tk.TOP)
        self.GUI_DRIVER_FRAME.pack(side=tk.TOP)
        self.GUI_FUNCTION_FRAME.pack(side=tk.TOP)

        # COM Frame Widgets
        self.COM_main_label = ttk.Label(self.GUI_COM_FRAME,text='COM')
        self.COM_selection = tk.StringVar()
        self.COM_windows_button = ttk.Radiobutton(self.GUI_COM_FRAME,text='Windows',variable=self.COM_selection,value='windows')
        self.COM_beaglebone_button = ttk.Radiobutton(self.GUI_COM_FRAME,text='BeagleBone',variable=self.COM_selection,value='beaglebone')
        self.COM_start_stop_button = ttk.Button(self.GUI_COM_FRAME,text='Start',command=self.sendSerialTest)

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
        self.FUNC_enable_motor = ttk.Button(self.GUI_FUNCTION_FRAME,text='Enable Motor')
        self.FUNC_position_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=4)
        self.FUNC_send_motor_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send Motor')
        self.FUNC_position_servo = ttk.Entry(self.GUI_FUNCTION_FRAME,width=4)
        self.FUNC_send_servo_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send Servo')
        self.FUNC_red_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Red Light')
        self.FUNC_green_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Green Light')
        self.FUNC_blue_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Blue Light')
        self.FUNC_ask_feedback_var = tk.BooleanVar()
        self.FUNC_ask_feedback_check = ttk.Checkbutton(self.GUI_FUNCTION_FRAME,text='Feedback',variable=self.FUNC_ask_feedback_var)
        self.FUNC_trame_label = ttk.Label(self.GUI_FUNCTION_FRAME,text='Trame :')
        self.FUNC_trame_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=20)
        self.FUNC_trame_send_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send')

        self.FUNC_driver_label.grid(row=0,column=0,sticky=tk.E)
        self.FUNC_driver_combo.grid(row=0,column=1)
        self.FUNC_home_button.grid(row=1,column=0,sticky=tk.EW)
        self.FUNC_enable_motor.grid(row=1,column=1,sticky=tk.EW)
        self.FUNC_position_entry.grid(row=2,column=0)
        self.FUNC_send_motor_button.grid(row=2,column=1)
        self.FUNC_position_servo.grid(row=3,column=0)
        self.FUNC_send_servo_button.grid(row=3,column=1)
        self.FUNC_red_button.grid(row=4,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_green_button.grid(row=5,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_blue_button.grid(row=6,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_ask_feedback_check.grid(row=7,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_trame_label.grid(row=8,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_trame_entry.grid(row=9,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_trame_send_button.grid(row=10,column=1,sticky=tk.EW)


    def sendSerialTest(self):
        port = pyftdi.serialext.serial_for_url('ftdi://ftdi:232:A50285BI/1', baudrate=9600)
        cw = [0x12]
        port.write(serial.to_bytes([0x12]))

app = GUI()
app.app.mainloop()