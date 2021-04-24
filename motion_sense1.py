import cv2 as cv
import pyautogui
import numpy as np
from time import sleep
cv.namedWindow('Images')
cap = cv.VideoCapture(0)


def getContours(img, width):
	x, y, r, left_centre = 0, 0, 0, (0, 0)
	
	contour_l, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	
	#cv.drawContours(imgResult, contour_l, -1, (0, 0, 255), 3)
	
	if len(contour_l) > 0:
		contour = max(contour_l, key=lambda x: cv.contourArea(x))
		
		((x, y), r) = cv.minEnclosingCircle(contour)
		M = cv.moments(contour)
		left_centre = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))
		#print(left_centre)
	return x, y, r, left_centre
	
	'''if len(contour_r) > 0:
		contour1 = max(contour_r, key=lambda x: cv.contourArea(x))
		((x, y), r) = cv.minEnclosingCircle(contour1)
		M = cv.moments(contour1)
		left_centre = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))
		return x, y, r '''
	
while cap.isOpened():
	keyPressed = False
	#sleep(10)
	ret, img = cap.read()
	img = cv.flip(img, 1)
	img = cv.resize(img, (0,0), fx=0.5, fy=0.5)
	height,width = img.shape[:2]
	img_blur = cv.GaussianBlur(img, (3, 3), 0)
	imgHSV = cv.cvtColor(img_blur, cv.COLOR_BGR2HSV)
	imgResult = img.copy()
	
	#print(h_min, h_max, s_min, s_max, v_min, v_max)
	lower = np.array([43, 90, 65])
	upper = np.array([154, 255, 255])
	# Senses green color
	# Lower and upper arrays of hsv values can be changed for different colors
	mask = cv.inRange(imgHSV, lower, upper)    
	
	kernel = np.ones((5,5))
	
	dilation = cv.dilate(mask, kernel, iterations=1)
	erosion = cv.erode(dilation, kernel, iterations=1)
    
	x, y, r, centre = getContours(erosion, width)
	if r>10:
		cv.circle(imgResult, (int(x), int(y)), int(r), (0, 0, 255), 2)
	else: centre =(0, 0)
	
	
	keyPressed = True
	if centre != (0, 0):	
		if centre[0] <= width//2 and centre[1] > height//2:
			cv.putText(imgResult ,'LEFT',(20,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
			pyautogui.press('left')
			keyPressed = True
		elif centre[0] > width//2 and centre[1] <= height//2:
			cv.putText(imgResult ,'RIGHT',(20,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
			pyautogui.press('right')
			keyPressed = True
		elif centre[1] < height//2 and centre[0] < width//2:
			cv.putText(imgResult ,'JUMP',(20,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
			pyautogui.press('up')
			keyPressed = True
		elif centre[1] > height//2 and centre[0] >= width//2:
			cv.putText(imgResult ,'BEND',(20,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
			pyautogui.press('down')
			keyPressed = True
	
	
	#cv.imshow('Mask', mask)
	
	cv.imshow('Image', imgResult)
	key = cv.waitKey(1)
	if key == 27: break
	
cap.release()
cv.destroyAllWindows()	
