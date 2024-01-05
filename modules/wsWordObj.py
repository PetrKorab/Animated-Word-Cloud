import sys
import pygame                     # The PyGame 'sub-framework'
from .colorer import *            # Module for generating word colours
import sys
sys.path.append('./framework/')
from .framework import *
from pygame.locals import * # Some parts of the PyGame framework to import locally


try: # Try to import advanced freetype font module 
    import pygame.freetype as freetype
except ImportError:
    print ("No FreeType support compiled")
    sys.exit ()

class wsWordObj(freetype.Font):

	padding = 30; # The number of pixels around the text of the word YEARLY
			# to give a little better visual clash protection
	#@TODO Create an option for this that can be import from a
	#	settings file and to scale with screen size.

	

	def __init__(self, string, hues):
		super(wsWordObj, self).__init__(None)
	
		self.colorer = wsColorer(hues) # Initialize the colourer
	
		self.string = string # Assign the string
		
		# Determine aspect ratio using a big size 
		#  to avoid rounding errors
		self.size = 100 
		self.fgcolor = list(self.colorer.getColor())
		self.render = self.render(self.string)[0]		
		
		# Calculate aspect ratio of textbox with padding
		self.boxSize = self.get_rect(self.string)[2:4] # Box size (px)
		self.paddedAR = (self.boxSize[1] + self.padding) / (float(self.boxSize[0]  + self.padding))
		self.paddedWScale = (self.boxSize[0] - self.padding) / float(self.boxSize[0])
		self.paddedHScale = (self.boxSize[1] - self.padding) / float(self.boxSize[1])
		
	def Draw(self, screen, pos):
	
		# Draw the word in a box of width of newSize(x,y) (px)	
		newSize = list((0,0))
		newSize[0] = int(self.boxSize[0] * self.paddedWScale)
		newSize[1] = int(self.boxSize[1] * self.paddedHScale) 
		scaledRender = pygame.transform.smoothscale(self.render, newSize)
		pos = list(pos)
		pos[0] = pos[0] - (newSize[0] / 2)
		pos[1] = pos[1] - (newSize[1] / 2)			
		screen.blit(scaledRender, pos)
