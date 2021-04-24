import cv2 as cv
import pyautogui
import numpy as np
from imutils.video import VideoStream
from time import sleep

cv.namedWindow('Images')
#cap = cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_BUFFERSIZE, 2)
cap = VideoStream(src=0).start()
sleep(2.0)
cascPath = '/Users/legend/Downloads/haarcascade_frontalface_default.xml'
def empty(a):
	pass

def detectFace(img, res):
	x, y, w, h = 0, 0, 0, 0
	faceCascade = cv.CascadeClassifier(cascPath)
	#gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		
	)
	for (x, y, w, h) in faces:
		cv.rectangle(res, (x, y), (x+w, y+h), (0, 255, 0), 2)
	return x+w//2, y+h//2


	
def getContours(img):
	contours, _ = cv.findContours(diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	
	contour = max(contours, key=lambda x: cv.contourArea(x))
	((x, y), r) = cv.minEnclosingCircle(contour)
	M = cv.moments(contour)
	centre = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))
	return centre
x, y = 0, 0	


while True:
	
	keyPressed = False
	#sleep(10)
	img = cap.read()
	img = cv.flip(img, 1)
	img = cv.resize(img, (0,0), fx=0.5, fy=0.5)
	imgResult = img.copy()
	

	height,width = img.shape[:2]
	# Start by aligning your face within this rectangle
	cv.rectangle(imgResult, (width//2 - 70, height//2 -70), (width//2 + 70, height//2 +70), (0, 0, 255), 0)
	
	x_p, y_p = detectFace(img, imgResult)
	

	x, y = width//2, height//2

	ans = abs(y_p - y) < abs(x_p - x)
	if abs(y_p - y) > 40 or abs(x_p - x) > 50:
	
		if x_p > x and ans: 
			cv.putText(imgResult, 'RIGHT', (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
			pyautogui.press('right')
		elif x_p < x and ans:
			cv.putText(imgResult, 'LEFT', (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
			pyautogui.press('left')
		elif y_p > y and not ans:
			cv.putText(imgResult, 'BEND', (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
			pyautogui.press('down')
		elif y_p < y and not ans:
			cv.putText(imgResult, 'JUMP', (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
			pyautogui.press('up')
	
	
	cv.imshow('Image', imgResult)

	key = cv.waitKey(1)
	if key == 27: break
	
cap.stop()
cv.destroyAllWindows()	
	

