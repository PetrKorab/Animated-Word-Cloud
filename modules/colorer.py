
import random
import colorsys

class wsColorer():
	
	hues = None
	rgb = None
	
	def __init__(self, hues):
	
		# Initialize two hues that all words will be coloured with
		self.hues = [-1, -1]
		
		if len(hues) == 1:
			self.hues[0] = hues[0]
			self.hues[1] = hues[0]
			return
		elif len(hues) == 3:
			self.rgb = hues
			return
		
		if hues[0] == -1:
			self.hues[0] = random.uniform(0,1)
		else:
			self.hues[0] = hues[0]/255.0
			
		if hues[1] == -1:
			self.hues[1] = random.uniform(0,1)
		else:
			self.hues[1] = hues[1]/255.0
		
	def getColor(self):
	
		if self.rgb == None:
			# Choose one of the two different hues, then select a
			#  saturation and a value that works well with the background
			#  color. Then convert to 0-255 RGB values
			hue = self.hues[random.randint(0,1)]
			sat = random.uniform(0.1,0.9)
			val = random.uniform(0.5,0.9)
		
			rgb = list(colorsys.hsv_to_rgb(hue, sat, val))
			rgb[0] = rgb[0] * 255
			rgb[1] = rgb[1] * 255
			rgb[2] = rgb[2] * 255
			
		else:
			rgb = self.rgb
		
		return rgb