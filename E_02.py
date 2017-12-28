from PIL import Image, ImageChops
import numpy as np
import operator
import math

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

def mainE02(problem):
	im1 = Image.open(problem.figures["A"].visualFilename)
	im2 = Image.open(problem.figures["B"].visualFilename)
	im3_ans = Image.open(problem.figures["C"].visualFilename)
	im4 = Image.open(problem.figures["D"].visualFilename)
	im5 = Image.open(problem.figures["E"].visualFilename)
	im6_ans = Image.open(problem.figures["F"].visualFilename)
	im7 = Image.open(problem.figures["G"].visualFilename)
	im8 = Image.open(problem.figures["H"].visualFilename)
	#im1_arr = np.asarray(im1)
	
	#print(list(im1_arr))
	im1 = im1.convert("L")
	im2 = im2.convert("L")
	
	im3 = ImageChops.darker(im1, im2)
	im3_ans = im3_ans.convert("L")
	
	im4 = im4.convert("L")
	im5 = im5.convert("L")
	
	im6 = ImageChops.darker(im4, im5)
	im6_ans = im6_ans.convert("L")
	
	im7 = im7.convert("L")
	im8 = im8.convert("L")
	im9 = ImageChops.darker(im7, im8)
	
	#im9.show()
	#print(list(np.asarray(im1)))
	
	calculateDiff(im3, im3_ans)
	calculateDiff(im6, im6_ans)
	
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
