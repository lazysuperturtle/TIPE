# class Path:
# 	def __init__(self, road, direction):
# 		self._road = road
# 		self._direction = direction
# 		self.cars = []
# class Road:
# 	def __init__(self):
# 		self._start = None
# 		self._stop = None
# 		self.paths = [ Path(self, 1), Path(self, -1) ] # Modele simplifie avec des routes a deux bandes
# 	def get_weight(self):
# 		return p.get_path_w() for p in self.paths
# class Map:
# 	def __init__(self, n_cars, *args):
# 		self.n_cars = n_cars
import cv2 as cv
import numpy as np

image = cv.imread("gray.png")
hsv=cv.cvtColor(image,cv.COLOR_BGR2HSV)

# # Define lower and uppper limits of what we call "brown"
# brown_lo=np.array([10,0,0])
# brown_hi=np.array([20,255,255])

# Mask image to only select browns
color = [230,230,230]
color2 = [47,47,47]

# Change image to red where we found brown
image[np.all(image == color, axis=-1)]=(0,0,0)
image[np.all(image == [0,0,0], axis=-1)]=(0,0,0)

cv.imwrite("result.png",image)
	


