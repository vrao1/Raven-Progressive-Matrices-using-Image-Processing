import sys
from PIL import Image, ImageChops
import numpy as np
import operator
import math

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

def mainD04(problem):
	imageList = []
	
	im6 = Image.open(problem.figures["F"].visualFilename)
	im6 = im6.convert("L")
	
	im6_shaded , left, upper, right,lower = separateComponents(im6)
	#im6_shaded.show()
	
	im6_arr = list(im6.getdata())
	im6_shaded_arr = list(im6_shaded.getdata())
	
	height, width = im6.size
	total_length = height*width
	im6_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im6_contour_arr[i] = XNOR(im6_arr[i], im6_shaded_arr[i])
		i = i+1
	
	im6_contour = Image.new(im6.mode, im6.size, "white")
	im6_contour.putdata(im6_contour_arr)
	
	#im6_contour.show()
	
	im8 = Image.open(problem.figures["H"].visualFilename)
	im8 = im8.convert("L")
	
	im8_middle , left, upper, right,lower = separateComponents(im8)
	
	#im8_middle.show()
	
	rectangle = (left, upper, right,lower)
	im6_contour.paste(im8_middle.crop(rectangle), rectangle)
	#im6_contour.show()
	
	im9 = im6_contour
	
	i = 1
	minDiff=99999999
	answer=0
	
	while i < 9:
		image_name = problem.figures[str(i)].visualFilename
		newImg = Image.open(image_name)
		newImg = newImg.convert("L")
		newDiff = rmsdiff_1997(im9, newImg)
		print("New Difference")
		print(newDiff)
		print("Min Difference")
		print(minDiff)
		if(minDiff > newDiff):
			minDiff = newDiff
			answer = i
		#newImg.show()
		i = i + 1
	
	return(answer)
