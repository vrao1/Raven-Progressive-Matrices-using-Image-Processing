from PIL import Image, ImageChops
import numpy as np
import operator
import math

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

def mainE05(problem):
	im1 = Image.open(problem.figures["A"].visualFilename)
	im2 = Image.open(problem.figures["B"].visualFilename)
	im3_ans = Image.open(problem.figures["C"].visualFilename)
	im4 = Image.open(problem.figures["D"].visualFilename)
	im5 = Image.open(problem.figures["E"].visualFilename)
	im6_ans = Image.open(problem.figures["F"].visualFilename)
	im7 = Image.open(problem.figures["G"].visualFilename)
	im8 = Image.open(problem.figures["H"].visualFilename)
	#im1_arr = np.asarray(im1)
	
	im1 = Image.open(problem.figures["H"].visualFilename)
	im2 = Image.open(problem.figures["H"].visualFilename)
	#print(list(im1_arr))
	im1 = im1.convert("L")
	im2 = im2.convert("L")
	data = im1.getdata()
	#print(type(data))
	
	data2 = im2.getdata()
	
	height, width = im1.size
	
	im1_arr = list(im1.getdata())
	image_new = list(im2.getdata())
	
	i = 0
	total_length = width * height
	new_image_arr = [0] * total_length
	
	while i < total_length:
		new_image_arr[i] = XNOR(im1_arr[i], image_new[i])
		i = i+1
	
	im3_new = Image.new(im1.mode, im1.size)
	im3_new.putdata(new_image_arr)
	im3_new_arr = list(im3_new.getdata())
	
	#To find Right Most and Left Most Black point
	
	X_MIN = 999999
	X_MAX = -1000
	Y_MIN = 999999
	Y_MAX = -1000
	
	for i in range(height):
		for j in range(width):
			stride = (width*i) + j 
			if im3_new_arr[stride] == 0:
				if X_MIN > j:
					X_MIN = j
				if X_MAX < j:
					X_MAX = j
	
				if Y_MIN > i:
					Y_MIN = i
				if Y_MAX < i:
					Y_MAX = i
	
	print("X_MIN = %d, X_MAX = %d\n" %(X_MIN, X_MAX))
	print("Y_MIN = %d, Y_MAX = %d\n" %(Y_MIN, Y_MAX))
	
	gapX = (width - (X_MAX - X_MIN))/2     # ->| gapX | Main Picture | gapX |<-
	offsetX = width - gapX - X_MAX
	
	gapY = (height - (Y_MAX - Y_MIN))/2     # ->| gapY | Main Picture | gapY |<-
	offsetY = height - gapY - Y_MAX
	
	print("offsetX = %d , gapX = %d\n" %(offsetX, gapX))
	print("offsetY = %d , gapY = %d\n" %(offsetY, gapY))

	offsetX = int(offsetX)	
	offsetY = int(offsetY)	

	im3_new = ImageChops.offset(im3_new, offsetX,offsetY)
	#im3_new.show()
	
	i = 1
	minDiff=99999999
	answer=0
	
	while i < 9:
		image_name = problem.figures[str(i)].visualFilename
		newImg = Image.open(image_name)
		newImg = newImg.convert("L")
		newDiff = rmsdiff_1997(im3_new, newImg)
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
