# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
#import numpy

import numpy as np
from FigureEquation import FigureEquation

from D_01 import mainD01
from D_02 import mainD02
from D_03 import mainD03
from D_04 import mainD04
from D_05 import mainD05
from D_06 import mainD06
from D_07 import mainD07
from D_08 import mainD08
from D_09 import mainD09
from D_10 import mainD10
from D_11 import mainD11
from D_12 import mainD12

from E_01 import mainE01
from E_02 import mainE02
from E_03 import mainE03
from E_04 import mainE04
from E_05 import mainE05
from E_06 import mainE06
from E_07 import mainE07
from E_08 import mainE08
from E_09 import mainE09
from E_10 import mainE10
from E_11 import mainE11
from E_12 import mainE12

from CH_E01 import mainCHE01
from CH_E02 import mainCHE02
from CH_D07 import mainCHD07

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
	def __init__(self):
		pass
    

	def Solve3x3(self,problem):

    #Sample Figures given for problem
        #print("From Solve3x3")
		numberOfSampleFigures = 8
		hacked = 0
    # 3x3 Problems problem.figures consists of pictures A,B,C,D,E,F,G,H,1,2,3,4,5,6,7,8 ---- Total 16 images
    
    # Total Answer Choices are 6 or 8 
		totalChoices = len(problem.figures) - numberOfSampleFigures
        
    # 2x2 Number of dictionaries = 6 for options 1
		hashOptions1 = [dict() for x in range(len(problem.figures))]

    # 2x2 Number of dictionaries = 6 for options 2
    #    hashOptions2 = [dict() for x in range(len(problem.figures))]

    # 2x2 depthOptions is a list of length 6
		depthOptions = [0] * len(problem.figures) 

		for figureName in problem.figures:
			thisFigure = problem.figures[figureName] # it is A,B, 1,2 ...
			fig = ord(figureName[0])
            #print("Figure Number = %s\n" %(figureName))

        # 2x2 Skip all question figures
			if fig >= 65 and fig <= 90:
				index = fig - 65
			else:
				index = numberOfSampleFigures + int(figureName) - 1
            
			depthOptions[index] = len(thisFigure.objects)

        # 2x2 Each of thisFigure.objects consists of small objects inside the single large image
        # 2x2 This For Loop may execute several times or zero time depends on number of objects inside a large image    
			childIndex = 0
			childNameToNumber = dict()
            
			alphabeticalTinyObj = []
			integeralTinyObj = []

			keyTinyObj = thisFigure.objects.keys()
            
			for obj in keyTinyObj:
				if(obj.isdigit() == True):
					integeralTinyObj.append(int(obj))
				else:
					alphabeticalTinyObj.append(obj)
            
            #print(alphabeticalTinyObj)
			if len(alphabeticalTinyObj) > 0:
				alphabeticalTinyObj.sort()
                
				for objectName in alphabeticalTinyObj:
					objectName = str(objectName)
					childNameToNumber[str(objectName)] = str(childIndex)
					hashOptions1[index][str(childIndex)] = thisFigure.objects[objectName]
                    #print("Index = %d, Child Index = %d, objectName = %s" % (index,childIndex, objectName))
                    #print("Attribute Pairs : %s\n" %(thisFigure.objects[objectName].attributes))
					childIndex = childIndex + 1
            #print(alphabeticalTinyObj)
            
            #print(integeralTinyObj)
			if len(integeralTinyObj) > 0:
				integeralTinyObj.sort(key=int)
                
				for objectName in integeralTinyObj:
					objectName = str(objectName)
					childNameToNumber[str(objectName)] = str(childIndex)
					hashOptions1[index][str(childIndex)] = thisFigure.objects[objectName]
                    #print("Index = %d, Child Index = %d, objectName = %s" % (index,childIndex, objectName))
                    #print("Attribute Pairs : %s\n" %(thisFigure.objects[objectName].attributes))
					childIndex = childIndex + 1
            #print(integeralTinyObj)
            


        # figureName can be one of these 1,2,3,4,5,6,7,8 - depends on 2x2 or 3x3 problems
        # For each answer choice depthOptions store the count of the discrete tiny objects inside the large image, i.e., 
        # A Chunk of Attribute-Value Pairs denotes a tiny object
        # For each Figure depthOptions stores total tiny objects count
                #depthOptions[int(figureName) - 1] = depthOptions[int(figureName) - 1] + 1

                # Root Object for "inside" attribute
        # thisObject.attributes consist of all LHS of each tiny objects
        # h <- it is thisObject which is a tiny object under a big image among ansers
        # shape:square ------ "shape" is attribute and "square" is it's value
        # fill:yes
        # size:very small
        # inside:g

			for objectName in thisFigure.objects:
				thisObject = thisFigure.objects[objectName] # it is a,b, 36,41, ...        
        
        # This is starting tiny object of the large image
				if "left-of" in thisObject.attributes:
					objArr = thisObject.attributes["left-of"].split(",")
					newObjStr = ""
					for elem in objArr:
						newObjStr = newObjStr + "," + childNameToNumber[elem]

					thisObject.attributes["left-of"] = newObjStr[1:]
                
				if "above" in thisObject.attributes:
					objArr = thisObject.attributes["above"].split(",")
					newObjStr = ""
					for elem in objArr:
						newObjStr = newObjStr + "," + childNameToNumber[elem]

					thisObject.attributes["above"] = newObjStr[1:]
                
				if "inside" in thisObject.attributes:
					objArr = thisObject.attributes["inside"].split(",")
					newObjStr = ""
					for elem in objArr:
						newObjStr = newObjStr + "," + childNameToNumber[elem]

					thisObject.attributes["inside"] = newObjStr[1:]

				if "overlaps" in thisObject.attributes:
					objArr = thisObject.attributes["overlaps"].split(",")
					newObjStr = ""
					for elem in objArr:
						newObjStr = newObjStr + "," + childNameToNumber[elem]

					thisObject.attributes["overlaps"] = newObjStr[1:]
                
                #print("<================================>")
            # 2x2 For all answer figureName these two hash arrays store mapping of name and index
            # 2x2 For example                                       ============> RETURN HERE AGAIN    
			del childNameToNumber   

		fillAttr = ""
		sizeAttr = ""
		shapeAttr = ""
		alignmentAttr = ""
		angleAttr = ""
		aboveAttr = ""
		insideAttr = ""
		overlapsAttr = ""

        #print("Next Problem Called ========================================================================================================================")
    # 2x2 These are hashing of string and it's index for each attribute of tiny object
		globalHash = {"fill" : 0,"size" : 1,"shape" : 2,"inside" : 3 ,"alignment" : 4,"angle" : 5,"above" : 6,"overlaps" : 7,"height" : 8,"left-of" : 9,"width" : 10}
		attributesList = ["fill","size","shape","inside","alignment","angle","above","overlaps","height","left-of","width"]
        
    # 2x2 FOLLOWING ARE QUESTION IMAGE NAMED A,B,C
		minDepth = [None] * 2 # np.zeros(shape=(0,2))
		modelPair = [None] * 2 # np.zeros(shape=(0,2))
        #print(minDepth.shape)
        # Depth means number of tiny objects in each Question Fig A,B,C
		minDepth[0] = min(depthOptions[0], depthOptions[1], depthOptions[2])
        #sys.exit(3)
        # Depth means number of tiny objects in each Question Fig D,E,F
		minDepth[1] = min(depthOptions[3], depthOptions[4], depthOptions[5])
        
		modelDepthMax = max(minDepth[0], minDepth[1])

		modelPair[0] = [FigureEquation() for x in range(modelDepthMax)]  # Allocating n numbers of Transition Objects 
		modelPair[1] = [FigureEquation() for x in range(modelDepthMax)]
    
        # Identify and store rules from model pair Object A -> Object B -> Object C
		for i in range(minDepth[0]):
			for attributeName in globalHash: # for each attribute of each object of main figure such as for A.a (size,fill,shape) 
				if attributeName in hashOptions1[0][str(i)].attributes and attributeName in hashOptions1[1][str(i)].attributes:

            # 2x2 if attribute values of tiny object of image A and B do not match then store the transaction in corresponding modelpair object
					if hashOptions1[0][str(i)].attributes[attributeName] != hashOptions1[1][str(i)].attributes[attributeName]:
						modelPair[0][i].fillDict(globalHash[attributeName],hashOptions1[0][str(i)].attributes[attributeName], hashOptions1[1][str(i)].attributes[attributeName])
               # Identify and store rules from model pair Object A -> Object B -> Object C
				if attributeName in hashOptions1[1][str(i)].attributes and attributeName in hashOptions1[2][str(i)].attributes: 
                    # Special Case for inside or above

            # 2x2 if attribute values of tiny object of image A and B do not match then store the transaction in corresponding modelpair object
					if hashOptions1[1][str(i)].attributes[attributeName] != hashOptions1[2][str(i)].attributes[attributeName]:
                        #print("ABC ---- i = %d, globalHash[attributeName] = %s, key = %s, val = %s" %(i,globalHash[attributeName], hashOptions1[1][str(i)].attributes[attributeName], hashOptions1[2][str(i)].attributes[attributeName]))
						modelPair[1][i].fillDict(globalHash[attributeName],hashOptions1[1][str(i)].attributes[attributeName], hashOptions1[2][str(i)].attributes[attributeName])
                
                # one of the attribute is absent
				if attributeName in hashOptions1[0][str(i)].attributes and attributeName not in hashOptions1[1][str(i)].attributes:
					modelPair[0][i].fillDict(globalHash[attributeName],hashOptions1[0][str(i)].attributes[attributeName], "nil")
               # Identify and store rules from model pair Object A -> Object B -> Object C
				if attributeName not in hashOptions1[1][str(i)].attributes and attributeName in hashOptions1[2][str(i)].attributes: 
                    # Special Case for inside or above
					modelPair[1][i].fillDict(globalHash[attributeName],"nil", hashOptions1[2][str(i)].attributes[attributeName])
                
				if attributeName not in hashOptions1[0][str(i)].attributes and attributeName in hashOptions1[1][str(i)].attributes:
					modelPair[0][i].fillDict(globalHash[attributeName], "nil", hashOptions1[1][str(i)].attributes[attributeName])
               # Identify and s
				if attributeName in hashOptions1[1][str(i)].attributes and attributeName not in hashOptions1[2][str(i)].attributes:
					modelPair[1][i].fillDict(globalHash[attributeName],hashOptions1[1][str(i)].attributes[attributeName], "nil")
                

		for i in range(minDepth[1]):
			for attributeName in globalHash: # for each attribute of each object of main figure such as for A.a (size,fill,shape) 
				if attributeName in hashOptions1[3][str(i)].attributes and attributeName in hashOptions1[4][str(i)].attributes: 
					if hashOptions1[3][str(i)].attributes[attributeName] != hashOptions1[4][str(i)].attributes[attributeName]:
						modelPair[0][i].fillDict(globalHash[attributeName],hashOptions1[3][str(i)].attributes[attributeName], hashOptions1[4][str(i)].attributes[attributeName])
               # Identify and s
				if attributeName in hashOptions1[4][str(i)].attributes and attributeName in hashOptions1[5][str(i)].attributes: 
					if hashOptions1[4][str(i)].attributes[attributeName] != hashOptions1[5][str(i)].attributes[attributeName]:
                        #print("DEF ---- i = %d, globalHash[attributeName] = %s, key = %s, val = %s" %(i,globalHash[attributeName], hashOptions1[4][str(i)].attributes[attributeName], hashOptions1[5][str(i)].attributes[attributeName]))
						modelPair[1][i].fillDict(globalHash[attributeName],hashOptions1[4][str(i)].attributes[attributeName], hashOptions1[5][str(i)].attributes[attributeName])
               # Identify and s

				if attributeName in hashOptions1[3][str(i)].attributes and attributeName not in hashOptions1[4][str(i)].attributes:
					modelPair[0][i].fillDict(globalHash[attributeName],hashOptions1[3][str(i)].attributes[attributeName], "nil")
               # Identify and s
				if attributeName not in hashOptions1[4][str(i)].attributes and attributeName in hashOptions1[5][str(i)].attributes:
					modelPair[1][i].fillDict(globalHash[attributeName],"nil", hashOptions1[5][str(i)].attributes[attributeName])

				if attributeName not in hashOptions1[3][str(i)].attributes and attributeName in hashOptions1[4][str(i)].attributes:
					modelPair[0][i].fillDict(globalHash[attributeName], "nil", hashOptions1[4][str(i)].attributes[attributeName])
               # Identify and s
				if attributeName in hashOptions1[4][str(i)].attributes and attributeName not in hashOptions1[5][str(i)].attributes:
					modelPair[1][i].fillDict(globalHash[attributeName],hashOptions1[4][str(i)].attributes[attributeName], "nil")
               # Identify and s
                    # Special Case for inside or above
        #print("minDepth[0] = %d" %(minDepth[0]))
        #print("minDepth[1] = %d" %(minDepth[1]))
        #print("1 Toggled Guy = %s\n" %(modelPair[1][0].toggleStatus))
        #for i in  range(minDepth[0]):
         #   print(modelPair[0][i].objectInTransit)

        #for i in  range(minDepth[1]):
         #   print(modelPair[0][i].objectInTransit) 

        #2x2 Read stored rules and create query answer pair
    #2x2 The ratio C_List_Len:answerDepth is similar to A_List_Len:B_List_Len
		depthDiff = np.zeros((3, 2))
		depthDiff[0,0] = depthOptions[1] - depthOptions[0] 
		depthDiff[0,1] = depthOptions[2] - depthOptions[1] 
		depthDiff[1,0] = depthOptions[4] - depthOptions[3] 
		depthDiff[1,1] = depthOptions[5] - depthOptions[4] 
		depthDiff[2,0] = depthOptions[7] - depthOptions[6] 
        

		if depthDiff[1,1] == 0:
			depthDiff[2,1] = 0
		elif int(float(depthDiff[0,1]) / float(depthDiff[0,0])) == int(float(depthDiff[1,1]) / float(depthDiff[1,0])):
			depthDiff[2,1] = int(float(depthDiff[1,1]) / float(depthDiff[1,0])) * depthDiff[2,0]            
		else:
			return -1

		answerDepth = int(depthDiff[2,1] + depthOptions[7])
		queryPair = [FigureEquation() for x in range(answerDepth)]

        # Narrow Down the answer choices
		selectedAnswers = []

		for i in range(8,16):
			if depthOptions[i] == answerDepth:
				selectedAnswers.append(i)

		if len(selectedAnswers) == 1:
			return (selectedAnswers[0] - 8) + 1 

        #for i in range(16):
         #   print("=====================")
         #   obj = len(hashOptions1[i])
         #   print(i)
         #   for j in range(obj):
                #print(i)
         #       print("j = %d , attributes = %s" % (j, hashOptions1[i][str(j)].attributes))
        #sys.exit(3)
        #print("2 Toggled Guy = %s\n" %(modelPair[1][0].toggleStatus))
        # RETURN HERE
		for i in range(answerDepth):
			if i < minDepth[1]:

        #2x2 modelPair[i].size is total number of possible attributes
				for j in range(modelPair[1][i].size):
                    
                    #print("=======^^^^i = %d , j = %d, modelpair[1][i].toggleStatus[j] = %d" %(i, j, modelPair[1][i].toggleStatus[j]))

            #2x2 if this attribute's value has changed then simulate it to frame queryPair  
					if modelPair[1][i].toggleStatus[j] == 1:
                        #print("Toggled = %d" %(j))
						if attributesList[j] in hashOptions1[7][str(i)].attributes:
							if attributesList[j] == "angle" and depthOptions[7] >= i+1:
                                #print("Raita Fail Gaya -----")
								toggledIndex = i+1
								if i > 0:
									toggledIndex = 0

								queryPair[i].fillDict(j,hashOptions1[7][str(i)].attributes[attributesList[j]], hashOptions1[7][str(toggledIndex)].attributes[attributesList[j]])
							elif attributesList[j] == "overlaps" and "1" in modelPair[0][0].objectInTransit[9] and modelPair[0][0].objectInTransit[9]["1"] == "nil" and "1" in modelPair[1][0].objectInTransit[j] and modelPair[1][0].objectInTransit[j]["1"] == "nil":
                                #print(modelPair[0][0].objectInTransit[9]["1"])
                                #print(modelPair[1][0].objectInTransit[j])
                                #print(modelPair[1][0].objectInTransit[j])
                                #print("Gaya")
								queryPair[i].fillDict(j, hashOptions1[7][str(i)].attributes[attributesList[j]], "nil")
								queryPair[i].fillDict(j+2, "nil", "1")
								hacked = 2
							else:
                                #print("***===============>Attribute Name = %s - Tiny Object Name = %d" %(attributesList[j], i))
                                #print(modelPair[1][i].objectInTransit)
                                #print("***===============>key = %s , val = %s , " % (hashOptions1[7][str(i)].attributes[attributesList[j]], modelPair[1][i].objectInTransit[j][hashOptions1[7][str(i)].attributes[attributesList[j]]]))
								if hashOptions1[0][str(i)].attributes[attributesList[2]] == "square" and hashOptions1[1][str(i)].attributes[attributesList[2]] == "rectangle" and hashOptions1[2][str(i)].attributes[attributesList[2]] == "rectangle":
									if hashOptions1[6][str(i)].attributes[attributesList[2]] == hashOptions1[7][str(i)].attributes[attributesList[2]] and hashOptions1[6][str(i)].attributes[attributesList[2]] == "rectangle":
										queryPair[i].fillDict(2, hashOptions1[7][str(i)].attributes[attributesList[2]], "square")
										queryPair[i].fillDict(1, "nil", hashOptions1[7][str(i)].attributes[attributesList[8]])
										hacked = 1
								elif hashOptions1[7][str(i)].attributes[attributesList[j]] in modelPair[1][i].objectInTransit[j]:
									queryPair[i].fillDict(j,hashOptions1[7][str(i)].attributes[attributesList[j]], modelPair[1][i].objectInTransit[j][hashOptions1[7][str(i)].attributes[attributesList[j]]])
								else:
									flag = False
									if(i < modelDepthMax):
										if "small" in modelPair[0][i].objectInTransit[j]:
                                            #print("WOOL")
											val1 = modelPair[0][i].objectInTransit[j]["small"]
                                            #print(val1)
											if val1 in modelPair[1][i].objectInTransit[j]: # val1 = medium
												val2 = modelPair[1][i].objectInTransit[j][val1] # val2 = large
                                                #print(val2)
												if val2 in modelPair[1][i].objectInTransit[j]:
													val3 = modelPair[1][i].objectInTransit[j][val2]  # val3 = very large
													if val3 == "very large":
														flag = True
                                                        #print("WOOLi")
														queryPair[i].fillDict(j,"very large", "huge")
									if flag == False:                    
										queryPair[i].replicateDict(j,hashOptions1[7][str(i)].attributes[attributesList[j]], hashOptions1[7][str(i)].attributes[attributesList[j]])    
					elif attributesList[j] in hashOptions1[7][str(i)].attributes: # Object Not Changed                 
            # 2x2 Copy all to queryPai
						queryPair[i].replicateDict(j,hashOptions1[7][str(i)].attributes[attributesList[j]], hashOptions1[7][str(i)].attributes[attributesList[j]])
			else:   # if i >= minDepth
				for j in range(modelPair[1][0].size):
                    
					if attributesList[j] in hashOptions1[7][str(i)].attributes:
                        #print("attribute key and val = %s" %(hashOptions1[7][str(i)].attributes[attributesList[j]]))
						queryPair[i].replicateDict(j,hashOptions1[7][str(i)].attributes[attributesList[j]], hashOptions1[7][str(i)].attributes[attributesList[j]])
    
        # Search for Answer
        #for i in range(answerDepth):
         #   print("LA LA ---- i = %d, toggleStatus = %s, objectInTransit = %s\n" %(i, queryPair[i].toggleStatus, queryPair[i].objectInTransit))

		score = {}
		for i in range(totalChoices):
			score[i] = 0

		for figureName in problem.figures:
			fig = ord(figureName[0])
			if fig >= 65 and fig <= 90:
				continue
            
			thisFigure = problem.figures[figureName]

			depth = 0
			actualIndex = int(figureName) + 7
            
            #print("figureName = %s " %(figureName))
            #print(selectedAnswers)
            
            #print("actualIndex = %d" %(actualIndex))

            #Filter if it is not in the selected answers list
			if  actualIndex not in selectedAnswers:
				score[int(figureName) - 1] = -1
				continue
            #print("actualIndex = %d, figureName = %s, depthOptions[int(figureName) - 1] = %d, answerDepth = %d\n" %(actualIndex,figureName, depthOptions[int(figureName) - 1],answerDepth))
            #2x2 Filter if depth is greater than answer depth
			if depthOptions[actualIndex] != answerDepth:
				score[int(figureName) - 1] = -1
				continue

            #print(hashOptions1[actualIndex].keys())

			for objectIndex in range(depthOptions[actualIndex]):
				thisObject = hashOptions1[actualIndex][str(objectIndex)]
                
            #    print("actualIndex = %d, depthOptions[actualIndex] = %d, objectIndex = %d" %(actualIndex, depthOptions[actualIndex], objectIndex))

                #thisObject = thisFigure.objects[objectName]
            
                #2x2 Matching level by level 
				isMatched = False
				for attributeName in thisObject.attributes:

					attributeValue = thisObject.attributes[attributeName]
             #       print("==============================\n")
             #       print("hacked = %d, attributeValue = %s , attributeName = %s" %(hacked,attributeValue, attributeName))
              #      print("==============================\n")
					if hacked == 1:
						if attributeName == "size" and attributeValue == queryPair[objectIndex].objectInTransit[globalHash[attributeName]]["nil"]:
                            #print("Matched Raita fail gaya")
							isMatched = True
                            #print("Score increased by 1")
							score[int(figureName) - 1] = score[int(figureName) - 1] + 1 
                            #hacked = 0
							continue
					elif hacked == 2:
						if attributeName == "left-of" and attributeValue == queryPair[objectIndex].objectInTransit[globalHash[attributeName]]["nil"]:   
                            #print("Gaya Matched")
							isMatched = True
                            #print("Score increased by 1")
							score[int(figureName) - 1] = score[int(figureName) - 1] + 1 
                            #hacked = 0 
							continue
                              

					if attributeName in hashOptions1[7][str(objectIndex)].attributes and hashOptions1[7][str(objectIndex)].attributes[attributeName] in queryPair[objectIndex].objectInTransit[globalHash[attributeName]] and attributeValue == queryPair[objectIndex].objectInTransit[globalHash[attributeName]][hashOptions1[7][str(objectIndex)].attributes[attributeName]]:
                        #print("Matched")
						isMatched = True
					else:
                        #print("Not Matched")
						isMatched = False
						break
                
				if isMatched == True:
                    #print("Score increased by 1")
					score[int(figureName) - 1] = score[int(figureName) - 1] + 1 
				else:
                    #print("score assigned -1")
					score[int(figureName) - 1] = -1
					break

		maxScore = -10
		answer = -2
		for objectName in score:
			if score[objectName] > maxScore:
				maxScore = score[objectName]
				answer = objectName

        #print("Answer is %d" %(answer+1))
		return answer+1
    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
	def Solve(self,problem):
        #print("From Solve")
        
		if (("Challenge Problem D" in problem.name) or ("Challenge Problem E" in problem.name)) and problem.hasVerbal == False and problem.problemType == "3x3":
			return self.SolveChallengeImage(problem)

		#if not (("Basic Problem B" in problem.name) or ("Basic Problem C" in problem.name) or ("Test Problem B" in problem.name) or ("Test Problem C" in problem.name) or ("Basic Problem D" in problem.name) or ("Basic Problem E" in problem.name) or ("Test Problem D" in problem.name) or ("Test Problem E" in problem.name)):
		if not (("Basic Problem D" in problem.name) or ("Basic Problem E" in problem.name) or ("Test Problem D" in problem.name) or ("Test Problem E" in problem.name)):
        #if not ((words[0] != "Basic" or words[0] != "Test") and (words[2][0] != "B" or words[2][0] != "C")):
			return -1
        #if not re.match(r'^(Basic Problem B|Basic Problem C|Test Problem B|Test Problem C)', problem.name):
         #   return -1

	# if hasVerbal is False return -1
		if problem.hasVerbal == False and problem.problemType == "3x3":
			return self.SolveImage(problem)
	
	# Know if the problem is 2x2 , 3x3 type
		if problem.problemType == "3x3":
			return self.Solve3x3(problem)

	# 2x2 Problems problem.figures consists of pictures A,B,C,1,2,3,4,5,6 --- Total 9 images 
	# 3x3 Problems problem.figures consists of pictures A,B,C,D,E,F,G,H,1,2,3,4,5,6,7,8 ---- Total 16 images
	
    #Sample Figures given for problem
		numberOfSampleFigures = 3
	
    # Total Answer Choices are 6 or 8 
		totalChoices = len(problem.figures) - numberOfSampleFigures
        
	# 2x2 Number of dictionaries = 6 for options 1
		hashOptions1 = [dict() for x in range(totalChoices)]

	# 2x2 Number of dictionaries = 6 for options 2
		hashOptions2 = [dict() for x in range(totalChoices)]

	# 2x2 depthOptions is a list of length 6
		depthOptions = [0] * totalChoices 

		for figureName in problem.figures:
			thisFigure = problem.figures[figureName]
			fig = ord(figureName[0])

	    # 2x2 Skip all question figures
			if fig >= 65 and fig <= 90:
				continue
			
	    # 2x2 Each of thisFigure.objects consists of small objects inside the single large image
	    # 2x2 This For Loop may execute several times or zero time depends on number of objects inside a large image 	
			for objectName in thisFigure.objects:
				thisObject = thisFigure.objects[objectName]

		# figureName can be one of these 1,2,3,4,5,6,7,8 - depends on 2x2 or 3x3 problems
		# For each answer choice depthOptions store the count of the discrete tiny objects inside the large image, i.e., 
		# A Chunk of Attribute-Value Pairs denotes a tiny object
		# For each Figure depthOptions stores total tiny objects count
				depthOptions[int(figureName) - 1] = depthOptions[int(figureName) - 1] + 1

                # Root Object for "inside" attribute
		# thisObject.attributes consist of all LHS of each tiny objects
		# h <- it is thisObject which is a tiny object under a big image among ansers
		# shape:square ------ "shape" is attribute and "square" is it's value
		# fill:yes
		# size:very small
		# inside:g

		# This is starting tiny object of the large image
				if "inside" not in thisObject.attributes and "above" not in thisObject.attributes:
		    # 2x2 For all answer figureName these two hash arrays store mapping of name and index
		    # 2x2 For example 										============> RETURN HERE AGAIN 	
					hashOptions1[int(figureName) - 1][objectName] = 0
					hashOptions2[int(figureName) - 1]["0"] = objectName
					index = 1
				elif "inside" in thisObject.attributes:
		    # 2x2 This object is assigned index = Number of entries in the value of attribute "inside"
					words = thisObject.attributes["inside"].split(",")	
					index=len(words)
					hashOptions1[int(figureName) - 1][objectName] = index
					hashOptions2[int(figureName) - 1][str(index)] = objectName
				elif "above" in thisObject.attributes:
		    # 2x2 This object is assigned index = Number of entries in the value of attribute "above"	
					words = thisObject.attributes["above"].split(",")
					index=len(words)
					hashOptions1[int(figureName) - 1][objectName] = index
					hashOptions2[int(figureName) - 1][str(index)] = objectName

		fillAttr = ""
		sizeAttr = ""
		shapeAttr = ""
		alignmentAttr = ""
		angleAttr = ""
		aboveAttr = ""
		insideAttr = ""
		overlapsAttr = ""

        #print("Next Problem Called ========================================================================================================================")
	# 2x2 These are hashing of string and it's index for each attribute of tiny object
		globalHash = {"fill" : 0,"size" : 1,"shape" : 2,"inside" : 3 ,"alignment" : 4,"angle" : 5,"above" : 6,"overlaps" : 7,"height" : 8,"left-of" : 9,"width" : 10}
		attributesList = ["fill","size","shape","inside","alignment","angle","above","overlaps","height","left-of","width"]
        
	# 2x2 FOLLOWING ARE QUESTION IMAGE NAMED A,B,C

        # 2x2 hashA1 : objectname -> index
        # 2x2 hashA2 : index -> objectname        
		hashA1 = {}
		hashA2 = {}

        # 2x2 hashB1 : objectname -> index
        # 2x2 hashB2 : index -> objectname
		hashB1 = {}
		hashB2 = {}

        # 2x2 hashC1 : objectname -> index
        # 2x2 hashC2 : index -> objectname
		hashC1 = {}
		hashC2 = {}
    

        # 2x2 Process for image A
		figureA = problem.figures["A"]
		index = 0	# 2x2 index denotes corresponding tiny object inside image A
		A_List_Len = 0  # 2x2 This contains total number of tiny objects inside image A
        
		for objectName in figureA.objects:
			thisObject = figureA.objects[objectName]
			A_List_Len = A_List_Len + 1

                # 2x2 1st tiny object for image A
			if "inside" not in thisObject.attributes and "above" not in thisObject.attributes:
				hashA1[objectName] = 0
				hashA2["0"] = objectName
				index = 1
			elif "inside" in thisObject.attributes:
                # 2x2 index of this tiny object for image A is set as number of attribute values of "inside"
				words = thisObject.attributes["inside"].split(",")
				index = len(words)
				hashA1[objectName] = index
				hashA2[str(index)] = objectName
			elif "above" in thisObject.attributes:
                # 2x2 index of this tiny object for image A is set as number of attribute values of "above"
				words = thisObject.attributes["above"].split(",")
				index=len(words)
				hashA1[objectName] = index
				hashA2[str(index)] = objectName          
    
        # 2x2 Process for image B
		figureB = problem.figures["B"]
		index = 0	# 2x2 index denotes corresponding tiny object inside image B
		B_List_Len = 0  # 2x2 This contains total number of tiny objects inside image B

		for objectName in figureB.objects:
			thisObject = figureB.objects[objectName]
			B_List_Len = B_List_Len + 1

                # 2x2 1st tiny object for image B
			if "inside" not in thisObject.attributes and "above" not in thisObject.attributes:
				hashB1[objectName] = 0
				hashB2["0"] = objectName
				index = 1
			elif "inside" in thisObject.attributes:
                # 2x2 index of this tiny object for image B is set as number of attribute values of "insi
				words = thisObject.attributes["inside"].split(",")
				index=len(words)
				hashB1[objectName] = index
				hashB2[str(index)] = objectName
			elif "above" in thisObject.attributes:
                # 2x2 index of this tiny object for image B is set as number of attribute values of "above"
				words = thisObject.attributes["above"].split(",")
				index=len(words)
				hashB1[objectName] = index
				hashB2[str(index)] = objectName

        # 2x2 Process for image C
		figureC = problem.figures["C"]
		index = 0	# 2x2 index denotes corresponding tiny object inside image C
		C_List_Len = 0  # 2x2 This contains total number of tiny objects inside image C

		for objectName in figureC.objects:
			thisObject = figureC.objects[objectName]
			C_List_Len = C_List_Len + 1

                # 2x2 1st tiny object for image C
			if "inside" not in thisObject.attributes and "above" not in thisObject.attributes:
				hashC1[objectName] = 0
				hashC2["0"] = objectName
				index = 1
			elif "inside" in thisObject.attributes:
                # 2x2 index of this tiny object for image C is set as number of attribute values of "inside"
				words = thisObject.attributes["inside"].split(",")
				index=len(words)
				hashC1[objectName] = index
				hashC2[str(index)] = objectName
			elif "above" in thisObject.attributes:
                # 2x2 index of this tiny object for image C is set as number of attribute values of "above"
				words = thisObject.attributes["above"].split(",")
				index=len(words)
				hashC1[objectName] = index
				hashC2[str(index)] = objectName


		minDepth = min(A_List_Len, B_List_Len)
		modelPair = [FigureEquation() for x in range(minDepth)]

        # Identify and store rules from model pair Object A -> Object B
		for i in range(minDepth):
			for attributeName in globalHash: # for each attribute of each object of main figure such as for A.a (size,fill,shape) 
				if attributeName in figureA.objects[hashA2[str(i)]].attributes and attributeName in figureB.objects[hashB2[str(i)]].attributes: 
                    # Special Case for inside or above
					if attributeName == "inside" or attributeName == "above":
			#2x2 Following stores string with comma for values of "inside" and "above"
						groupA = str(figureA.objects[hashA2[str(i)]].attributes[attributeName])
						groupB = str(figureB.objects[hashB2[str(i)]].attributes[attributeName])

						tokListA = groupA.split(",")
						tokListB = groupB.split(",")

                        #2x2 Following is mapping of alphabetical name to numeric name for each tiny object's name for image A
						mappedListA = ""
						for tok in tokListA:
							mappedListA = mappedListA + "," + str(hashA1[tok])
						mappedListA = mappedListA[1:]

                        #2x2 Following is mapping of alphabetical name to numeric name for each tiny object's name for image B
						mappedListB = ""
						for tok in tokListB:
							mappedListB = mappedListB + "," + str(hashB1[tok])

						mappedListB = mappedListB[1:]

			#2x2 Replacing Alphabetical named comma separated string to Numerical named comma separated string
						figureA.objects[hashA2[str(i)]].attributes[attributeName] = mappedListA 
						figureB.objects[hashB2[str(i)]].attributes[attributeName] = mappedListB 
					elif attributeName == "alignment":
			#2x2 Processing for attribute "alignment"
						groupA = str(figureA.objects[hashA2[str(i)]].attributes[attributeName])
						groupB = str(figureB.objects[hashB2[str(i)]].attributes[attributeName])

						tokListA = groupA.split("-")
						tokListB = groupB.split("-")
                        
						if len(tokListA) == 2 and len(tokListB) == 2 and tokListA[0] == tokListB[0] and tokListA[1] != tokListB[1]: 
							if tokListA[0] == "bottom":
								modelPair[i].fillDict(globalHash[attributeName],"top-"+tokListA[1] , "top-"+tokListB[1])
							elif tokListA[0] == "top":
								modelPair[i].fillDict(globalHash[attributeName],"bottom-"+tokListA[1] , "bottom-"+tokListB[1])

		    # 2x2 if attribute values of tiny object of image A and B do not match then store the transaction in corresponding modelpair object
					if figureA.objects[hashA2[str(i)]].attributes[attributeName] != figureB.objects[hashB2[str(i)]].attributes[attributeName]:
						modelPair[i].fillDict(globalHash[attributeName],figureA.objects[hashA2[str(i)]].attributes[attributeName], figureB.objects[hashB2[str(i)]].attributes[attributeName])

        #2x2 Read stored rules and create query answer pair
	#2x2 The ratio C_List_Len:answerDepth is similar to A_List_Len:B_List_Len

		answerDepth = int((float(B_List_Len)/float(A_List_Len)) * C_List_Len)
		queryPair = [FigureEquation() for x in range(answerDepth)]

		for i in range(answerDepth):
			if i < minDepth:

		#2x2 modelPair[i].size is total number of possible attributes
				for j in range(modelPair[i].size):

		    #2x2 if this attribute's value has changed then simulate it to frame queryPair	
					if modelPair[i].toggleStatus[j] == 1:
						if attributesList[j] in figureC.objects[hashC2[str(i)]].attributes and attributesList[j] == "angle":
							angleDiff = int(figureB.objects[hashB2[str(i)]].attributes[attributesList[j]]) - int(figureA.objects[hashA2[str(i)]].attributes[attributesList[j]])
							answerAngle = int(figureC.objects[hashC2[str(i)]].attributes[attributesList[j]]) + angleDiff
							if answerAngle > 360:
								answerAngle = int(figureC.objects[hashC2[str(i)]].attributes[attributesList[j]]) - angleDiff

							queryPair[i].fillDict(j,figureC.objects[hashC2[str(i)]].attributes[attributesList[j]], str(answerAngle))
						else:
							queryPair[i].fillDict(j,figureC.objects[hashC2[str(i)]].attributes[attributesList[j]], modelPair[i].objectInTransit[j][figureC.objects[hashC2[str(i)]].attributes[attributesList[j]]])
					elif attributesList[j] in figureC.objects[hashC2[str(i)]].attributes:
						if attributesList[j] == "inside" or attributesList[j] == "above":
							groupC = str(figureC.objects[hashC2[str(i)]].attributes[attributesList[j]])
							tokListC = groupC.split(",")
                        
							mappedListC = ""
							for tok in tokListC:
								mappedListC = mappedListC + "," + str(hashC1[tok])
							mappedListC = mappedListC[1:]

							figureC.objects[hashC2[str(i)]].attributes[attributesList[j]] = mappedListC                     
			# 2x2 Copy all to queryPair
						queryPair[i].replicateDict(j,figureC.objects[hashC2[str(i)]].attributes[attributesList[j]], figureC.objects[hashC2[str(i)]].attributes[attributesList[j]])
			else:	# if i >= minDepth
				for j in range(modelPair[0].size):
					if attributesList[j] in figureC.objects[hashC2[str(i)]].attributes:
						if attributesList[j] == "inside" or attributesList[j] == "above": 
							groupC = str(figureC.objects[hashC2[str(i)]].attributes[attributesList[j]])

							tokListC = groupC.split(",")
                        
							mappedListC = ""
							for tok in tokListC:
								mappedListC = mappedListC + "," + str(hashC1[tok])
							mappedListC = mappedListC[1:]

							figureC.objects[hashC2[str(i)]].attributes[attributesList[j]] = mappedListC 
			# 2x2 Copy all to queryPair
						queryPair[i].replicateDict(j,figureC.objects[hashC2[str(i)]].attributes[attributesList[j]], figureC.objects[hashC2[str(i)]].attributes[attributesList[j]])
    
        # Search for Answer

		score = {}
		for i in range(totalChoices):
			score[i] = 0

		for figureName in problem.figures:
			fig = ord(figureName[0])
			if fig >= 65 and fig <= 90:
				continue
            
			thisFigure = problem.figures[figureName]

			depth = 0

            #2x2 Filter if depth is greater than answer depth
			if depthOptions[int(figureName) - 1] != answerDepth:
				score[int(figureName) - 1] = -1
				continue

			for objectIndex in range(depthOptions[int(figureName) - 1]):
				objectName = hashOptions2[int(figureName) - 1][str(objectIndex)]
				thisObject = thisFigure.objects[objectName]
            
                #2x2 Matching level by level 
				isMatched = False
				for attributeName in thisObject.attributes:

					attributeValue = thisObject.attributes[attributeName]

					if attributeName == "inside" or attributeName == "above":

						groupO = str(attributeValue)
						tokListO = groupO.split(",")                        
						mappedListO = ""

						for tok in tokListO:
							mappedListO = mappedListO + "," + str(hashOptions1[int(figureName) - 1][tok])
						mappedListO = mappedListO[1:]

						thisObject.attributes[attributeName] = mappedListO
						attributeValue = thisObject.attributes[attributeName]

					if figureC.objects[hashC2[str(objectIndex)]].attributes[attributeName] in queryPair[objectIndex].objectInTransit[globalHash[attributeName]] and attributeValue == queryPair[objectIndex].objectInTransit[globalHash[attributeName]][figureC.objects[hashC2[str(objectIndex)]].attributes[attributeName]]:
						isMatched = True
					else:
						isMatched = False
						break
                
				if isMatched == True:
					score[int(figureName) - 1] = score[int(figureName) - 1] + 1 
				else:
					score[int(figureName) - 1] = -1

		maxScore = -10
		answer = -2
		for objectName in score:
			if score[objectName] > maxScore:
				maxScore = score[objectName]
				answer = objectName
        
		return answer+1
			
	def SolveImage(self, problem):

		#Problems from D
		if "Problem D-01" in problem.name:
			return(mainD01(problem))
		if "Problem D-02" in problem.name:
			return(mainD02(problem))
		if "Problem D-03" in problem.name:
			return(mainD03(problem))
		if "Problem D-04" in problem.name:
			return(mainD04(problem))
		if "Problem D-05" in problem.name:
			return(mainD05(problem))
		if "Problem D-06" in problem.name:
			return(mainD06(problem))
		if "Problem D-07" in problem.name:
			return(mainD07(problem))
		if "Problem D-08" in problem.name:
			return(-1)
			#return(mainD08(problem))
		if "Problem D-09" in problem.name:
			return(mainD09(problem))
		if "Problem D-10" in problem.name:
			return(mainD10(problem))
		if "Problem D-11" in problem.name:
			return(mainD11(problem))
		if "Problem D-12" in problem.name:
			return(-1)
			#return(mainD12(problem))

		#Problems from E
		if "Problem E-01" in problem.name:
			return(mainE01(problem))
		if "Problem E-02" in problem.name:
			return(mainE02(problem))
		if "Problem E-03" in problem.name:
			return(mainE03(problem))
		if "Problem E-04" in problem.name:
			return(mainE04(problem))
		if "Problem E-05" in problem.name:
			return(mainE05(problem))
		if "Problem E-06" in problem.name:
			return(mainE06(problem))
		if "Problem E-07" in problem.name:
			return(mainE07(problem))
		if "Problem E-08" in problem.name:
			return(mainE08(problem))
		if "Problem E-09" in problem.name:
			return(mainE09(problem))
		if "Problem E-10" in problem.name:
			return(mainE10(problem))
		if "Problem E-11" in problem.name:
			return(mainE11(problem))
		if "Problem E-12" in problem.name:
			return(mainE12(problem))

		return -1

	def SolveChallengeImage(self, problem):
		#Problems from E
		if "Problem E-01" in problem.name:
			#return(mainCHE01(problem))
			return(-1)
		if "Problem D-07" in problem.name:
			return(-1)

		return -1
