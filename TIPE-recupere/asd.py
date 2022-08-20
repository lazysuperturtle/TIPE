import cv2 as cv
import numpy as np

img = cv.imread('em1.png')
grayImage1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage1) = cv.threshold(grayImage1, 127, 255, cv.THRESH_BINARY)

img = cv.imread('em2.png')
grayImage2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage2) = cv.threshold(grayImage2, 127, 255, cv.THRESH_BINARY)

match = 0

m = min(len(blackAndWhiteImage1), len(blackAndWhiteImage2)) 
l = min(len(blackAndWhiteImage1[0]), len(blackAndWhiteImage2[0]))
n = 0
tot = m * l


while n < m:
	l1, l2 = blackAndWhiteImage1[n], blackAndWhiteImage2[n]
	mat = [1 for x in range(l) if l1[x] == l2[x]]
	match += len(mat)
	n+=1

res = (match/tot) * 100
print(f"Images match: {res}%")


cv.imshow('tt.png',blackAndWhiteImage1)
cv.imshow('tt.png',blackAndWhiteImage2)