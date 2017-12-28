import sys
from PIL import Image, ImageChops
import numpy as np
import operator
import math

# Count Number of Black Pixels
def countBlackPixels(im):
	count = 0
	height, width = im.size
	total_length = height*width
	im_arr = list(im.getdata())
	for i in range(total_length):
		if im_arr[i] == 0:
			count = count + 1

	return count
	
#To find Right Most and Left Most Black point

def findExtrema(im,height,width):
	X_MIN = 999999
	X_MAX = -1000
	Y_MIN = 999999
	Y_MAX = -1000

	for i in range(height):
		for j in range(width):
			stride = (width*i) + j 
			if im[stride] == 0:
				if X_MIN > j:
					X_MIN = j
				if X_MAX < j:
					X_MAX = j

				if Y_MIN > i:
					Y_MIN = i
				if Y_MAX < i:
					Y_MAX = i

	return (X_MIN,X_MAX,Y_MIN,Y_MAX)

def XNOR(x,y):
	x_inv = -1
	y_inv = -1

	if x == 0:
		x_inv = 1
	else:
		x = 1
		x_inv = 0

	if y == 0:
		y_inv = 1
	else:
		y = 1
		y_inv = 0
	
	res =  ((x_inv and y_inv) or (x and y))
	if res == 1:
		return 255

	return res
	
def rmsdiff_1997(im1, im2):
	#"Calculate the root-mean-square difference between two images"

	h = ImageChops.difference(im1, im2).histogram()

	summation = 0
	denominator = float(im1.size[0]) * im1.size[1]

        # calculate rms
	for i in range(256):
		summation += h[i]*(i**2)

	quotient = summation/denominator
	return math.sqrt(quotient)

def calculateDiff(img1,img2):
	s = 0
	m1 = np.array(img1).reshape(*img1.size)
	m2 = np.array(img2).reshape(*img2.size)
	s += np.sum(np.abs(m1-m2))
	return s

def isEqual(im1, im2):
	im_diff = ImageChops.difference(im1, im2)
	diff_array = np.asarray(im_diff)
	return not np.nonzero(diff_array)
	#print(diff_array[np.nonzero(diff_array)])

def separateComponents(im):
	height, width = im.size
	arr = list(im.getdata())
	#print(arr)
	#sys.exit(3)
	totalLength = height * width

	originX = int(width/2)
	originY = int(height/2)

	MAX_X = originX
	MIN_X = originX
	MAX_Y = originY
	MIN_Y = originY

	# j is Y
	# i is X
	# Traverse 1st Quadrant
	j = originY*width + originX
	
	while arr[j] == 0:
		i = j
		offset = originX
		while arr[i] == 0:
			i = i+1
			offset = offset + 1

		if offset > MAX_X:
			MAX_X = offset
		j = j-width

	# Traverse 4th Quadrant
	j = originY*width + originX
	while arr[j] == 0:
		i = j
		offset = originX
		while arr[i] == 0:
			i = i+1
			offset = offset + 1

		if offset > MAX_X:
			MAX_X = offset
		j = j+width

	# Traverse 3rd Quadrant
	j = originY*width + originX
	while arr[j] == 0:
		i = j
		offset = originX
		while arr[i] == 0:
			i = i-1
			offset = offset - 1

		if offset < MIN_X:
			MIN_X = offset
		j = j-width

	# Traverse 4th Quadrant
	j = originY*width + originX
	while arr[j] == 0:
		i = j
		offset = originX
		while arr[i] == 0:
			i = i-1
			offset = offset - 1

		if offset < MIN_X:
			MIN_X = offset
		j = j+width

	# For MIN Y
	# Traverse 1st Quadrant
	i = originY*width + originX
	
	while arr[i] == 0:
		j = i
		offset = originY
		while arr[j] == 0:
			j = j - width
			offset = offset - 1

		if offset < MIN_Y:
			MIN_Y = offset
		print("1st MIN_Y = %d \n" % (MIN_Y))
		i = i+1

	# Traverse 2nd Quadrant
	i = originY*width + originX
	
	while arr[i] == 0:
		j = i
		offset = originY
		while arr[j] == 0:
			j = j - width
			offset = offset - 1

		if offset < MIN_Y:
			MIN_Y = offset
		print("2nd MIN_Y = %d \n" % (MIN_Y))
		i = i-1

	# Traverse 3rd Quadrant
	i = originY*width + originX
	
	while arr[i] == 0:
		j = i
		offset = originY
		while arr[j] == 0:
			j = j + width
			offset = offset + 1

		if offset > MAX_Y:
			MAX_Y = offset
		i = i-1

	# Traverse 4th Quadrant
	i = originY*width + originX
	
	while arr[i] == 0:
		j = i
		offset = originY
		while arr[j] == 0:
			j = j + width
			offset = offset + 1

		if offset > MAX_Y:
			MAX_Y = offset
		i = i+1

	rectangle = (MIN_X,MIN_Y,MAX_X,MAX_Y)
	croppedImg = im.crop(rectangle)
	newImg = Image.new(im.mode, im.size, "white")
	newImg.paste(croppedImg, rectangle)
	return (newImg, MIN_X,MIN_Y,MAX_X,MAX_Y) 	

def mainD09(problem):
	sampleListAlpha = ['A','B','C','D','E','F','G','H']
	queryFlag = [True] * 8
	ansFlag = [True] * 8
	
	for i in range(8):
	
		qus_image = problem.figures[str(sampleListAlpha[i])].visualFilename
		qusImg = Image.open(qus_image)
		qusImg = qusImg.convert("L")
		diffMIN = 999999.0
		whichIndex = -1
	
		for j in range(8):
			ans_image = problem.figures[str(j+1)].visualFilename
			ansImg = Image.open(ans_image)
			ansImg = ansImg.convert("L")
			diff = rmsdiff_1997(qusImg, ansImg)
			if diff < diffMIN:
				diffMIN = diff
				whichIndex = j	
	
		if diffMIN < 50.0 and whichIndex >= 0:
			queryFlag[i] = False
			ansFlag[whichIndex] = False
	
	for i in range(8):
		if ansFlag[i] == True:
			return(i+1)
