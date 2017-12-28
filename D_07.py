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

def mainD07(problem):
	sampleShadedImageList = []
	sampleContourImageList = []
	queryShadedImageList = []
	queryContourImageList = []
	sampleImageRectangleList = []
	
	im1 = Image.open(problem.figures["A"].visualFilename)
	im1 = im1.convert("L")
	
	im1_shaded , left, upper, right,lower = separateComponents(im1)
	sampleShadedImageList.append(im1_shaded)
	rect = (left, upper, right,lower)
	sampleImageRectangleList.append(rect)
	#im1_shaded.show()
	
	im1_arr = list(im1.getdata())
	im1_shaded_arr = list(im1_shaded.getdata())
	
	height, width = im1.size
	total_length = height*width
	im1_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im1_contour_arr[i] = XNOR(im1_arr[i], im1_shaded_arr[i])
		i = i+1
	
	im1_contour = Image.new(im1.mode, im1.size, "white")
	im1_contour.putdata(im1_contour_arr)
	sampleContourImageList.append(im1_contour)
	#im1_contour.show()
	
	im2 = Image.open(problem.figures["B"].visualFilename)
	im2 = im2.convert("L")
	
	im2_shaded , left, upper, right,lower = separateComponents(im2)
	sampleShadedImageList.append(im2_shaded)
	rect = (left, upper, right,lower)
	sampleImageRectangleList.append(rect)
	#im2_shaded.show()
	
	im2_arr = list(im2.getdata())
	im2_shaded_arr = list(im2_shaded.getdata())
	
	height, width = im2.size
	total_length = height*width
	im2_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im2_contour_arr[i] = XNOR(im2_arr[i], im2_shaded_arr[i])
		i = i+1
	
	im2_contour = Image.new(im2.mode, im2.size, "white")
	im2_contour.putdata(im2_contour_arr)
	sampleContourImageList.append(im2_contour)
	#im2_contour.show()
	
	im3 = Image.open(problem.figures["C"].visualFilename)
	im3 = im3.convert("L")
	
	im3_shaded , left, upper, right,lower = separateComponents(im3)
	sampleShadedImageList.append(im3_shaded)
	rect = (left, upper, right,lower)
	sampleImageRectangleList.append(rect)
	#im3_shaded.show()
	
	im3_arr = list(im3.getdata())
	im3_shaded_arr = list(im3_shaded.getdata())
	
	height, width = im3.size
	total_length = height*width
	im3_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im3_contour_arr[i] = XNOR(im3_arr[i], im3_shaded_arr[i])
		i = i+1
	
	im3_contour = Image.new(im3.mode, im3.size, "white")
	im3_contour.putdata(im3_contour_arr)
	sampleContourImageList.append(im3_contour)
	#im3_contour.show()
	
	im7 = Image.open(problem.figures["G"].visualFilename)
	im7 = im7.convert("L")
	
	im7_shaded , left, upper, right,lower = separateComponents(im7)
	queryShadedImageList.append(im7_shaded)
	#im7_shaded.show()
	
	im7_arr = list(im7.getdata())
	im7_shaded_arr = list(im7_shaded.getdata())
	
	height, width = im7.size
	total_length = height*width
	im7_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im7_contour_arr[i] = XNOR(im7_arr[i], im7_shaded_arr[i])
		i = i+1
	
	im7_contour = Image.new(im7.mode, im7.size, "white")
	im7_contour.putdata(im7_contour_arr)
	queryContourImageList.append(im7_contour)
	#im7_contour.show()
	
	im8 = Image.open(problem.figures["H"].visualFilename)
	im8 = im8.convert("L")
	
	im8_shaded , left, upper, right,lower = separateComponents(im8)
	queryShadedImageList.append(im8_shaded)
	#im8_shaded.show()
	
	im8_arr = list(im8.getdata())
	im8_shaded_arr = list(im8_shaded.getdata())
	
	height, width = im8.size
	total_length = height*width
	im8_contour_arr = [255] * total_length
	
	i = 0
	while i < total_length:
		im8_contour_arr[i] = XNOR(im8_arr[i], im8_shaded_arr[i])
		i = i+1
	
	im8_contour = Image.new(im8.mode, im8.size, "white")
	im8_contour.putdata(im8_contour_arr)
	queryContourImageList.append(im8_contour)
	#im8_contour.show()
	
	# FINISH
	
	
	#Loop to find Contour
	lengthQuery = len(queryContourImageList)
	for i in range(lengthQuery):
		lengthSample = len(sampleContourImageList)
		diffMIN = 99999.0
		whichIndex=-1
		for j in range(lengthSample):
			diff = rmsdiff_1997(queryContourImageList[i], sampleContourImageList[j])
			if diff < diffMIN:
				diffMIN = diff
				whichIndex = j
		if whichIndex != -1:
			del sampleContourImageList[whichIndex]
	
	im9_contour = sampleContourImageList[0]
	#im9_contour.show()
	
	#Loop to find Shaded Area
	lengthQuery = len(queryShadedImageList)
	for i in range(lengthQuery):
		lengthSample = len(sampleShadedImageList)
		diffMIN = 99999.0
		whichIndex=-1
		for j in range(lengthSample):
			diff = rmsdiff_1997(queryShadedImageList[i], sampleShadedImageList[j])
			if diff < diffMIN:
				diffMIN = diff
				whichIndex = j
			print("index i = %d, index j = %d , DIFF = %f, DIFFMIN = %f\n" %(i,j,diff, diffMIN))
	
		if whichIndex != -1:
			del sampleShadedImageList[whichIndex]
			del sampleImageRectangleList[whichIndex]
	
	im9_contour = sampleContourImageList[0]
	
	im9_contour.paste(sampleShadedImageList[0].crop(sampleImageRectangleList[0]), sampleImageRectangleList[0])
	#im9_contour.show()
	
	im9 = im9_contour
	
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
