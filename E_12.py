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

def mainE12(problem):
	im1 = Image.open(problem.figures["G"].visualFilename)
	im2 = Image.open(problem.figures["H"].visualFilename)

	im1 = im1.convert("L")
	im2 = im2.convert("L")
	im2 = im2.transpose(Image.FLIP_TOP_BOTTOM) 
	
	data = im1.getdata()
	data2 = list(im2.getdata())
	height, width = im1.size
	
	im3_new_arr = list(data)
	
	X_MIN, X_MAX, Y_MIN, Y_MAX = findExtrema(im3_new_arr,height,width)
	X_MIN_2, X_MAX_2, Y_MIN_2, Y_MAX_2 = findExtrema(data2,height,width)
	
	print("X_MIN = %d, X_MAX = %d\n" %(X_MIN, X_MAX))
	print("Y_MIN = %d, Y_MAX = %d\n" %(Y_MIN, Y_MAX))
	
	offsetX = X_MIN_2 - X_MIN
	
	total_length = height * width
	
	for i in range(height):
		offset = width*i
		for j in range(width):
			if data2[offset + j] == 0:
				data2[offset + j - offsetX] = 0
				data2[offset +j ] = 255
	
	third_arr = [0] * total_length
	for i in range(total_length):
		third_arr[i] = XNOR(im3_new_arr[i], data2[i])
	
	#Remove Noise from the final Image 
	for i in range(height):
		offset = width*i
		for j in range(width):
			if third_arr[offset + j] == 0:
				if third_arr[offset + j + width] == third_arr[offset + j - width]:
					third_arr[offset +j] = 255 
	
	X_MIN_3, X_MAX_3, Y_MIN_3, Y_MAX_3 = findExtrema(third_arr,height,width)
	
	gapX = (width - (X_MAX_3 - X_MIN_3))/2     # ->| gapX | Main Picture | gapX |<-
	offsetX = width - gapX - X_MAX_3
	
	im3_new = Image.new(im1.mode, im1.size, "white")
	im3_new.putdata(third_arr)

	offsetX = int(offsetX)
	
	im3_new = ImageChops.offset(im3_new, offsetX, 0)
	#im3_new.save("ilu.problem.figures["H"].visualFilename)
	
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
