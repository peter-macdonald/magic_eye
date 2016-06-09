#!/usr/bin/python

import numpy as np
import scipy.misc as smp
import math
from random import *
import time

t = time.clock()
dt = time.clock() - t
print "Null time: %f" % dt
t = time.clock()

HEIGHT = 500
WIDTH = 1000

def dist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


#data[512,512] = [254,0,0]       # Makes the middle pixel red
#data[512,513] = [0,0,255]       # Makes the next pixel blue

# Generate interesting repeating pattern image
def genRandPattern(height,width):
	pat = np.zeros( (height,width,3), dtype=np.uint8)
	for x in range(width):
		for y in range(height):
			pat[y,x] = [randint(0,255),randint(0,255),randint(0,255)]
	return pat

pattern = genRandPattern(100,100)

dt = time.clock() - t
print "Init: %f" % dt
t = time.clock()

# Generate image to be 3d
def genTestImage(width,height):
	img = np.zeros( (height,width,1), dtype=np.uint8 )
	for x in range(width):
		for y in range(width):
			d = dist(x,y,width/2,height/2)
			if ( d < 100 ):
				img[y,x] = d/10
	return img

image = genTestImage(WIDTH,HEIGHT)

dt = time.clock() - t
print "Image generation: %f" % dt
t = time.clock()

D = 100
def genShiftMap(img,width,height):
	''' 
	Shift of z where z is the height causes a rise at x, and a fall at x+D
	'''
	# Apply shift algorithm to make the image 3D
	shift_map = np.zeros( (height,width,1), dtype=np.uint8 )
	for y in range(height):
		for x in range(width):
			if ( img[y,x] > 0 ):
				for x2 in range(x,width,D):	
					shift_map[y,x2] += img[y,x]
	return shift_map

shiftmap = genShiftMap(image,WIDTH,HEIGHT)

dt = time.clock() - t
print "Shift map: %f" % dt
t = time.clock()
	
def genMagicImg(shift_map,pattern,width,height):
	magic_img = np.zeros( (height,width,3), dtype=np.uint8 )
	for y in range(height):
		for x in range(width):
			shift = shiftmap[y,x]
			px = (x+shift)%D
			py = y%D
			magic_img[y,x] = pattern[py,px]
	return magic_img

data = genMagicImg(shiftmap,pattern,WIDTH,HEIGHT)

dt = time.clock() - t
print "Magic image generation: %f" % dt
t = time.clock()
	
img = smp.toimage( data )       # Create a PIL image
img.show() 

dt = time.clock() - t
print "Output: %f" % dt
t = time.clock()
	
