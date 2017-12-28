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

def mainCHD07(problem):

	listImage = []
	im1 = Image.open(problem.figures["A"].visualFilename)
	listImage.append(im1)
	im2 = Image.open(problem.figures["B"].visualFilename)
	listImage.append(im2)
	im3_ans = Image.open(problem.figures["C"].visualFilename)
	listImage.append(im3_ans)
	im4 = Image.open(problem.figures["D"].visualFilename)
	listImage.append(im4)
	im5 = Image.open(problem.figures["E"].visualFilename)
	listImage.append(im5)
	im6_ans = Image.open(problem.figures["F"].visualFilename)
	listImage.append(im6_ans)
	im7 = Image.open(problem.figures["G"].visualFilename)
	listImage.append(im7)
	im8 = Image.open(problem.figures["H"].visualFilename)
	#im1_arr = np.asarray(im1)
	listImage.append(im8)
	
	im1 = Image.open(problem.figures["G"].visualFilename)
	im2 = Image.open(problem.figures["H"].visualFilename)
	#print(list(im1_arr))
	im1 = im1.convert("L")
	im2 = im2.convert("L")
	data = im1.getdata()
	#print(type(data))
	
	data2 = im2.getdata()
	
	height, width = im1.size
	
	centerX = width / 2
	centerY = height / 2
	
	i = centerX
	# Find Circle Coordinates to crop it
	while i < width:
		stride = ((centerY-1)*width) + i 
		stride = int(stride)
		if data[stride] == 0:
			i = i + 1
		else:
			break
	
	radius = i-centerX-1
	
	upper = centerY - radius
	left = centerX - radius
	lower = centerY + radius
	right = centerX + radius
	
	rectangle = (int(left), int(upper),int(right), int(lower))
	
	im1_arr = list(im1.getdata())
	image_new = list(im2.getdata())
	
	i = 0
	total_length = width * height
	new_image_arr = [0] * total_length
	
	while i < total_length:
		new_image_arr[i] = XNOR(im1_arr[i], image_new[i])
		i = i+1
	
	croppedRect = im1.crop(rectangle)
	im3_new = Image.new(im1.mode, im1.size)
	
	im3_new.putdata(new_image_arr)
	im3_new.paste(croppedRect, rectangle)
	im3_new_arr = list(im3_new.getdata())
	flag = [True] * 8	
	#To find Right Most and Left Most Black point
	i = 1
	minDiff=99999999
	answer=0
	
	while i < 8:
		if flag[i] == False:
			i = i+1
			continue
		minDiff=99999999
		image_name = problem.figures[str(i)].visualFilename
		newImg = Image.open(image_name)
		newImg = newImg.convert("L")
		answer = -1
		j = 0
		for im3_new in listImage:
			im3_new = im3_new.convert("L")
			newDiff = rmsdiff_1997(im3_new, newImg)
			print("New Difference")
			print(newDiff)
			print("Min Difference")
			print(minDiff)
			if(minDiff > newDiff):
				minDiff = newDiff
				answer = j
			j = j+1
		if answer != -1 and minDiff<50:
			del listImage[answer]
			flag[i] = False
		i = i + 1
	
	for i in range(8):
		if flag[i] == True:
			return(i)
