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

image = cv.imread("result1.png")
# hsv=cv.cvtColor(image)

# # Define lower and uppper limits of what we call "brown"
# brown_lo=np.array([10,0,0])
# brown_hi=np.array([20,255,255])

# Mask image to only select browns
# color = [163,250,250]
# color2 = [248,248,248]

# # Change image to red where we found brown
# image[np.all(image == color, axis=-1)]=color2
# # image[np.all(image == [0,0,0], axis=-1)]=

# cv.imwrite("result1.png",image)
import numpy as np
	

def new_get_line(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	slope = (y1 - y2)/(x1 - x2)
	b = (x1*y2 - x2*y1)/(x1 - x2)
	r = (x1, x2) if x1<x2 else (x2, x1)
	line=[]
	for x in np.arange(r[0], r[1], 0.1):
		y = slope*x+b
		line.append((int(x),int(y)))
	print(line) 

p1 = 438, 9
p2 = 435, 100

print(new_get_line(p1, p2))
