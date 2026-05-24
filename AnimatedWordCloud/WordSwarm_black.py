import sys, os, getopt
import random
import re
import subprocess

from .framework.framework import *
import pygame
from pygame.locals import *

from .wsWordObj import *
from .NGrams import *


class WordSwarm(Framework):
	# Settings
	name = ""
	show_title = True  # Show title by default
	saveFrames = True
	csvName = 'matrix.csv'
	saveFolder = './postprocessing/frames/'

	frameN = 0;
	shapes = [];
	fixtures = [];
	bodies = [];
	joints = [];
	wordObjs = []
	sun = []
	wordHue = (-1, -1)
	topN = sys.maxsize
	nFrames = 150  # Default number of frames per period

	# Size of words (m)
	maxSize = 2
	minSize = 0.1

	# Sun strength
	frequency = 0.1
	damping = 2

	def __init__(self, argv):

		# Initialize pygame/pybox2d framework/world
		super(WordSwarm, self).__init__()
		self.world.gravity = (0, 0);
		startDateStr = None
		endDateStr = None

		# Parse arguments
		try:
			opts, args = getopt.getopt(argv,
									   "hxst:i:d:m:c:b:e:n:f:", ["ifile="])
		except getopt.GetoptError:
			print
			'Invalid argument'
			print(argv)
			print('try:')
			print
			'wordSwarm.py -n <topN] -s -t <title> -i <inputfile> -d <outputFolder> -m <maxWordHeight> -c <HexHue1_HexHue2> -b <startDate YYYYMMDD> -e <endDate YYYYMMDD>'
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				print
				'wordSwarm.py -n <topN] -s -t <title> -i <inputfile> -d <outputFolder> -m <maxWordHeight> -c <HexHue1_HexHue2> -b <startDate YYYYMMDD> -e <endDate YYYYMMDD>'
				sys.exit()
			elif opt == '-x':
				self.show_title = False
				print('Title display disabled')
			elif opt in ("-i", "--ifile"):

				print('Reading csv: %s' % arg)
				self.csvName = arg

			elif opt in ("-d"):
				self.saveFrames = True
				self.saveFolder = arg
				print('Saving frames to %s' % self.saveFolder)

			elif opt in ("-s"):
				self.saveFrames = True
				print('Saving frames to %s' % self.saveFolder)

			elif opt in ("-t"):

				print('WordSwarm title: %s' % arg)
				self.name = arg

			elif opt in ("-m"):
				self.maxSize = int(arg)
				print('Max word height set to: %d' % self.maxSize)

			elif opt in ("-c"):
				self.wordHue = (int(arg[0:2], 16), int(arg[3:5], 16))
				print('Words will have hues %d or %d' % (self.wordHue[0], self.wordHue[1]))

			elif opt in ("-b"):
				startDateStr = arg
				print('Starting animation at %s' % startDateStr)

			elif opt in ("-e"):
				endDateStr = arg
				print('Ending animation on %s' % endDateStr)

			elif opt in ("-n"):
				self.topN = int(arg)
				print('Displaying only the first %d results in csv' % self.topN)

			elif opt in ("-f"):
				self.nFrames = int(arg)
				print('Number of frames per period set to: %d' % self.nFrames)

		# Create output directory if required
		if self.saveFrames:
			if not os.path.exists(self.saveFolder):
				os.makedirs(self.saveFolder)
			else:
				self.purge(self.saveFolder, '.*')

		# Create ngrams database
		self.nGrams = wsNGrams(self.csvName, startDateStr, endDateStr, self.topN)

		box_half_size = (0.5, 0.5)

		# Place word objects
		self.shapes = [None] * self.nGrams.nWords
		self.fixtures = [None] * self.nGrams.nWords
		self.bodies = [None] * self.nGrams.nWords
		self.joints = [None] * self.nGrams.nWords
		self.wordObjs = [None] * self.nGrams.nWords;
		for word_k in range(0, self.nGrams.nWords):

			# The centre of the universe
			self.sun.append(self.world.CreateStaticBody(
				position=b2Vec2(random.uniform(
					-45, 65), 0)));

			# Create word object
			if self.nGrams.areColors == 'hue':
				self.wordObjs[word_k] = wsWordObj(
					self.nGrams.words[word_k], [self.nGrams.colors[word_k]])
			elif self.nGrams.areColors == 'rgb':
				self.wordObjs[word_k] = wsWordObj(
					self.nGrams.words[word_k], self.nGrams.colors[word_k])
			else:
				self.wordObjs[word_k] = wsWordObj(
					self.nGrams.words[word_k], self.wordHue)

			# Create body for word
			self.bodies[word_k] = self.world.CreateDynamicBody(
				position=(random.uniform(-60, 70), random.uniform(-40, 40)))

			# Add fixture to body
			self.fixtures[word_k] = self.bodies[word_k].CreateFixture(
				b2FixtureDef(shape=b2PolygonShape(box=(
					box_half_size[0] / self.wordObjs[word_k].paddedAR, box_half_size[0]))))

			# Link word object to sun
			self.joints[word_k] = self.world.CreateJoint(
				b2DistanceJointDef(
					frequencyHz=self.frequency,
					dampingRatio=self.damping,
					bodyA=self.sun[word_k],
					bodyB=self.bodies[word_k],
					localAnchorA=(0, 0),
					localAnchorB=(0, 0),
					length=0.5))

	# Removes files from a directory matching a pattern
	def purge(self, dir, pattern):
		for f in os.listdir(dir):
			if re.search(pattern, f):
				os.remove(os.path.join(dir, f))

	# Converts a size in (m) to a size in (px)
	def convertWorld2Screen(self, size_m):

		# Generate faux coordinates in (m)
		coord_m1 = size_m
		coord_m2 = list(size_m)
		coord_m2[0] = -coord_m2[0]
		coord_m2[1] = -coord_m2[1]

		# Convert faux coordinates to (px)
		coord_px1 = self.renderer.to_screen(coord_m1)
		coord_px2 = self.renderer.to_screen(coord_m2)

		# Calculate size from new coordinates
		size_p = [abs(coord_px1[0] - coord_px2[0]),
				  abs(coord_px1[1] - coord_px2[1])]

		return size_p


	# @TODO Scale text and line weight with screen size
	def Draw_Date(self, date_k):
		color = (255, 255, 255)
		dateTxt = freetype.Font(None)
		dateTxt.size = 24
		dateTxt.fgcolor = color

		top = (int(self.screen.get_height() * 0.075), int(self.screen.get_height() * 0.125))
		bot = (int(self.screen.get_height() * 0.075), int(self.screen.get_height() * (1 - 0.125)))

		# Only draw title if show_title is True
		if self.show_title:
			self.screen.blit(dateTxt.render(self.name)[0],
							 (self.screen.get_height() * 0.03, self.screen.get_height() * 0.03))

		pygame.draw.line(self.screen, color, top, bot, 4)
		pygame.draw.line(self.screen, color, (top[0] - 4, top[1]), (top[0] + 4, top[1]), 4)
		pygame.draw.line(self.screen, color, (bot[0] - 4, bot[1]), (bot[0] + 4, bot[1]), 4)

		start_year = self.nGrams.dates[0].year
		end_year = self.nGrams.dates[-1].year

		progress = ((self.nGrams.dates[date_k].year - start_year) +
					(self.nGrams.dates[date_k].month / 12.0)) / (end_year - start_year + 1)

		pos = (top[0] + 1, int((bot[1] - top[1]) * progress + top[1]))
		pygame.draw.circle(self.screen, color, pos, 8)

		self.screen.blit(dateTxt.render('%d' % self.nGrams.dates[date_k].year)[0],
						 (pos[0] + 20, pos[1] - 10))


	def Step(self, settings):
		self.screen.fill((0, 0, 0))      #Black background
		self.frameN = self.frameN + 1;

		# Update ngram date every n-frames
		nFrames = self.nFrames

		date_k = int(self.frameN / nFrames) + 1  # Date moving towards
		phase = (self.frameN % nFrames) / float(nFrames)  # (0-1) way to new date

		# Stop if at the end of the dataset
		if date_k == self.nGrams.nDates:
			print('WordSwarm animation complete')
			print('Running ffmpeg to create video...')
			try:
				# Use title from self.name or default
				video_filename = self.name if self.name else 'wordSwarmOut'
				video_filename = video_filename + '.mp4'
				
				# Run ffmpeg directly with custom output filename
				subprocess.run([
					'ffmpeg\\bin\\ffmpeg.exe',
					'-y',
					'-framerate', '30',
					'-i', 'frames\\%d.png',
					'-c:v', 'libx264',
					'-profile:v', 'high',
					'-r', '30',
					'-pix_fmt', 'yuv420p',
					video_filename
				], cwd='postprocessing', shell=True, check=True)
				
				print('Video creation completed successfully!')
				print(f'Video saved to: postprocessing/{video_filename}')
			except subprocess.CalledProcessError as e:
				print(f'Error running ffmpeg: {e}')
			except Exception as e:
				print(f'Unexpected error: {e}')
			print('Hope you enjoyed the show!')
			raise SystemExit(0)

		dateTxt = freetype.Font(None)
		dateTxt.size = 10
		dateTxt.fgcolor = (255, 255, 255)

		self.Draw_Date(date_k)  # Draw the date

		# Update size of each word
		# @TODO There is a memory leak in creating the new bodies (it doesn't delete the old ones)
		for word_k in range(0, self.nGrams.nWords):

			# Calculate word sizes
			if phase == 1:
				newSize = (0, 0)

				newSize[1] = (self.maxSize - self.minSize) * (
							self.nGrams.counts[word_k][date_k - 1] / float(self.nGrams.maxCount)) + self.minSize

				newSize[0] = newSize[1] / self.wordObjs[word_k].paddedAR

				self.wordObjs[word_k].boxSize = self.convertWorld2Screen(newSize)
			else:
				newSize = list((0, 0))
				newSize[1] = (self.maxSize - self.minSize) * (
							self.nGrams.counts[word_k][date_k] / float(self.nGrams.maxCount)) + self.minSize
				newSize[0] = newSize[1] / self.wordObjs[word_k].paddedAR

				oldSize = list((0, 0))
				oldSize[1] = (self.maxSize - self.minSize) * (
							self.nGrams.counts[word_k][date_k - wsNGrams.nDates] / float(self.nGrams.maxCount)) + self.minSize
				oldSize[0] = oldSize[1] / self.wordObjs[word_k].paddedAR

				size = list((0, 0))
				size[0] = (newSize[0] - oldSize[0]) * phase + oldSize[0]
				size[1] = (newSize[1] - oldSize[1]) * phase + oldSize[1]

				self.wordObjs[word_k].boxSize = self.convertWorld2Screen(size)

			# Re-create fixture
			self.bodies[word_k].DestroyFixture(self.fixtures[word_k])
			self.fixtures[word_k] = None
			self.fixtures[word_k] = self.bodies[word_k].CreateFixture(
				b2FixtureDef(shape=b2PolygonShape(box=newSize)))

			# Redraw word in new shape
			pos = self.renderer.to_screen(self.bodies[word_k].position);
			self.wordObjs[word_k].Draw(self.screen, pos)

		# Save frames to create film
		if self.saveFrames:
			pygame.image.save(self.screen,
							  self.saveFolder + int(self.frameN).__format__('')
							  + '.png')

		Framework.Step(self, settings);
