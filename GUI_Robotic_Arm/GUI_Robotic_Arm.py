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

import ikpy
import numpy as np





class GUI():
    def __init__(self):

        self.ftdi = None
        self.trameString = ''
        self.trameByte = [0x00,0x00,0x00,0x00,0x00]
        self.checksumByte = [0x00,0x00,0x00,0x00,0x00]
        # Option Var
        self.homingEnableVar = 0
        self.enableMotorVar = 0
        self.redLightVar = 0
        self.greenLightVar = 0
        self.blueLightVar = 0
        self.driverNumber = 0
        self.homing = 0
        self.lsbPosition = 0
        self.gripperPosition = 0
        self.angle = [0,0,0,0,0]

        #Open URDF file of arm for links and chains
        self.my_chain = ikpy.chain.Chain.from_urdf_file("ur3_robot.urdf")

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
        self.initTabDebug()
        self.initTabMain()

    def initTabMain(self):
        # Main Frame
        self.GUI_LEFT_FRAME_MAIN = ttk.Frame(self.main_tab)
        self.GUI_RIGHT_FRAME_MAIN = ttk.Frame(self.main_tab)

        self.GUI_LEFT_FRAME_MAIN.pack(side=tk.LEFT,fill=tk.BOTH)
        self.GUI_RIGHT_FRAME_MAIN.pack(side=tk.LEFT,fill=tk.BOTH)

        # KI position widget
        self.KI_position_label = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "Robot end effector")

        self.x_label = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "X:")
        self.x_entry = ttk.Entry(self.GUI_LEFT_FRAME_MAIN, width = 3)
        self.y_label = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "Y:")
        self.y_entry = ttk.Entry(self.GUI_LEFT_FRAME_MAIN, width = 3)
        self.z_label = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "Z:")
        self.z_entry = ttk.Entry(self.GUI_LEFT_FRAME_MAIN, width = 3)

        self.calculateAngle = ttk.Button(self.GUI_LEFT_FRAME_MAIN, text = "Calculate",command = self.calculateKI)

        self.final_angle_one = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "1:")
        self.final_angle_two = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "2:")
        self.final_angle_three = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "3:")
        self.final_angle_four = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "4:")
        self.final_angle_five = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "5:")
        self.final_angle_six = ttk.Label(self.GUI_LEFT_FRAME_MAIN, text = "6:")

        self.sendAngle = ttk.Button(self.GUI_LEFT_FRAME_MAIN, text = "Send Angle", command = self.sendAngle)

        # Place widget
        self.KI_position_label.grid(row=0,column=0,columnspan=6,sticky=tk.EW,padx=5,pady=5)

        self.x_label.grid(row=1,column=0)
        self.x_entry.grid(row=1,column=1)
        self.y_label.grid(row=1,column=2)
        self.y_entry.grid(row=1,column=3)
        self.z_label.grid(row=1,column=4)
        self.z_entry.grid(row=1,column=5)

        self.calculateAngle.grid(row=2,column=0,columnspan=6,sticky=tk.EW)

        self.final_angle_one.grid(row=3,column=0,columnspan=2,sticky=tk.EW)
        self.final_angle_two.grid(row=3,column=2,columnspan=2,sticky=tk.EW)
        self.final_angle_three.grid(row=3,column=4,columnspan=2,sticky=tk.EW)
        self.final_angle_four.grid(row=4,column=0,columnspan=2,sticky=tk.EW)
        self.final_angle_five.grid(row=4,column=2,columnspan=2,sticky=tk.EW)
        self.final_angle_six.grid(row=4,column=4,columnspan=2,sticky=tk.EW)

        self.sendAngle.grid(row=5,column=0,columnspan=6,sticky=tk.EW)

        # Graph robot.

    def calculateKI(self):
        if (self.x_entry.get() != None) & (self.y_entry.get() != None) & (self.z_entry.get() != None):
            x = float(self.x_entry.get()) /100
            y = float(self.y_entry.get()) /100
            z = float(self.z_entry.get()) /100
        else:
            return 0
        #Matrice for end-effector's position
        target_position = [x, y, z]

        #List of joints angles
        angles = self.my_chain.inverse_kinematics(target_position)

        #Convert radians to degrees
        for a in range(len(angles) - 2):
            angles[a] = np.degrees(angles[a])

        #Add offset to angles (homing 0's)
        self.final_angle_one['text'] = "1: " + str(int(angles[1] + 85))
        self.final_angle_two['text'] = "2: " + str(int(angles[2] + 135))
        self.final_angle_three['text'] = "3: " + str(int(angles[3] + 110))
        self.final_angle_four['text'] = "4: " + str(int(angles[4] + 146))
        self.final_angle_five['text'] = "5: " + str(int(angles[5] + 180))
        self.final_angle_six['text'] = "6: 0"

        self.angle[0] = int(angles[1] + 95)
        self.angle[1] = int(angles[2] + 135)
        self.angle[2] = int(angles[3] + 110)
        self.angle[3] = int(angles[4] + 146)
        self.angle[4] = int(angles[5] + 180)

    def sendAngle(self):
        i = 1
        if self.enableMotorVar == 0:
            self.enableMotorFunction()
        for angle in self.angle:
            self.FUNC_position_entry.delete(0,tk.END)
            self.FUNC_position_entry.insert(0, angle)
            self.motorValueFunction()
            self.FUNC_driver_combo.current(i)
            self.selectDriverFunction()
            i += 1
            self.sendTrame()
            time.sleep(0.5)





    def initTabDebug(self):
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
        driveNumber = 0
        for i in range(7):
            self.DRIVER_label_list.append(ttk.Label(self.GUI_DRIVER_FRAME,text='#'+str(i)+' :'))
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
        self.FUNC_driver_combo['values'] = ['#0','#1','#2','#3','#4','#5','#6']
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
        self.FUNC_trame_string = tk.StringVar()
        self.FUNC_trame_string.set('0000000000')
        #self.FUNC_trame_string.trace('w',self.calculateCheckSum)
        self.FUNC_trame_entry = ttk.Entry(self.GUI_FUNCTION_FRAME,width=10,textvariable=self.FUNC_trame_string)
        #self.FUNC_trame_entry.insert(0,'0000000000')
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
                    self.ftdi = pyftdi.serialext.serial_for_url('ftdi://ftdi:232:A50285BI/1', baudrate=19200) # Change for FTDI.
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
            if len(trame) == 10:
                switch = trame[1] + trame[0]
                self.trameByte[0] = int(switch, 16)
                
                switch = trame[3] + trame[2]
                self.trameByte[1] = int(switch, 16)

                switch = trame[5] + trame[4]
                self.trameByte[2] = int(switch, 16)

                switch = trame[7] + trame[6]
                self.trameByte[3] = int(switch, 16)

                switch = trame[9] + trame[8]
                self.trameByte[4] = int(switch, 16)

                try:
                    self.ftdi.write(serial.to_bytes(self.trameByte))
                    #self.ftdi.read()
                    #print(self.ftdi.read(5))
                    self.trameByte = [0x00,0x00,0x00,0x00,0x00]
                except:
                    print('Error while writting on FTDI')
            else:
                print('Invalid Trame Length')
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

    # Address 0-2 (3b)
    def selectDriverFunction(self,event=None):
         number = self.FUNC_driver_combo.get()
         self.driverNumber = int(number[1])
         number = self.homing + self.driverNumber
         self.writeHexinEntry(number,0,1) 

    # Homing 3 (1b)
    def homingFunction(self):
        if self.homingEnableVar == 0:
            number = 8
            self.FUNC_position_entry.delete(0,tk.END)
            self.FUNC_position_entry.insert(0, '0')
            self.motorValueFunction()
            self.homingEnableVar = 1;
        else:
            number = 0
            self.homingEnableVar = 0;
        self.homing = number
        number = self.homing + self.driverNumber
        self.writeHexinEntry(number,0,1) 

    # RGBMode 4-6 (3b)
    def redLightFunction(self):
        if self.redLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 1
            self.redLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 1
            self.redLightVar = 0

        self.writeHexinEntry(number,1,1)

    def greenLightFunction(self):
        if self.greenLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 2
            self.greenLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 2
            self.greenLightVar = 0

        self.writeHexinEntry(number,1,1)

    def blueLightFunction(self):
        if self.blueLightVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 4
            self.blueLightVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 4
            self.blueLightVar = 0

        self.writeHexinEntry(number,1,1)

    # Enable/Disable 7 (1b)
    def enableMotorFunction(self):
        if self.enableMotorVar == 0:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number += 8
            self.enableMotorVar = 1
        else:
            number = int(self.FUNC_trame_entry.get()[1:2],16)
            number -= 8
            self.enableMotorVar = 0

        self.writeHexinEntry(number,1,1)

    # Gripper 8-14 (7b)
    def servoValueFunction(self):
        if self.FUNC_position_servo.get() == '':
            return
        position = int(self.FUNC_position_servo.get())

        if position > 100 or position < 0:
            print("Invalid Position. 0-100 values only")
            self.FUNC_position_servo.delete(0,tk.END)
            return

        self.gripperPosition = position & 0x7F
        position = self.gripperPosition + self.lsbPosition
        self.writeHexinEntry((position & 0x0F),2,1)
        self.writeHexinEntry((position >> 4),3,1)

    # Position 15-23 (9b)
    def motorValueFunction(self):
        if self.FUNC_position_entry.get() == '':
            return
        self.homingEnableVar = 0;
        self.writeHexinEntry(0 + self.driverNumber,0,1) 
        number = int(self.FUNC_position_entry.get())
        if number > 360 or number < 0:
            print("Invalid Position. 0-360 values only")
            self.FUNC_position_entry.delete(0,tk.END)
            return

        self.lsbPosition = (number & 0x01) << 7
        position = self.gripperPosition + self.lsbPosition
        self.writeHexinEntry((position & 0x0F),2,1)
        self.writeHexinEntry((position >> 4),3,1)

        number = number >> 1
        self.writeHexinEntry((number & 0x0F),4,1)
        self.writeHexinEntry((number >> 4),5,1)

    # Fan 24-31 (8b)
    def FanValueFunction(self):
        if self.FUNC_fan_entry.get() == '':
            return
        number = int(self.FUNC_fan_entry.get())

        if number > 100 or number < 0:
            print("Invalid Number. 0-100 values only")
            self.FUNC_fan_entry.delete(0,tk.END)
            return

        #if number == 0:
        #    self.writeHexinEntry('00',6,2)
        #    return

        self.writeHexinEntry((number & 0x0F), 6, 1)
        self.writeHexinEntry((number >> 4), 7, 1)

    # Checksum 32-39 (8b)
    def calculateCheckSum(self):
        #trame = self.FUNC_trame_entry.get()
        trame = self.FUNC_trame_string.get()
        print(len(trame))
        if len(trame) == 10:
            switch = trame[1] + trame[0]
            self.checksumByte[0] = int(switch, 16)
                
            switch = trame[3] + trame[2]
            self.checksumByte[1] = int(switch, 16)

            switch = trame[5] + trame[4]
            self.checksumByte[2] = int(switch, 16)

            switch = trame[7] + trame[6]
            self.checksumByte[3] = int(switch, 16)

            self.checksumByte[4] = self.checksumByte[0] + self.checksumByte[1] + self.checksumByte[2] + self.checksumByte[3]
            if self.checksumByte[4] >= 256:
                self.checksumByte[4] -= 256
            
            print(hex(self.checksumByte[4]))
            number = self.checksumByte[4]

            lsb = number >> 4

            if lsb == 10:
                lsb = 'a'
            elif lsb == 11:
                lsb = 'b'
            elif lsb == 12:
                lsb = 'c'
            elif lsb == 13:
                lsb = 'd'
            elif lsb == 14:
                lsb = 'e'
            elif lsb == 15:
                lsb = 'f'

            msb = number & 0x0F

            if msb == 10:
                msb = 'a'
            elif msb == 11:
                msb = 'b'
            elif msb == 12:
                msb = 'c'
            elif msb == 13:
                msb = 'd'
            elif msb == 14:
                msb = 'e'
            elif msb == 15:
                msb = 'f'

            self.FUNC_trame_entry.delete(8, 9)
            self.FUNC_trame_entry.insert(8,msb)
            self.FUNC_trame_entry.delete(9, 10)
            self.FUNC_trame_entry.insert(9,lsb)
        else:
            print('Invalid lenght checksum')

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
        self.calculateCheckSum()

    def resetTrame(self):
        self.FUNC_trame_entry.delete(0,tk.END)
        self.FUNC_trame_entry.insert(0,'0000000000')
        self.homingEnableVar = 0
        self.enableMotorVar = 0
        self.redLightVar = 0
        self.greenLightVar = 0
        self.blueLightVar = 0
        self.homing = 0
        self.driverNumber = 0
        self.lsbPosition = 0
        self.gripperPosition = 0
        self.FUNC_position_entry.delete(0,tk.END)
        self.FUNC_position_servo.delete(0,tk.END)
        self.FUNC_fan_entry.delete(0,tk.END)
        self.selectDriverFunction()



app = GUI()
app.app.mainloop()