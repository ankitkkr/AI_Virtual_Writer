import cv2
import mediapipe as mp
import time



class handdetector():
	def __init__(self,mode=False,maxHands=2,complexity=1,detectionCon=0.5,trackCon=0.5):
		self.mode=mode
		self.maxHands=maxHands
		self.complexity=complexity
		self.detectionCon=detectionCon
		self.trackCon=trackCon



		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.complexity,self.detectionCon,self.trackCon)
		self.mpdraw = mp.solutions.drawing_utils

		self.tipIds=[4,8,12,16,20]



	def findhands(self,img,draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		results = self.hands.process(imgRGB)
		# print(results.multi_hand_landmarks)

		if results.multi_hand_landmarks:
			for handLms in results.multi_hand_landmarks:
				if draw:
					self.mpdraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
		return img			


	def finposition(self, img, handNo=0, draw=True):

		self.lmlist= []
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		results = self.hands.process(imgRGB)
		if results.multi_hand_landmarks:
			myhand = results.multi_hand_landmarks[handNo]
			for id,lm in enumerate(myhand.landmark):
					# print(id,lm)

				h, w, c=img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				# print(id,cx,cy) 
				self.lmlist.append([id,cx,cy])


				if draw:
					cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

		return self.lmlist
				



	def fingersup(self, handNo=0):

		fingers = []
		# #thumb

		if (handNo):
			if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]:
				fingers.append(1)
			else:
				fingers.append(0)

		else:
			if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]:
				fingers.append(0)
			else:
				fingers.append(1)



		#4 fingers

		for id in range(1,5):
			if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
				fingers.append(1)

			else:
				fingers.append(0)

		return fingers









	





def main():


	pTime = 0
	cTime = 0
	cap = cv2.VideoCapture(0)
	dectetor= handdectetor()

	while True:
		success, img = cap.read()

		img=dectetor.findhands(img)

		lmList=dectetor.finposition(img)
		if len(lmList) !=0:
			print(lmList[4])




		cTime=time.time()
		fps = 1/(cTime-pTime)
		pTime = cTime


		cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),3)
		cv2.imshow("image",img)
		cv2.waitKey(1)





if __name__ == '__main__':
	main()