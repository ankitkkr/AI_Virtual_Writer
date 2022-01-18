import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm



folderPath = "Header"
mylist = os.listdir(folderPath)
# print(mylist)


overlayList=[]
for imPath in mylist:
	image = cv2.imread(f'{folderPath}/{imPath}')
	overlayList.append(image)

# print(len(overlayList))
header = overlayList[0]
drawcolor = (255,0,255)
brushthickness = 15
eraserthickness = 50




cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handdetector(detectionCon=0.85)



imgcanvas = np.zeros((720,1280,3), np.uint8)



while True:
	success, img = cap.read()
	img = cv2.flip(img,1)


	img=detector.findhands(img)
	lmList = detector.finposition(img, draw=False)

	if(len(lmList)!=0):

		#tip of index and middle fingure
		x1,y1 = lmList[8][1:]
		x2,y2 = lmList[12][1:]

		fingers = detector.fingersup()
		# print(fingers)



		if fingers[1] and fingers[2]:
			xp,yp=0,0
			cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawcolor,cv2.FILLED)
			# print("selection mode")

			#header colors
			if y1< 125:
				if 250<x1<450:
					header=overlayList[0]
					drawcolor = (255,0,255)
				elif 450<x1< 750:
					header=overlayList[1]
					drawcolor = (255,0,0)

				elif 750<x1< 950:
					header=overlayList[2]
					drawcolor = (0,255,0)

				elif 1050<x1< 1200:
					drawcolor = (0,0,0)
					header=overlayList[3]




		if fingers[1] and fingers[2]==False:
			cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
			# print("drawing mode")

			if xp==0 and yp==0:
				xp=x1
				yp=y1

			if drawcolor==(0,0,0):
				cv2.line(img,(xp,yp),(x1,y1),drawcolor,eraserthickness)
				cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,eraserthickness)

			else:
				cv2.line(img,(xp,yp),(x1,y1),drawcolor,brushthickness)
				cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthickness)

		xp,yp=x1,y1


	# setting the header img
	img[0:125,0:1280] = header

	# increasing the transparency 
	imgGray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
	_, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
	imgInv =  cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
	img = cv2.bitwise_and(img,imgInv)
	img = cv2.bitwise_or(img,imgcanvas)

	# blending two images
	img = cv2.addWeighted(img,0.5,imgcanvas,0.5,0)

	cv2.imshow("Image",img)
	cv2.waitKey(1)