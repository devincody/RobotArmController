import numpy as np

import random as rand 
lib = 1
try:
	import matplotlib.pyplot as plt
except:
	lib = 0

arm_len = np.zeros([4,1])
arm_len[0] = 4.257
arm_len[1] = 3.93
arm_len[2] = 6.5 #change if needed for open/close
arm_len[3] = 1.225

def gradient(dest, prev_ang):
	prev_ang2 = prev_ang
	dimensions = len(dest) #x,y,z
	numb_joints = len(prev_ang2) #angles in radians (4)
	#print numb_joints
	#print dimensions
	destination = np.zeros([dimensions,1])#typically 3 rows, 1 column

	curr_ang = np.zeros([numb_joints,1])
	next_ang = np.zeros([numb_joints,1])

	#curr_ang[0] = rand.uniform(0,np.pi/2)
	for i in range(0,len(curr_ang)):
	 	curr_ang[i] = prev_ang2[i] #-rand.uniform(0,np.pi/2)

	for i in range(dimensions):
		destination[i] = float(dest[i]) #make destination object is an numpy array
	jacob = np.zeros([dimensions,numb_joints])
	alpha = .01 #learning rate
	trig = np.zeros([dimensions,numb_joints+1])
	valsx = [] #DEBUG
	valsy = [] #DEBUG
	dist = 3.0
	while dist > .1:
		#print "dist ", dist
		for i in range(numb_joints):
			trig[0][i] = np.sin(curr_ang[0:i+1].sum())
			trig[1][i] = np.cos(curr_ang[0:i+1].sum())

		trig[0][numb_joints] = np.cos(curr_ang.sum())
		trig[1][numb_joints] = np.sin(curr_ang.sum())
		#print curr_ang
		#print trig
		arm_foo = np.zeros([4,1])
		arm_foo[:] = arm_len
		#print trig
		for j in range(numb_joints):
			#print "j",j
			jacob[0][j] = - np.dot(trig[0],arm_foo)
			jacob[1][j] = np.dot(trig[1],arm_foo)
			#print arm_foo, jacob
			arm_foo[j] = 0
		#print jacob
		Tjacob = np.transpose(jacob)

		curr_loc = np.zeros([dimensions,1])
		curr_loc[0] = np.dot(trig[1],arm_len)
		curr_loc[1] = np.dot(trig[0],arm_len)
		#print Tjacob

		error = destination - curr_loc
		#print error
		dist = np.sqrt(np.dot(np.transpose(error), error))
		
		#print dist
		next_ang = curr_ang + alpha * np.dot(Tjacob,error)
		curr_ang = next_ang
		valsx.append(curr_loc[0])
		valsy.append(curr_loc[1])
	jointx = np.zeros(numb_joints+1)
	jointy = np.zeros(numb_joints+1)
	for i in range(1,numb_joints+1):
		jointx[i] = jointx[i-1]+trig[1][i-1]*arm_len[i-1]
		jointy[i] = jointy[i-1]+trig[0][i-1]*arm_len[i-1]
	
	print curr_loc
	print curr_ang*180/np.pi
	# #fig = plt.figure()
	# plt.plot(valsx,valsy)
	# #plt.show()
	# plt.clf()

	# plt.plot(jointx,jointy)
	# #plt.show()
	# #plt.clf()
	return curr_ang #should be in radians
	

#gradient([6,7],[.5,-.6,-.2])

def optimize_gradient(a,b): # b is in radians
	soln = []
	angle_min = []
	for r in range(5):
		flag = 1
		while flag != 0:
			b2=[]
			for t in range(len(b)):
				b2.append(rand.gauss(0,.25) + b[t]) #add some noise
			print "starting ", b2
			angles = gradient(a,b2) #angles should be in radians
			print "angles: ", angles
			angles1 = angles*180/np.pi
			flag = 0
			for w in range(len(angles1)):
				if w == 0:
					if angles1[w] < 27.6 or angles1[w] > 180:
						flag += 1
				if w == 1:
					if angles1[w] < -128 or angles1[w] > 0:
						flag += 1
				if w == 2:
					if angles1[w] < -159.3 or angles1[w] > 0:
						flag += 1
			print "flag: ", flag
		soln.append(angles)
		diff = np.zeros(len(angles))
		for y in range(len(angles)):
			diff[y] = angles[y] - b[y]
		#print "diff",  diff
		dist1 = np.sqrt(np.dot(np.transpose(diff),diff))
		#print "dist1", dist1
		angle_min.append(dist1)
	print "minimum angle movement", angle_min
	ans = soln[angle_min.index(min(angle_min))]
	return ans, soln

if lib == 1:
	final, soln = optimize_gradient([4.34,7.69],[2,-.5,-1.3])
	# print final*180/np.pi

	# trig = np.zeros([2,4])

	# trig[0] = np.zeros(4)
	# trig[1] = np.zeros(4)

	# for i in range(len(final)):
	# 	trig[0][i] = np.sin(final[0:i+1].sum())
	# 	trig[1][i] = np.cos(final[0:i+1].sum())

	# trig[0][3] = np.cos(final.sum())
	# trig[1][3] = np.sin(final.sum())

	# jointx = np.zeros(4)
	# jointy = np.zeros(4)

	# for i in range(1,len(jointy)):
	# 	jointx[i] = jointx[i-1]+trig[1][i-1]*arm_len[i-1]
	# 	jointy[i] = jointy[i-1]+trig[0][i-1]*arm_len[i-1]

	# jointx[len(jointy)-1] += trig[1][3]*arm_len[3] 
	# jointy[len(jointy)-1] += trig[0][3]*arm_len[3] 

	# fig = plt.figure()
	# plt.scatter(jointx,jointy)
	# plt.show()

	for i in soln:
		final = i
		trig = np.zeros([2,4])
		trig[0] = np.zeros(4)
		trig[1] = np.zeros(4)

		for i in range(len(final)):
			trig[0][i] = np.sin(final[0:i+1].sum())
			trig[1][i] = np.cos(final[0:i+1].sum())

		trig[0][3] = np.cos(final.sum())
		trig[1][3] = np.sin(final.sum())

		jointx = np.zeros(4)
		jointy = np.zeros(4)

		for i in range(1,len(jointy)):
			jointx[i] = jointx[i-1]+trig[1][i-1]*arm_len[i-1]
			jointy[i] = jointy[i-1]+trig[0][i-1]*arm_len[i-1]

		jointx[len(jointy)-1] += trig[1][3]*arm_len[3] 
		jointy[len(jointy)-1] += trig[0][3]*arm_len[3] 

		plt.plot(jointx,jointy)
	plt.title("Family of Possible Solutions")
	plt.show()




