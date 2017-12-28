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

	print(h)
	summation = 0
	denominator = float(im1.size[0]) * im1.size[1]

	# calculate rms
	for i in range(256):	
		summation += h[i]*(i**2)

	quotient = summation/denominator
	print(quotient)

	#val = reduce(operator.add,map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1])

	#print(val)

	#val = math.sqrt(reduce(operator.add,map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
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

"""	
im1 = Image.open("A.png")
im2 = Image.open("B.png")
im3 = Image.open("C.png")
im1 = im1.convert("L")
im2 = im2.convert("L")
im3 = im3.convert("L")

diff_1_2 = rmsdiff_1997(im1,im2)
diff_2_3 = rmsdiff_1997(im2,im3)

im4 = Image.open("D.png")
im5 = Image.open("E.png")
im6 = Image.open("F.png")
im4 = im4.convert("L")
im5 = im5.convert("L")
im6 = im6.convert("L")

diff_4_5 = rmsdiff_1997(im4,im5)
diff_5_6 = rmsdiff_1997(im5,im6)

im7 = Image.open("G.png")
im8 = Image.open("H.png")
im7 = im7.convert("L")
im8 = im8.convert("L")

diff_7_8 = rmsdiff_1997(im7,im8)
"""

def mainD01(problem):
	i = 1
	minDiff=99999999
	answer=0
	sampleFile = problem.figures["H"].visualFilename


	im8 = Image.open(sampleFile)
	im8 = im8.convert("L")

	while i < 9:
		image_name = problem.figures[str(i)].visualFilename
		newImg = Image.open(image_name)
		newImg = newImg.convert("L")
		newDiff = rmsdiff_1997(im8, newImg)
		print("New Difference")
		print(newDiff)
		print("Min Difference")
		print(minDiff)
		if(minDiff > newDiff):
			minDiff = newDiff
			answer = i
	#newImg.show()
		i = i + 1

	return answer	
