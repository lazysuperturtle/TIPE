from collections import defaultdict, namedtuple
from pprint import pprint
from matplotlib import pyplot as plt
from collections import defaultdict
from math import sqrt
import tkinter as tkt
import random as rnd
import numpy as np
import cv2 as cv
import json
import time

#test another neighbor function
from sklearn.neighbors import NearestNeighbors



#VARS
V_LENGTH = 5
V_WIDTH = 5
SEC_INT = 3



class Node:

	def __init__(self, coord):
		self.coords = coord
		self.x, self.y = coord


	def __str__(self):
		return "Node(%s,%s)" % (self.x, self.y,)

class Road:

	def __init__(self, origin, destination):
		self._capacity = self._calc_road_capacity()
		self._right_path = []
		self._left_path = []
		self.o_node = origin
		self.d_node = destination

	def __str__(self):
		return "%s -> %s" % (self.o_node, self.d_node) 

	def _calc_road_capacity(self): pass


class RoadMap:

	def __init__(self, connections):
		self._conns = defaultdict(set)
		self._create_connections(connections)

	def __str__(self):
		data = defaultdict(set)
		for x in self._conns.keys():
			data[str(x)] = {str(y) for y in self._conns[x]}  

		return str(data)

	def _create_connections(self, conns):
		for o_node, d_node in conns:
			n1 = Node(o_node)
			n2 = Node(d_node)
			self.add(n1, n2)

	def contains(self, coord):
		node = coord
		if node in self._conns.keys():
			return True

	def get_nodes(self):
		return self._conns.keys()

	def add(self, onode, d_node):
		g1 = Road(onode, d_node)
		g2 = Road(d_node, onode)
		self._conns[onode].add(g1) #revoir s'il faut pas changer de forme
		self._conns[d_node].add(g2)




class Traffic:

	Vehicle = namedtuple("Vehicle", ("x", "y", "velocity"))


	def __init__(self, gui, road_map):
		self._road_map = road_map
		self._nodes = self._road_map.get_nodes()
		self._vehicles = []

	def generate_vehicle(self, coord=None):
		if self._road_map.contains(coord):
			start_coord = coord
		else:
			start_coord = rd.choice(self._nodes)
		finish_coord = rd.choice([node for node in self._nodes if node != start_coord])
		direction = random.choice([-1, 1])


#Basculer vers matplotlib car animation plus belles

		self._coords = coord
		self.x, self.y = coord



