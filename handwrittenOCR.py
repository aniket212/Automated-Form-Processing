import cv2
import GlobalVariables
import PreProcessing
from keras.models import load_model
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
import numpy as np
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import RemoveBorders
import pytesseract

#Dictionay to store keys and values of corresponding handwritten cells
handwritten_dict={}

def FindBoundary(crop_img):
	rows, cols = crop_img.shape 
	flag=False 
	vertical_sum=[]
	horizontal_sum=[]
	x=0
	y=0
	w=0
	h=0

	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += crop_img[i,j]
		vertical_sum.append(temp_sum)

	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += crop_img[i,j]
		horizontal_sum.append(temp_sum) 

	temp = 255*rows
	for i in range(len(vertical_sum)):
		if vertical_sum[i]!=temp:
			x=i
			break 
	for i in range(len(vertical_sum)-1,-1,-1):
		if vertical_sum[i]!=temp:
			w = i
			break 
	temp = 255*cols
	for i in range(len(horizontal_sum)):
		if horizontal_sum[i]!=temp:
			y=i
			break 
	for i in range(len(horizontal_sum)-1,-1,-1):
		if horizontal_sum[i]!=temp:
			h = i
			break 
	return crop_img[y:h,x:w] 

# Function predicts the digit from the image
def get_Prediction(img): 
	#Reshaping the image to 28*28
	img = np.reshape(img,[1,28,28,1])
	y_pred1=model.predict(img) 
	prediction=np.argmax(y_pred1,axis=1)
	return prediction

#Returns the number formed after appending the digits in the image
def GetDigits(img):
	img = PreProcessing.Binarization(img)
	cv2.imshow('binarized number', img) 
	cv2.waitKey(0)
	rows,cols = img.shape[:] 
	cols_coordinates = [0]
	number=''
	flag = True
	for j in range(0,cols):

		temp_sum = 0
		for i in range(0,rows):
			temp_sum += img[i][j]  

		#Detecting column of all white pixels and then splitting the digits from the image	
		if temp_sum == 255*rows and not flag:
			cols_coordinates.append(j+5)
			flag = True
		if temp_sum!=255*rows and flag:
			flag = False

	print(cols_coordinates)
	if len(cols_coordinates)>0: 
		x = cols_coordinates[0] 

	for i in range(1,len(cols_coordinates)):
		w = cols_coordinates[i]
		crop_img = img[:,x:w]
		x = w 
		crop_img = FindBoundary(crop_img)
		crop_img = cv2.resize(crop_img, (20,20)) 
		temp_crop_img = []
		for i in range(28):
			temp = []
			for j in range(28):
				temp.append(0)
			temp_crop_img.append(temp)

		for i in range(20):
			for j in range(20):
				if crop_img[i][j]>127:
					crop_img[i][j] = 255
				else:
					crop_img[i][j] = 0

				if crop_img[i][j]==0:
					temp_crop_img[4+i][4+j] = 255  
		cv2.imshow('Boundary', np.float32(temp_crop_img))
		cv2.waitKey(0) 
		pred_digit=get_Prediction(temp_crop_img)
		count=0
		digit=str(pred_digit[0])
		for i in range(20):
			for j in range(20): 
			    if temp_crop_img[4+i][4+j] == 255 :
				    count=count+1
		if count>=(200):
			digit="1"
		print(digit) 
		#Appending each digit to form a  number
		number=number + digit 
	return number	

# Returns the Dictionary of handwritten characters
def check_white_img(image):
	image = PreProcessing.Binarization(image)
	rows,cols=image.shape
	sum1=0
	for i in range(int(rows/2)-10,int(rows/2)+10):
		for j in range(10,cols-10):
			sum1=sum1+image[i,j]
	white=255*20*(cols-20)
	if sum1 >= int(0.99*white):
		return True
	return False	
 
def get_handwritten_dict(RotatedImage, FINAL_CROP_IMAGES_COORDINATES):
	image_dict = GlobalVariables.handwritten_info_dict
	final_ans = {}

	for key in image_dict.keys():
		value_list = image_dict[key]
		VALUE = []
		for element in value_list:
			value_image_index = FINAL_CROP_IMAGES_COORDINATES[element-1]
			y = value_image_index[0]
			x = value_image_index[1]
			w = value_image_index[2]
			h = value_image_index[3]
			value_image = RotatedImage[y:y+h, x:x+w]
			value_image = RemoveBorders.remove(value_image)
			if check_white_img(value_image):
				VALUE.append("")
			else:
				VALUE.append(str(GetDigits(value_image)))
		if key=='INCHES OUT':
			final_ans[key] = [VALUE[0][1:]]
		else:
			final_ans[key] = VALUE
	return final_ans

#Loading Model 
model_name=GlobalVariables.Model_Name
model=load_model(model_name) 
