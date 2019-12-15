import cv2
import Settings

def smoothening(img):
	dst = cv2.GaussianBlur(img,(5,5),0)
	return dst

def Binarization(img):
	threshold = Settings.Binarization_Threshold
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img,(5,5),0)
	ret,th1 = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return th1