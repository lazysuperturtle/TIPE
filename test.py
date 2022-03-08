from matplotlib import pyplot as plt
from math import sqrt
import tkinter as tkt
import numpy as np
import cv2 as cv
import json
import time



# img_test = cv.imread('test.png')
# img_gray = cv.cvtColor(img_test, cv.COLOR_BGR2GRAY)
# template = cv.imread('car4.png',0)
# w, h = template.shape[::-1]
# res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
# threshold = 0.5
# loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv.rectangle(img_test, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
# cv.imwrite('res.png',img_test)


class Image(tkt.Frame):

	def __init__(self, tk, file):
		super().__init__(tk)
		self.file = file
		self.window = tkt.Toplevel()
		self.canvas = tkt.Canvas(self, width=800, height=800)
		self.canvas2 = tkt.Canvas(self.window, width=800, height=800)

		self.img = tkt.PhotoImage(file=self.file)
		self.canvas.create_image(0, 0, anchor=tkt.NW, image=self.img)
		self.bttn = tkt.Button(self, text="Save", command=self.save)
		self.bttn.pack()
		self.bttn1 = tkt.Button(self, text="Test", command=self.test)
		self.bttn1.pack()
		self.bttn2 = tkt.Button(self, text="Restore", command=self.restore)
		self.bttn2.pack()
		self.bttn3 = tkt.Button(self, text="Connect", command=self.k_neigh)
		self.bttn3.pack()
		self.coords = []
		self.circles = []
		self.canvas.bind("<Button-1>", self.get_coords)
		self.canvas.pack()
		self.canvas2.pack()
		self.pack()

		self.image = cv.imread(self.file)
		color = [0,0,0] #230 230 230 

		y, x = np.where(np.all(self.image==color, axis=2))
		self.restricted_zones = np.column_stack((x, y))
		# self.restricted_zones = list(zip(x,y))
		
		r=1
		for x, y in self.restricted_zones:
			self.canvas2.create_oval(x-r, y-r, x+r, y+r, fill='red')	


	def save(self):
		with open("data.json", "w") as jfile:
			data = json.dumps(self.coords)
			jfile.write(data)
		print("Saved")

	def draw(self):
		data = self.coords.copy()
		data.sort()
		for i in range(1, len(data)):
			c1, c2 = data[i-1], data[i]
			self.canvas.create_line(c1[0], c1[1], c2[0], c2[1], fill='green', width=1)

	def restore(self):
		with open("data.json", "r") as jfile:
			file_data = jfile.readlines()
			data = json.loads(file_data[0])
			self.coords = data
			r=5
			data.sort()
			for coord in data:
				x, y = coord
				self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')	

	def undo(self):
		if len(self.circles)>0:
			circle = self.circles.pop()
			self.canvas.delete(circle)
			self.coords.pop()

	def get_coords(self, event):
		x, y = event.x, event.y
		self.coords.append((x, y))
		r = 5
		circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')
		self.circles.append(circle)

	def k_neigh(self):
		k=8
		distance = lambda c1, c2 : sqrt( abs(c1[0] - c2[0])**2 + abs(c1[1] - c2[1])**2 )
		map_coords = self.coords.copy()
		for main_coord in map_coords:
			coords_data = [(coord, distance(main_coord, coord)) for coord in map_coords if coord != main_coord]
			coords_data.sort(key=lambda x: x[1])
			k_coords = [c[0] for c in coords_data[:k]]
			self._draw_lines(main_coord, k_coords)


	def _draw_lines(self, main, coords):

		contains = lambda l1, l2: True in np.isin(l1,l2)
		good_coords = [c for c in coords if True not in np.isin(self.get_line_coords(main, c), self.restricted_zones)]
		print()
		for c in good_coords:
			print(np.isin(self.get_line_coords(main, c), self.restricted_zones))
			line=self.canvas.create_line(c[0], c[1], main[0], main[1], fill='green', width=1)
			if main[0]<c[0]:
				self.test(main,c)
			else:
				self.test(c, main)


	def get_line_coords(self, p1, p2):
		if p1[0]<p2[0]:
			x1, y1 = p1
			x2, y2 = p2
		else:
			x1, y1 = p2
			x2, y2 = p1

		if x1 == x2: x1 += 1
		p = (y1 - y2)/(x1 - x2)
		b = (x1*y2 - x2*y1)/(x1 - x2)
		r = range(x1, x2) if x1<x2 else range(x2, x1)
		line = [p*x+b for x in r]
		return line

	def test(self, p1, p2):
		if p1[0] == p2[0]: p1[0] += 1
		p = (p1[1] - p2[1])/(p1[0] - p2[0])
		b = (p1[0]*p2[1] - p2[0]*p1[1])/(p1[0] - p2[0])
		line = []
		for x in range(p1[0], p2[0]+1):
			y = p * x + b
			line.append([x, y])
		r = 2
		for point in line:
			x, y = point
			self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='red')	



tk= tkt.Tk()
app = Image(tk, "result.png")
app.mainloop()