class Image(tkt.Frame):

	def __init__(self, tk, file):
		super().__init__(tk)

		#AFFICHAGE
		self.file = file
		self.canvas = tkt.Canvas(self, width=800, height=800) 
		self.img = tkt.PhotoImage(file="map.png")
		self.canvas.create_image(0, 0, anchor=tkt.NW, image=self.img)
		self.bttn = tkt.Button(self, text="Save", command=self.save)
		# self.bttn.pack() #ne pas afficher ces buttons pendant la presentation TIPE
		self.file = file
		self.canvas = tkt.Canvas(self, width=800, height=800)

		self.img = tkt.PhotoImage(file="map.png")
		self.canvas.create_image(0, 0, anchor=tkt.NW, image=self.img)
		self.bttn = tkt.Button(self, text="Save", command=self.save)
		self.bttn.pack()
		# self.bttn1 = tkt.Button(self, text="Test", command=self.test)
		# self.bttn1.pack()
		self.bttn2 = tkt.Button(self, text="Restore", command=self.restore)
		self.bttn2.pack()
		self.bttn3 = tkt.Button(self, text="Connect", command=self.k_neigh)
		self.bttn3.pack()
		self.coords = []
		self.graph_coords = []
		self.circles = []
		self.canvas.bind("<Button-1>", self.get_coords)
		# self.canvas.bind("<Button-3>", self.deletec)
		self.canvas.pack()
		self.pack()

		#ANALYSE IMAGE
		self.image = cv.imread(self.file)
		roads = [248, 248, 248] #couleur de pixel routes
		y, x = np.where(np.all(self.image!=roads, axis=2))
		self.restricted_zones = list(zip(x,y))
		

		#PARTIE TRAFFIC
		# self._traffic_init()

		# afficher les zones interdites au passage, ne pas utiliser car prend trop de temps
		self.circles = []
		self.canvas.bind("<Button-1>", self.get_coords)
		# self.canvas.bind("<Button-3>", self.deletec)

		self.canvas.pack()
		self.pack()

		self.image = cv.imread(self.file)
		roads = [248, 248, 248]

		y, x = np.where(np.all(self.image!=roads, axis=2))
		self.restricted_zones = list(zip(x,y))
		
		roads = [248, 248, 248]

		y, x = np.where(np.all(self.image!=roads, axis=2))
		self.restricted_zones = list(zip(x,y))
		
		# r=1
		# for x, y in self.restricted_zones:
		# 	self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')	


	def _traffic_init(self):
		self.road_map = RoadMap(self.graph_coords)
		self.traffic_listener = Traffic(self, self.road_map)

	def save(self):
		with open("data1.json", "w") as jfile:
			data = json.dumps(self.coords)
			jfile.write(data)
		print("Saved")

		print("Saved")


	def draw(self):
		data = self.coords.copy()
		data.sort()
		for i in range(1, len(data)):
			c1, c2 = data[i-1], data[i]
			self.canvas.create_line(c1[0], c1[1], c2[0], c2[1], fill='red', width=2)

	def restore(self):
		with open("data1.json", "r") as jfile:
			file_data = jfile.readlines()
			data = json.loads(file_data[0])
			self.coords = data
			r=3
			data.sort()
			for coord in data:
				x, y = coord
				self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')

		# with open("lines_data.json", "r") as lines_file:
		# 	try:
		# 		file_data = lines_file.readlines()
		# 		if len(file_data) != 0:	
		# 			data = json.loads(file_data[0])
		# 			self.graph_coords = data
		# 			for c1, c2 in data:
		# 				line=self.canvas.create_line(c1[0], c1[1], c2[0], c2[1], fill='red', width=3)
		# 	except:
		# 		pass

		self._traffic_init()
		pprint(str(self.road_map))


	def undo(self):
		if len(self.circles)>0:
			circle = self.circles.pop()
			self.canvas.delete(circle)
			self.coords.pop()

	def get_coords(self, event):
		x, y = event.x, event.y
		self.coords.append((x, y))
		r = 3
		circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')
		self.circles.append(circle)

	def deletec(self, event):
		x, y = event.x, event.y
		x1, y1 = x+5, y+5
		x2, y2 = x-5, y-5
		ev_coords = []
		for x in range(x2, x1):
			for y in range(y2, y1):
				ev_coords.append([x, y])
		map_coords = self.coords.copy()
		for c in map_coords:
			if c in ev_coords:
				print('delete', c)
				self.coords.remove(c)
			

	# def k_neigh(self):
	# 	k=3
	# 	# distance = lambda c1, c2 : sqrt( abs(c1[0] - c2[0])**2 + abs(c1[1] - c2[1])**2 )
	# 	distance = lambda c1, c2 : np.linalg.norm(np.array(c1) - np.array(c2))
	# 	map_coords = self.coords.copy()
	# 	for main_coord in map_coords:
	# 		coords_data = [(coord, distance(main_coord, coord)) for coord in map_coords if coord != main_coord]
	# 		coords_data.sort(key=lambda x: x[1])
	# 		k_coords = [c[0] for c in coords_data[:k]]
		
	# 		self._draw_lines(main_coord, k_coords)
	# 	self.save_lines()


	def k_neigh(self):
		s=6
		k=2
		distance = lambda c1, c2 : np.linalg.norm(np.array(c1) - np.array(c2))
		map_coords = self.coords.copy()
		for main in map_coords:
			neighbors = [(distance(main,coord), coord) for coord in map_coords if coord != main]
			neighbors.sort(key=lambda x: x[0])
			n=0
			for _,coord in neighbors[:s]:
				if n == k: break
				if coord == main or (coord, main) in self.graph_coords:
					continue
				line = self.get_line_coords(main, coord)
				m_line = line[len(line)//2]
				in_ = m_line in self.restricted_zones
				if not in_:
					n+=1
					self.graph_coords.append((main, coord))
					line=self.canvas.create_line(coord[0], coord[1], main[0], main[1], fill='green', width=2)

		self.save_lines()

	def _draw_lines(self, main, coords):
		for coord in coords:
			line = self.get_line_coords(main, coord)
			m_line = line[len(line)//2]
			in_ = m_line in self.restricted_zones
			if not in_:
				self.graph_coords.append((main, coord))
				line=self.canvas.create_line(coord[0], coord[1], main[0], main[1], fill='green', width=2)

	def save_lines(self):
		if len(self.graph_coords) == 0: return None
		with open("lines_data.json", "w") as jfile:
			data = json.dumps(self.graph_coords)
			jfile.write(data)
			print("Graphs Saved")		

	def get_line_coords(self, p1, p2):
		x1, y1 = p2
		x2, y2 = p1
		if x1 == x2: x1 += 1
		p = (y1 - y2)/(x1 - x2)
		b = (x1*y2 - x2*y1)/(x1 - x2)
		r = (x1, x2) if x1<x2 else (x2, x1)
		line=[]
		for x in np.arange(r[0], r[1], 0.1):
			y = p*x+b
			line.append((int(x),int(y)))
		return line


tk= tkt.Tk()
app = Image(tk, "map.png")
app.mainloop()