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
 
logo = "/home/pi/Desktop/thesis/tkinter/"

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
#GPIO OUTPUTS TO LOW
GPIO.output(GPIO21_Fwd, GPIO.LOW)
GPIO.output(GPIO20_Rev, GPIO.LOW)
GPIO.output(GPIO26_Stop, GPIO.LOW)


master = tk.Tk()
master.title("GPIO Control")
master.attributes("-fullscreen", True)
master.configure(background='black')

myFont = font.Font(family='Helvetica', size=20, weight='bold')
smallFont = font.Font(family='Helvetica', size=15, weight='bold')



Fwd_state = False
Rev_state = False


def FwdButton():
    global Fwd_state, Rev_state, FWDlabel, OL_global
    if OL_global == True:
        FWDlabel['text'] = "Cannot start\nOL Detected"
    elif Fwd_state == True:
        print("FWD RUNNING ALREADY")
        INFOlabel['text'] = "WARNING: Motor already in Forward run"     
    elif Rev_state == False:
        GPIO.output(GPIO21_Fwd, GPIO.HIGH)
        Fwd_state = True
        FWDlabel['text'] = "FORWARD RUNNING"
        REVlabel['text'] = "LOCKED"
        print("FORWARD push button pressed, relay going ON")
        INFOlabel['text'] = "COMMAND: Forward button pressed"
        sleep(sleep_timer)
        GPIO.output(GPIO21_Fwd, GPIO.LOW)
        print("Fwd relay going OFF")
        #FWDlabel = tk.Label(master, text="REVERSE ON", bg="black", fg="green")
        #FWDlabel.grid(row=0, column=1)
        #FWDlabel['font'] = myFont
    elif Rev_state == True:
        FWDlabel['text'] = "STOP MOTOR FIRST\nBEFORE FORWARDING"
        STOPlabel['text'] = "STOP MOTOR FIRST\nBEFORE CHANGING"
        INFOlabel['text'] = "INVALID OPERATION: Motor must first be turned off\nbefore switching between Forward/Reverse"
        print("WARNING: REVERSE ALREADY RUNNING")
    else:
        print("UNHANDLED CONDITION in FWD FUNC")

def RevButton():
    global Fwd_state, Rev_state, REVlabel, OL_global
    if OL_global == True:
        REVlabel['text'] = "Cannot start\nOL Detected"
    elif Rev_state == True:
        print("REVERSE RUNNING ALREADY") 
        INFOlabel['text'] = "WARNING: Motor already in Reverse run" 
    elif Fwd_state == False:
        GPIO.output(GPIO20_Rev, GPIO.HIGH)
        Rev_state = True
        print("REVERSE push button pressed, relay going ON")
        INFOlabel['text'] = "COMMAND: Reverse button pressed"
        sleep(sleep_timer)
        GPIO.output(GPIO20_Rev, GPIO.LOW)
        print("Rev relay OFF")
        #REVlabel = tk.Label(master, text="REVERSE ON", bg="black", fg="green")
       # REVlabel['font'] = myFont
       # REVlabel.grid(row=1, column=1)
        FWDlabel['text'] = "LOCKED"
        REVlabel['text'] = "REVERSE RUN"
    elif Fwd_state == True:
        FWDlabel['text'] = "REVERSE RUNNING"
        REVlabel['text'] = "STOP MOTOR FIRST\nBEFORE REVERSING"
        STOPlabel['text'] = "STOP MOTOR FIRST\nBEFORE CHANGING"
        INFOlabel['text'] = "INVALID OPERATION: Motor must first be turned off\nbefore switching between Forward/Reverse"
        print("WARNING: FORWARD ALREADY RUNNING")
    else:
        print("UNHANDLED CONDITION in REV FUNC")
        
def StopButton():
    global Fwd_state, Rev_state
    Fwd_state = False
    Rev_state = False
    GPIO.output(GPIO20_Rev, GPIO.LOW)
    GPIO.output(GPIO21_Fwd, GPIO.LOW)
    ### STOP RELAY WILL BE NC, SIGNAL WILL SWITCH TO NO
    print("STOP button, relay going ON(NC TO NO)")
    GPIO.output(GPIO26_Stop, GPIO.HIGH)
    master.after(2000, AfterTimerOff)
    #sleep(sleep_timer)
    #GPIO.output(GPIO26_Stop, GPIO.LOW)
    print("Relay going off(NO to NC)")
    FWDlabel['text'] = "MOTOR STOP"
    REVlabel['text'] = "MOTOR STOP"
    STOPlabel['text'] = "MOTOR STOP"
    INFOlabel['text'] = "WARNING: Please make sure the motor is \ncompletely stopped before changing reverse/forward"
    
  #  FWDlabel = tk.Label(master, text="MOTOR STOPPED", bg="black", fg="green")
  #  REVlabel = tk.Label(master, text="MOTOR STOPPED", bg="black", fg="green")
    print("STOPPED")

def AfterTimerOff():
    GPIO.output(GPIO26_Stop, GPIO.LOW)
    print("Entered after timer")
    print("STOP NO TO NC now LOW")
    
