import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox

import time
from datetime import datetime

from array import array

try:
    import pyftdi.serialext
    from pyftdi.ftdi import Ftdi
    import serial
except:
    print("Unable to import pyftdi & serial")






class GUI():
    def __init__(self):

        self.ftdi = None
        self.trameString = ''
        self.trameByte = [0x00,0x00,0x00,0x00]

        # Option Var
        self.homingEnableVar = 0
        self.enableMotorVar = 0
        self.redLightVar = 0
        self.greenLightVar = 0
        self.blueLightVar = 0

        self.initGUI()
        

    def initGUI(self):
        self.app = tk.Tk()
        self.app.geometry('800x480')     # Set size of the frame + place it at 0,0 in the screen
        self.app.configure(bg='white')    # set background
        self.app.title('GUI Robotic Arm') # set window's title
        self.app.bind("<Return>", self.handleReturn)
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
        self.COM_start_stop_button = ttk.Button(self.GUI_COM_FRAME,text='Start',command=self.gestionSerial)

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
        driveNumber = 1
        for i in range(6):
            self.DRIVER_label_list.append(ttk.Label(self.GUI_DRIVER_FRAME,text='#'+str(i+1)+' :'))
            self.DRIVER_label_list[i].grid(row=i+1,column=0)
            self.DRIVER_entry_list.append(ttk.Entry(self.GUI_DRIVER_FRAME,width=3))
            self.DRIVER_entry_list[i].insert(0,driveNumber)
            driveNumber += 1
            self.DRIVER_entry_list[i].grid(row=i+1,column=1,sticky=tk.W)
            self.DRIVER_checkbox_state_list.append(tk.BooleanVar())
            self.DRIVER_checkbox_list.append(ttk.Checkbutton(self.GUI_DRIVER_FRAME,variable=self.DRIVER_checkbox_state_list[i]))
            self.DRIVER_checkbox_list[i].grid(row=i+1,column=2)

        # FUNCTION Frame Widgets
        self.FUNC_driver_label = ttk.Label(self.GUI_FUNCTION_FRAME,text='Driver :')
        self.FUNC_driver_combo = ttk.Combobox(self.GUI_FUNCTION_FRAME,width=3)
        self.FUNC_driver_combo.bind('<<ComboboxSelected>>', self.selectDriverFunction)
        self.FUNC_driver_combo['values'] = ['#1','#2','#3','#4','#5','#6']
        self.FUNC_home_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Homing',command=self.homingFunction)
        self.FUNC_enable_motor = ttk.Button(self.GUI_FUNCTION_FRAME,text='Enable Motor',command=self.enableMotorFunction)
        self.FUNC_position_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=4)
        self.FUNC_send_motor_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send Motor',command=self.motorValueFunction)
        self.FUNC_position_servo = ttk.Entry(self.GUI_FUNCTION_FRAME,width=4)
        self.FUNC_send_servo_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send Servo',command=self.servoValueFunction)
        self.FUNC_fan_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=4)
        self.FUNC_send_fan_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send Fan',command=self.FanValueFunction)
        self.FUNC_red_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Red Light',command=self.redLightFunction)
        self.FUNC_green_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Green Light',command=self.greenLightFunction)
        self.FUNC_blue_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Blue Light',command=self.blueLightFunction)
        self.FUNC_ask_feedback_var = tk.BooleanVar()
        self.FUNC_ask_feedback_check = ttk.Checkbutton(self.GUI_FUNCTION_FRAME,text='Feedback',variable=self.FUNC_ask_feedback_var)
        self.FUNC_reset_trame = ttk.Button(self.GUI_FUNCTION_FRAME,text='Reset',command=self.resetTrame)
        self.FUNC_trame_label = ttk.Label(self.GUI_FUNCTION_FRAME,text='Trame :')
        self.FUNC_trame_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=10)
        self.FUNC_trame_entry.insert(0,'00000000')
        self.FUNC_trame_send_button = ttk.Button(self.GUI_FUNCTION_FRAME,text='Send',command=self.sendTrame)

        self.FUNC_driver_label.grid(row=0,column=0,sticky=tk.E)
        self.FUNC_driver_combo.grid(row=0,column=1)
        self.FUNC_home_button.grid(row=1,column=0,sticky=tk.EW)
        self.FUNC_enable_motor.grid(row=1,column=1,sticky=tk.EW)
        self.FUNC_position_entry.grid(row=2,column=0)
        self.FUNC_send_motor_button.grid(row=2,column=1)
        self.FUNC_position_servo.grid(row=3,column=0)
        self.FUNC_send_servo_button.grid(row=3,column=1)
        self.FUNC_fan_entry.grid(row=4,column=0)
        self.FUNC_send_fan_button.grid(row=4,column=1)
        self.FUNC_red_button.grid(row=5,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_green_button.grid(row=6,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_blue_button.grid(row=7,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_ask_feedback_check.grid(row=8,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_reset_trame.grid(row=8,column=1,sticky=tk.EW)
        self.FUNC_trame_label.grid(row=9,column=0,columnspan=2,sticky=tk.EW)
        self.FUNC_trame_entry.grid(row=10,column=0,sticky=tk.EW)
        self.FUNC_trame_send_button.grid(row=10,column=1,sticky=tk.EW)

    def gestionSerial(self):
        if self.COM_start_stop_button['text'] == 'Start':
            if self.COM_selection.get() == 'windows':
                print('start windows')
                try:
                    self.ftdi = pyftdi.serialext.serial_for_url('ftdi://ftdi:232:A50285BI/1', baudrate=9600)
                    self.COM_start_stop_button['text'] = 'Stop'

                except:
                    print('Unable to connect to Ftdi')

            elif self.COM_selection.get() == 'beaglebone':
                None
        else:
            if self.COM_selection.get() == 'windows':
                print('close windows')
                try:
                    self.ftdi.close()
                    self.COM_start_stop_button['text'] = 'Start'
                except:
                    print('Unable to close Serial Port')

            elif self.COM_selection.get() == 'beaglebone':
                None
            
    def sendTrame(self):
        if self.FUNC_trame_entry.get() != '':
            trame = self.FUNC_trame_entry.get()
            if len(trame) == 8:
                self.trameByte[0] = int(trame[0:2],16)
                self.trameByte[1] = int(trame[2:4],16)
                self.trameByte[2] = int(trame[4:6],16)
                self.trameByte[3] = int(trame[6:8],16)
                try:
                    self.ftdi.write(serial.to_bytes(self.trameByte))
                    self.trameByte = [0x00,0x00,0x00,0x00]
                except:
                    print('Error while writting on FTDI')
            else:
                print('Invalid Lenght Trame')
        else:
            print("Empty Trame")

    # Handle for Return aka ENTER
    def handleReturn(self,event):               
        if event.widget == self.FUNC_trame_entry: #if the focus is on Trame entry, send the trame
            self.sendTrame()
        elif event.widget == self.FUNC_position_entry:
            self.motorValueFunction()
        elif event.widget == self.FUNC_position_servo:
            self.servoValueFunction()
        elif event.widget == self.FUNC_fan_entry:
            self.FanValueFunction()

    def homingFunction(self):
        if self.homingEnableVar == 0:
            number = int(self.FUNC_trame_entry.get()[0:1],16)
            number += 1
            self.homingEnableVar = 1;
        else:
            number = int(self.FUNC_trame_entry.get()[0:1],16)
            number -= 1
            self.homingEnableVar = 0;

        self.writeHexinEntry(number,0,1)

    def enableMotorFunction(self):
        if self.enableMotorVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 1
            self.enableMotorVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 1
            self.enableMotorVar = 0

        self.writeHexinEntry(number,1,1)

    def redLightFunction(self):
        if self.redLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 8
            self.redLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 8
            self.redLightVar = 0

        self.writeHexinEntry(number,1,1)

    def greenLightFunction(self):
        if self.greenLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 4
            self.greenLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 4
            self.greenLightVar = 0

        self.writeHexinEntry(number,1,1)

    def blueLightFunction(self):
        if self.blueLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 2
            self.blueLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 2
            self.blueLightVar = 0

        self.writeHexinEntry(number,1,1)

    def motorValueFunction(self):
        if self.FUNC_position_entry.get() == '':
            return
        number = int(self.FUNC_position_entry.get())
        if number > 360 or number < 0:
            print("Invalid Position. 0-360 values only")
            self.FUNC_position_entry.delete(0,tk.END)
            return

        if number >= 256:
            highBit = int(self.FUNC_trame_entry.get()[3:4],16)
            if highBit % 2 == 0:
                highBit += 1
            number -= 256
        else:
            highBit = int(self.FUNC_trame_entry.get()[3:4],16)
            if highBit % 2 != 0:
                highBit -= 1
        self.writeHexinEntry(highBit,3,1)

        if number == 0:
            self.writeHexinEntry('00',4,2)
            return

        number = number.to_bytes(((number.bit_length() + 7) // 8),"big").hex() # convertion dec to hex
        self.writeHexinEntry(number,4,2)

    def servoValueFunction(self):
        if self.FUNC_position_servo.get() == '':
            return
        number = int(self.FUNC_position_servo.get())
        directionBit = int(self.FUNC_trame_entry.get()[3:4],16) # read directionBit before write new value.

        if number > 100 or number < 0:
            print("Invalid Position. 0-100 values only")
            self.FUNC_position_servo.delete(0,tk.END)
            return
        number <<= 1 # shift by 1 to free the first one.
       
        if number == 0:
            self.writeHexinEntry('00',2,2)
            if directionBit % 2 == 1:                   # if the bit is 1, write it back in the entry.
                self.writeHexinEntry(directionBit,3,1)

            return

        number = number.to_bytes(((number.bit_length() + 7) // 8),"big").hex() # convertion dec to hex
        self.writeHexinEntry(number,2,2)
        if directionBit % 2 == 1:
            number = int(self.FUNC_trame_entry.get()[3:4],16)
            number += 1
            self.writeHexinEntry(number,3,1)

    def FanValueFunction(self):
        if self.FUNC_fan_entry.get() == '':
            return
        number = int(self.FUNC_fan_entry.get())
        if number > 100 or number < 0:
            print("Invalid Number. 0-100 values only")
            self.FUNC_fan_entry.delete(0,tk.END)
            return
        if number == 0:
            self.writeHexinEntry('00',6,2)
            return

        number = number.to_bytes(((number.bit_length() + 7) // 8),"big").hex() # convertion dec to hex
        self.writeHexinEntry(number,6,2)

    def writeHexinEntry(self,number,position,lenght):

        if number == 10:
            number = 'a'
        elif number == 11:
            number = 'b'
        elif number == 12:
            number = 'c'
        elif number == 13:
            number = 'd'
        elif number == 14:
            number = 'e'
        elif number == 15:
            number = 'f'

        self.FUNC_trame_entry.delete(position,position+lenght)
        self.FUNC_trame_entry.insert(position,str(number))

    def resetTrame(self):
        self.FUNC_trame_entry.delete(0,tk.END)
        self.FUNC_trame_entry.insert(0,'00000000')
        self.homingEnableVar = 0
        self.enableMotorVar = 0
        self.redLightVar = 0
        self.greenLightVar = 0
        self.blueLightVar = 0
        self.FUNC_position_entry.delete(0,tk.END)
        self.FUNC_position_servo.delete(0,tk.END)
        self.FUNC_fan_entry.delete(0,tk.END)

    def selectDriverFunction(self,event=None):
         wantedDriver = self.FUNC_driver_combo.get()
         driverNumber = 0
         for i in range(len(self.DRIVER_label_list)):
             if self.DRIVER_label_list[i]['text'][0:2] == wantedDriver: # Compare the isolated string from the label to the driver Combo box
                 driverNumber = i
                 break
         number = int(self.DRIVER_entry_list[i].get())
         number <<= 1
         homing = int(self.FUNC_trame_entry.get(),16) # take the homing value.
         self.writeHexinEntry(number,0,1)
         if homing % 2 == 1:
             number = int(self.FUNC_trame_entry.get()[0:1],16)
             number += 1
             self.writeHexinEntry(number,0,1)



        
                



app = GUI()
app.app.mainloop()