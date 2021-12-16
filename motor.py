#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import os
import sys
import tkinter as tk
import tkinter.font as font
import time
from time import strftime
from PIL import Image, ImageTk

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
 
logo = "/home/pi/Desktop/thesis/main_git/"

GPIO21_Fwd = 21
GPIO20_Rev = 20
GPIO26_Stop = 26
GPIO5_OL = 5

sleep_timer = 1
GPIO.setmode(GPIO.BCM)
#GPIO SETUP I/O
GPIO.setup(GPIO21_Fwd, GPIO.OUT)
GPIO.setup(GPIO20_Rev, GPIO.OUT)
GPIO.setup(GPIO26_Stop, GPIO.OUT)
##### CONNECT A SERIES RESISTOR FROM 3.3v to GPIO 5 FOR OVERLOAD
GPIO.setup(GPIO5_OL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##### CONNECT A SERIES RESISTOR FROM 3.3v to GPIO 5 FOR OVERLOAD
#GPIO OUTPUTS TO HIGH because of logic low relay
GPIO.output(GPIO21_Fwd, GPIO.HIGH)
GPIO.output(GPIO20_Rev, GPIO.HIGH)
GPIO.output(GPIO26_Stop, GPIO.HIGH)


canvassinit_time = 10000
canvassinfo_time = 20000

master = tk.Tk()
master.title("GPIO Control")
master.attributes("-fullscreen", True)
master.configure(background='black')

myFont = font.Font(family='Helvetica', size=20, weight='bold')
smallFont = font.Font(family='Helvetica', size=15, weight='bold')
OLFont = font.Font(family='Helvetica', size=10, weight='bold')
titleFont = font.Font(family='Helvetica', size=23, weight='bold')


Fwd_state = False
Rev_state = False


def FwdButton():
    global Fwd_state, Rev_state, FWDlabel, OL_global, canvassbutton, p8, canvassforward, canvassbuffer
    if OL_global == True:
        FWDlabel['text'] = "Cannot start\nOL Detected"
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray"
        FWDbutton['activebackground'] = "gray"
        REVbutton['activebackground'] = "gray"
    elif Fwd_state == True:
        print("FWD RUNNING ALREADY")
        INFOlabel['text'] = "WARNING:\nMotor already in Forward run" 
        FWDbutton['activebackground']="#4dff4d"     
    elif Rev_state == False:
        GPIO.output(GPIO21_Fwd, GPIO.LOW)
        REVbutton['activebackground']="gray" 
        FWDbutton['activebackground']="#4dff4d" 
        FWDbutton['bg'] = "#4dff4d"
        REVbutton['bg'] = "gray"
        Fwd_state = True
        FWDlabel['text'] = "FORWARD RUN"
        REVlabel['text'] = "LOCKED"
        REVbutton['bg'] = "gray"
        print("\nFORWARD SW ON\n")
        INFOlabel['text'] = "COMMAND:\nForward button pressed"
        #p8 = Image.open(logo+'canvassforward.png')
        #canvassforward = ImageTk.PhotoImage(p8)
        canvassbutton['image']=canvassforward
        canvassbuffer = canvassforward
        sleep(sleep_timer)
        GPIO.output(GPIO21_Fwd, GPIO.HIGH)
        print("Fwd SW OFF\n\n\n")
    elif Rev_state == True:
        FWDbutton['activebackground']="gray"    
        REVbutton['bg'] = "#4dff4d"
        REVlabel['text'] = "REVERSE RUNNING"
        FWDlabel['text'] = "LOCKED"
        STOPlabel['text'] = "STOP MOTOR FIRST\nBEFORE CHANGING"
        INFOlabel['text'] = "INVALID OPERATION:\nMotor must first be turned off\nbefore switching Forward/Reverse"
        print("WARNING: REVERSE ALREADY RUNNING")
    else:
        print("UNHANDLED CONDITION in FWD FUNC")

def RevButton():
    global Fwd_state, Rev_state, REVlabel, OL_global, canvassbutton, p7, canvassreverse,canvassbuffer
    if OL_global == True:
        REVlabel['text'] = "Cannot start\nOL Detected"
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray"
        FWDbutton['activebackground'] = "gray"
        REVbutton['activebackground'] = "gray"
    elif Rev_state == True:
        print("REVERSE RUNNING ALREADY")
        REVbutton['activebackground']="#4dff4d"
        INFOlabel['text'] = "WARNING:\nMotor already in Reverse run" 
    elif Fwd_state == False:
        GPIO.output(GPIO20_Rev, GPIO.LOW)
        FWDbutton['activebackground']="gray" 
        REVbutton['activebackground']="#4dff4d"
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "#4dff4d"
        FWDlabel['text'] = "LOCKED"
        REVlabel['text'] = "REVERSE RUN"
        #p7 = Image.open(logo+'canvassreverse.png')
        #canvassreverse = ImageTk.PhotoImage(p7)
        canvassbutton['image']= canvassreverse
        canvassbuffer = canvassreverse
        Rev_state = True
        print("\n\nREVERSE ON")
        INFOlabel['text'] = "COMMAND:\nReverse button pressed"
        sleep(sleep_timer)
        GPIO.output(GPIO20_Rev, GPIO.HIGH)
        print("Rev relay OFF\n\n")

    elif Fwd_state == True:
        REVbutton['activebackground']="gray"
        FWDbutton['bg'] = "#4dff4d"
        REVbutton['bg'] = "gray"
        FWDlabel['text'] = "FORWARD RUNNING"
        REVlabel['text'] = "LOCKED"
        STOPlabel['text'] = "STOP MOTOR FIRST\nBEFORE CHANGING"
        INFOlabel['text'] = "INVALID OPERATION:\nMotor must first be turned off\nbefore switching Forward/Reverse"
        print("WARNING: FORWARD ALREADY RUNNING")
    else:
        print("UNHANDLED CONDITION in REV FUNC")
        
def StopButton():
    global Fwd_state, Rev_state, canvassbutton, p6, canvassstop, canvassbuffer
    if OL_global == True:
        GPIO.output(GPIO26_Stop, GPIO.LOW)
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray"
    else:
        Fwd_state = False
        Rev_state = False
        GPIO.output(GPIO20_Rev, GPIO.HIGH)
        GPIO.output(GPIO21_Fwd, GPIO.HIGH)
        if not(Fwd_state or Rev_state):
            canvassbutton['image']=canvassstop
            canvassbuffer = canvassstop
        ### STOP RELAY WILL BE NC, SIGNAL WILL SWITCH TO NO
        print("\n\nSTOP press")
        GPIO.output(GPIO26_Stop, GPIO.LOW)
        master.after(2000, AfterTimerOff)
        sleep(sleep_timer)
        #GPIO.output(GPIO26_Stop, GPIO.LOW)
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray"
        FWDlabel['text'] = "MOTOR STOP"
        REVlabel['text'] = "MOTOR STOP"
        STOPlabel['text'] = "MOTOR STOP"
        INFOlabel['text'] = "WARNING:\nPlease make sure the motor is \ncompletely stopped before start"
        print("STOPPED")

def AfterTimerOff():
    GPIO.output(GPIO26_Stop, GPIO.HIGH)
    print("Stop depress\n\n")
    
    

OL_global = False
OL_global = GPIO.input(GPIO5_OL)
#OL_global = True
def TurnOffOL():
    global OL_global
    OL_global=False

def OverLoadCheck():
    global OL_global, OLbutton, stopOnceOL, canvassbutton, p9, canvassoverload, p6, canvassstop, canvassbuffer, FWDbutton, REVbutton
    OL_global = GPIO.input(GPIO5_OL)
    #master.after(10000, TurnOffOL)   ###### OVERLOAD TEST AUTOMATIC TURN OFF
    if OL_global == True:
        FWDbutton['activebackground'] = "gray"
        REVbutton['activebackground'] = "gray"
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray"
        OLbutton['activebackground']="orange"
        OLbutton['bg']="orange"
        OLbutton['text']="OL\nDETECTED"
        INFOlabel['text'] = "CRITICAL: OVERLOAD DETECTED"
        Fwd_state = False
        Rev_state = False
        GPIO.output(GPIO20_Rev, GPIO.HIGH)
        GPIO.output(GPIO21_Fwd, GPIO.HIGH)
        GPIO.output(GPIO26_Stop, GPIO.LOW)
        FWDlabel['text'] = "OVERLOAD STOP"
        REVlabel['text'] = "OVERLOAD STOP"
        STOPlabel['text'] = "RESET"
        FWDbutton['bg'] = "gray"
        REVbutton['bg'] = "gray" 
        canvassbutton['image']=canvassoverload
        canvassbuffer=canvassoverload
    elif OL_global == False:
        OLbutton['bg']="gray"
        OLbutton['activebackground']="gray"
        OLbutton['text']="OVER\nLOAD" 
        GPIO.output(GPIO26_Stop, GPIO.HIGH) #turn off stop button after OL
    master.after(2000, OverLoadCheck)

def creditsbuttonClick():
    global creditsbutton, canvassbutton, p5, canvassinfo, canvassbuffer
    canvassbutton['image']=canvassinfo
    master.after(canvassinfo_time, canvassChangeBack)

def canvassChangeBack():
    global canvassbutton, canvassbuffer
    canvassbutton['image']=canvassbuffer
    
##   #4dff4d    light green #00b300
###OVERLOAD CHECK
master.after(2000, OverLoadCheck)
###OVERLOAD CHECK
FWDbutton = tk.Button(master, text="Forward", bg="gray", command=FwdButton, height="3", width="6",bd=6,  )
FWDbutton.place(x=20, y=20)

REVbutton = tk.Button(master, text="Reverse",bg="gray" , command=RevButton,height="3", width="6",bd =6,  )
REVbutton.place(x=20, y=140)

STOPbutton = tk.Button(master, text="STOP",activebackground="#ff1a1a", bg="#cc0000" , command=StopButton,height="3", width="6",bd =6,  )
STOPbutton.place(x=20, y=260)

OLbutton = tk.Button(master, text="OVER\nLOAD",activebackground="gray", bg="gray", fg="black" ,height="3", width="8",bd =6,  )
OLbutton.place(x =20, y=390)

creditsbutton = tk.Button(master, text="INFO",activebackground="#b9ff2b", bg="#6f9620", fg="black" ,height="3", width="5",bd =6,  command=creditsbuttonClick )
creditsbutton.place(x =1000, y=300, anchor='e')

FWDlabel = tk.Label(master, text="Fwd Idle", bg="black", fg="white" , justify='left')
FWDlabel.place(x=160, y=65)
FWDlabel['font'] = smallFont
REVlabel = tk.Label(master, text="Rev Idle", bg="black", fg="white", justify='left')
REVlabel.place(x=160, y=180)
REVlabel['font'] = smallFont
STOPlabel = tk.Label(master, text="Stop motor first\nbefore switching", bg="black", fg="white", justify='left' )
STOPlabel.place(x=160, y=295)
STOPlabel['font'] = smallFont

INFOlabel = tk.Label(master, bg="black", fg="white", anchor="sw", justify='left')
INFOlabel.place(x=15, y=510)

titleLabel = tk.Label(master, bg="black", fg="#00a3cc", anchor="ne", justify='center', text="FORWARD/REVERSE\nMOTOR CONTROLLER",)
titleLabel.place(x =350, y=490)

subTitle = tk.Label(master, bg="black", fg="#00a3cc", anchor="ne", justify='center', text="by Gearbulk ETO Cadets\nBATCH 3",)
subTitle.place(x =400, y=550)


INFOlabel['font'] = smallFont
REVbutton['font'] = myFont
FWDbutton['font'] = myFont
STOPbutton['font'] = myFont
OLbutton['font']=smallFont
titleLabel['font']=titleFont
subTitle['font']=smallFont
creditsbutton['font']=smallFont

etm = Image.open(logo+'etm.png')
ph3 = ImageTk.PhotoImage(etm)
etmbutton = tk.Button(master, image=ph3,highlightthickness=0 )
etmbutton.place(x =1000, y=405, anchor='e')

gb = Image.open(logo+'gearbulk.png')
ph = ImageTk.PhotoImage(gb)
gearbulk = tk.Button(master, image=ph,highlightthickness=0 )
gearbulk.place(x =1000, y=490, anchor='e')

ntc = Image.open(logo+'NTC.png')
ph2 = ImageTk.PhotoImage(ntc)
ntcbutton = tk.Button(master, image=ph2,highlightthickness=0 )
ntcbutton.place(x =1000, y=560, anchor='e')

p4 = Image.open(logo+'canvassinfo.png')
canvassinit = ImageTk.PhotoImage(p4)
p5 = Image.open(logo+'canvassinfo.png')
canvassinfo = ImageTk.PhotoImage(p5)
p6 = Image.open(logo+'canvassstop.png')
canvassstop = ImageTk.PhotoImage(p6)
p7 = Image.open(logo+'canvassreverse.png')
canvassreverse = ImageTk.PhotoImage(p7)
p8 = Image.open(logo+'canvassforward.png')
canvassforward = ImageTk.PhotoImage(p8)
p9 = Image.open(logo+'canvassoverload.png')
canvassoverload = ImageTk.PhotoImage(p9)

canvassbuffer = canvassstop
canvassbutton = tk.Button(master, image=canvassinit ,highlightthickness=0 )
canvassbutton.place(x =835, y=240, anchor='e')
master.after(canvassinit_time, canvassChangeBack)

def my_time():
    time_string = strftime('%H:%M:%S %p \n %A \n %x') # time format 
    timeWin['text']=time_string
    timeWin.after(1000,my_time) # time delay of 1000 milliseconds 
    

timeWin=tk.Label(master,font=('Helvetica', 15, 'bold'), bg='black', fg='yellow', justify='right')
timeWin.place(x=1010, y=20, anchor='ne')

my_time()

def main():
    master.attributes("-fullscreen",True)
    master.config(cursor='none')
    master.mainloop()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('INTERRUPT..\n CLEANING UP GPIO PORTS\n')
        sys.exit(0)