OL_global = False
OL_global = GPIO.input(GPIO5_OL)
def TurnOffOL():
    global OL_global
    OL_global=False
    
def OverLoadCheck():
    global OL_global, OLbutton
    OL_global = GPIO.input(GPIO5_OL)
    #print("###OVERLOAD CHECKER###")
    #master.after(10000, TurnOffOL)
    if OL_global == True:
        OLbutton['activebackground']="orange"
        OLbutton['bg']="orange"
        OLbutton['text']="OVERLOAD\nDETECTED"
        INFOlabel['text'] = "CRITICAL: OVERLOAD DETECTED"
        Fwd_state = False
        Rev_state = False
        GPIO.output(GPIO20_Rev, GPIO.LOW)
        GPIO.output(GPIO21_Fwd, GPIO.LOW)
        GPIO.output(GPIO26_Stop, GPIO.HIGH)
        master.after(2000, AfterTimerOff)
        FWDlabel['text'] = "OVERLOAD STOP"
        REVlabel['text'] = "OVERLOAD STOP"
        STOPlabel['text'] = "MOTOR STOP"        
    elif OL_global == False:
        OLbutton['bg']="gray"
        OLbutton['activebackground']="gray"
        OLbutton['text']="OVERLOAD\nINDICATOR" 
    master.after(2000, OverLoadCheck)


###OVERLOAD CHECK
master.after(2000, OverLoadCheck)
###OVERLOAD CHECK
FWDbutton = tk.Button(master, text="Forward",activebackground="#4dff4d", bg="#00b300", command=FwdButton, height="3", width="6",bd=6, padx=30, pady=30, )
FWDbutton.grid(row=0, column=0)

REVbutton = tk.Button(master, text="Reverse",activebackground="#4dff4d",bg="#00b300" , command=RevButton,height="3", width="6",bd =6, padx=30, pady=30, )
REVbutton.grid(row=1, column=0)

STOPbutton = tk.Button(master, text="STOP",activebackground="#ff1a1a", bg="#cc0000" , command=StopButton,height="3", width="6",bd =6, padx=30, pady=30, )
STOPbutton.grid(row=2, column=0)

OLbutton = tk.Button(master, text="OVERLOAD\nINDICATOR",activebackground="gray", bg="gray", fg="black" ,height="3", width="6",bd =6, padx=30, pady=30, )
#OLbutton.grid(row=2, column=7, sticky='e')
OLbutton.place(x =500, y=200)
FWDlabel = tk.Label(master, text="Fwd Idle", bg="black", fg="white" , justify='left')
FWDlabel.grid(row=0, column=2, padx=20, sticky='w', )
FWDlabel['font'] = myFont
REVlabel = tk.Label(master, text="Rev Idle", bg="black", fg="white", justify='left')
REVlabel.grid(row=1, column=2,padx=20, sticky='w',)
REVlabel['font'] = myFont
STOPlabel = tk.Label(master, text="Stop motor first\nbefore switching", bg="black", fg="white", justify='left' )
STOPlabel.grid(row=2, column=2,padx=20, sticky='w',)
STOPlabel['font'] = myFont

INFOlabel = tk.Label(master, bg="black", fg="white", anchor="sw", justify='left')
INFOlabel.grid(row=3, column=0, padx=30, pady=30,sticky='w', columnspan=10, rowspan=3)

NElabel = tk.Label(master, bg="black", fg="#00a3cc", anchor="ne", justify='center', text="Forward/Reverse\nMotor Controller",)
NElabel.place(x =700, y=70)
NElabel1 = tk.Label(master, bg="black", fg="#00a3cc", anchor="ne", justify='center', text="by Gearbulk ETO Cadets\nBATCH 3",)
NElabel1.place(x =700, y=150)
INFOlabel['font'] = smallFont
REVbutton['font'] = myFont
FWDbutton['font'] = myFont
STOPbutton['font'] = myFont
OLbutton['font']=smallFont
NElabel['font']=myFont
NElabel1['font']=smallFont

gb = Image.open(logo+'gearbulk.png')
ph = ImageTk.PhotoImage(gb)
gearbulk = tk.Button(master, image=ph,highlightthickness=0 )
gearbulk.place(x =700, y=250)

ntc = Image.open(logo+'NTC.png')
ph2 = ImageTk.PhotoImage(ntc)
ntcbutton = tk.Button(master, image=ph2,highlightthickness=0 )
ntcbutton.place(x =700, y=320)

yong = Image.open(logo+'yong.png')
ph3 = ImageTk.PhotoImage(yong)
yongbutton = tk.Button(master, image=ph3,highlightthickness=0 )
yongbutton.place(x =500, y=420)

def my_time():
    time_string = strftime('%H:%M:%S %p \n %A \n %x') # time format 
    timeWin['text']=time_string
    timeWin.after(1000,my_time) # time delay of 1000 milliseconds 
    print("time")
    


timeWin=tk.Label(master,font=('Helvetica', 25, 'bold'), bg='black', fg='yellow', justify='right')
timeWin.place(x=800, y=480)

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

