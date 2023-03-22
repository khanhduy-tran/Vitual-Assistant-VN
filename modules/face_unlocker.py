import cv2
import os
from os.path import isfile, join
from typing import Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont

face_classifier = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_classifier.detectMultiScale(gray, 1.3, 5)

	if faces is ():
		return img,[]

	for (x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255), 2)
		#region of interest
		roi = img[y:y+h, x:x+w]
		roi = cv2.resize(roi, (200,200))

	return img,roi

def startDetecting():
	try:
		model = cv2.face.LBPHFaceRecognizer_create()
		model.read('userData/trainer.yml')
	except:
		print('Vui lòng thêm khuôn mặt của bạn.')
		return None
		
	flag = False
	cap = cv2.VideoCapture(0)

	while True:
		ret, frame = cap.read()
		image, face = face_detector(frame)

		try:
			face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
			result = model.predict(face)

			if result[1] < 500:
				confindence = int((1-(result[1])/300) * 100) #percentange
				display_string = str(confindence) + '%'
			cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)

			if confindence > 80:
				cv2.putText(image, "Da mo khoa", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
				cv2.imshow('Cat khuon mat', image)
				flag = True
				break
			else:
				cv2.putText(image, "Da khoa", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
				cv2.imshow('Cat khuon mat', image)


		except Exception as e:
			cv2.putText(image, "Khong tim thay khuon mat", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
			cv2.imshow('Cat khuon mat', image)
			pass

		if cv2.waitKey(1) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
	return flag

imageName = ''
def clickPhoto():
	global imageName
	if os.path.exists('Camera')==False:
		os.mkdir('Camera')
	
	from time import sleep
	import playsound
	from datetime import datetime

	cam = cv2.VideoCapture(0)
	_, frame = cam.read()
	playsound.playsound('assets/audios/photoclick.mp3')
	imageName = 'Camera/Camera_'+str(datetime.now())[:19].replace(':', '_')+'.png'
	cv2.imwrite(imageName, frame)
	cam.release()
	cv2.destroyAllWindows()

def viewPhoto():
	from PIL import Image
	img = Image.open(imageName)
	img.show()
def cv2_img_add_text(img, text, left_corner: Tuple[int, int],
                     text_rgb_color=(255, 0, 0), text_size=24, font='assets/fonts/VHARIAL.TTF', **option):
    """
    USAGE:
        cv2_img_add_text(img, '中文', (0, 0), text_rgb_color=(0, 255, 0), text_size=12, font='mingliu.ttc')
    """
    pil_img = img
    if isinstance(pil_img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))
    draw.text(left_corner, text, text_rgb_color, font=font_text)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    if option.get('replace'):
        img[:] = cv2_img[:]
        return None
    return cv2_img
