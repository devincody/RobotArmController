import numpy as np
import random as rand 
import gradient4 as grad
import os
import time

# Pins:
# Base (Rotation)			11
# Shoulder					13
# Elbow						15
# Wrist						16
# Hand						18
# Grip						22
# Ground					6,9,14,20,25

# Pin Scheme:
# 2-4-6-8-10-12-14-16-18-20-22 			vid mic
# 1-3-5-7-09-11-13-15-17-19
# SD card

pwm_pin = [1,3,4,5,6,7]
raw_pin = [11,13,15,16,18,22]

ang = np.zeros([6,3])
data = np.zeros([6,3])
ang[0] = [90, 0, -90] #Rotation
ang[1] = [180, 90, 0]# Shoulder
ang[2] = [-128, -90, 0]# Elbow	
ang[3] = [-159.3, -90, 0]
ang[4] = [0, 90, 180]# Hand
ang[5] = [0, 90, 180]# Grip	0 = open, 180 = closed

data[0] = [75, 36, 00]# Base (Rotation)
data[1] = [05, 42, 80]# Shoulder	
data[2] = [82, 57, 18]# Elbow	
data[3] = [84, 53, 15]# Wrist	
data[4] = [04, 41, 80]# Hand	
data[5] = [50, 66, 83]# Grip	

# cd PiBits/ServoBlaster/user/
# sudo ./servod
os.chdir("PiBits")
os.chdir("ServoBlaster")
os.chdir("user")
os.system('sudo ./servod')



class servo(object):
	def __init__(self,pin, angles,percent):
		self.pin = pin
		self.angles = angles
		self.percent = percent
	def set_servo_to(self,angle):
		duty = self.angle2duty(angle)
		print "angle = ", angle, ", duty = ", duty
		message = "echo %d=%d%% > /dev/servoblaster" %(self.pin, duty)
		print "about to write the following message: ", message
		os.system(message)
	def angle2duty(self,angle):
		if angle > self.angles[1]:
			Range = 1
		else:
			Range = 0
		slope = (self.percent[1+Range]-self.percent[0+Range])/(self.angles[1+Range]-self.angles[0+Range])
		y_int = self.percent[1+Range] - slope*self.angles[1+Range]
		per = slope*angle +y_int
		return per

Rotation = servo(pwm_pin[0],ang[0],data[0])
Shoulder = servo(pwm_pin[1],ang[1],data[1])
Elbow = servo(pwm_pin[2],ang[2],data[2])
Wrist = servo(pwm_pin[3],ang[3],data[3])
Hand = servo(pwm_pin[4],ang[4],data[4])
Grip = servo(pwm_pin[5],ang[5],data[5])

previous = [.2,.5,-.6,-.2]

instruct_list = [[0.1,2,7],[7,2,7]] #[X,Y,Z]
for i in range(len(instruct_list)):
	r = np.sqrt(instruct_list[i][0]**2 + instruct_list[i][1]**2)
	theta = np.arctan(instruct_list[i][1]/instruct_list[i][0])
	final, other = grad.optimize_gradient([r,instruct_list[i][2]],previous[1:])

	waypts = 50
	interp = []
	interp.append(np.linspace(previous[0],theta,waypts))
	for k in range(1,len(previous)):
		interp.append(np.linspace(previous[k],final[k-1][0],waypts))
		previous[k] = final[k-1][0]
	#interp1 = interp*180/np.pi

	for j in range(waypts):
		Rotation.set_servo_to(interp[0][j]*180/np.pi)
		Shoulder.set_servo_to(interp[1][j]*180/np.pi)
		Elbow.set_servo_to(interp[2][j]*180/np.pi)
		Wrist.set_servo_to(interp[3][j]*180/np.pi)
		time.sleep(.01)

	previous[0] = theta
	time.sleep(1)


def kill_all():
	for i in range(7):
		message = "echo %d=0 > /dev/servoblaster" %(i)
		os.system(message)

# cd PiBits/ServoBlaster/user/
# sudo ./servod
# echo 1=0 > /dev/servoblaster
# echo 2=0 > /dev/servoblaster
# echo 3=0 > /dev/servoblaster
# echo 4=0 > /dev/servoblaster
# echo 5=0 > /dev/servoblaster
# echo 6=0 > /dev/servoblaster
# echo 7=0 > /dev/servoblaster





time.sleep(10)
kill_all()
