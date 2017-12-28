import numpy as np

# Position of each object type in objectInTransit
# 1. fill = "no"
# 2. size = "very large"
# 3. shape = "square"
# 4. inside = "c" 
# 5. alignment = ""
# 6. angle = ""
# 7. above = ""
# 8. overlaps = ""

class FigureEquation:
	
	def __init__(self):
		self.attributesList = ["fill","size","shape","inside","alignment","angle","above","overlaps","height","left-of","width"]
		self.size = len(self.attributesList)

		# 2x2 This bit array sets if any of 8 attribute's value changes
		self.toggleStatus = np.zeros(self.size, dtype=np.int) # Initialize with zeros
		#for i in range(self.size):
		#	self.toggleStatus[i] = 0

		# 2x2 this is an array of dictionaries to store corresponding attribute's values if they change
		self.objectInTransit = [dict() for x in range(self.size)]
		
	def fillDict(self, whichPosition, key, val):
		if whichPosition < 0 or whichPosition >= self.size:
			print("Wrong Index Value")
			return

		# 2x2 this bit is set because the attribute's value is changing 
		self.toggleStatus[whichPosition] = 1

		# 2x2 Corresponding Dictionary is getting populated in case attribute's value changes
		#print("position = %d , key = %s , val = %s, toggleStatus[whichPosition] = %d\n" %(whichPosition, key, val, self.toggleStatus[whichPosition]))
		self.objectInTransit[whichPosition][key] = val # obj[1]["very large"] = "huge"

	def replicateDict(self, whichPosition, key, val):
		if whichPosition < 0 or whichPosition >= self.size:
			print("Wrong Index Value")
			return

		# 2x2 Bit is reset to 0 , since there is only replication of the transition
		self.toggleStatus[whichPosition] = 0
		self.objectInTransit[whichPosition][key] = val # obj[1]["very large"] = "huge"
