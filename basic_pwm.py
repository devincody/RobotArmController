import numpy as np
import RPi.GPIO as GPIO
import time
import random
from Tkinter import *

GPIO.setmode(GPIO.BOARD)

rate = 70.0
scale = rate/50.0
pins = [7,11,18,13,15,16]
joint = []

for i in range(len(pins)):
	GPIO.setup(pins[i],GPIO.OUT)
	joint.append(GPIO.PWM(pins[i],rate)) #50hz

def home():
	joint[0].start(scale*7.5)
	joint[1].start(scale*7.5)
	joint[2].start(scale*9)
	joint[3].start(scale*7.5)
	joint[4].start(scale*7.5)
	joint[5].start(scale*8)

home()

def show_values():
    print (w1.get(), w2.get())

def show_values2(a):
    print (w1.get(), w2.get())
    master.update()

def update_servos(a):
	master.update()
	for i in range(len(pins)):
		print scaleLS[i].get()
		joint[i].start(scale*7.5)


master = Tk()

scaleLS = []
for i in range(len(pins)):
	scaleLS.append(Scale(master, from_=0, to=180, length = 300, command=update_servos))
	scaleLS[i].pack(side = LEFT)
	scaleLS.pack(side = LEFT)

Button(master, text='Home', command=home).pack()

mainloop()

