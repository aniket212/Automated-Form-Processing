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

handwritten_dict={}
def removeBlackPixels():
	img = cv2.imread("Cropped_Images/row_11_col_1.png")
	cv2.imshow('', img)
	cv2.waitKey(0)
	# img = PreProcessing.Binarization(img)

	rows,cols = img.shape[:2]

	for i in range(rows-1):
		for j in range(cols-1):
			B = img[i][j][0]
			G = img[i][j][1]
			R = img[i][j][2]
			if (R<130 and G<130 and B<130):
				img[i][j] = [255,255,255]
			else:	
				print(R,G,B)

	cv2.imshow('', img)
	cv2.waitKey(0)
	return img

def FindBoundary(crop_img):
	rows, cols = crop_img.shape[:] 
	flag=False 
	vertical_sum=[]
	horizontal_sum=[]
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

def get_Prediction(img): 
	img = np.reshape(img,[1,28,28,1])
	y_pred1=model.predict(img)
	prediction=np.argmax(y_pred1,axis=1)
	return prediction

def GetDigits(img):
	img = PreProcessing.Binarization(img)
	cv2.imshow('', img) 
	rows,cols = img.shape[:] 
	cols_coordinates = []
	number=''
	flag = True
	for j in range(0,cols):

		temp_sum = 0
		for i in range(0,rows):
			temp_sum += img[i][j]

		if temp_sum == 255*rows and flag:
			cols_coordinates.append(j+5)
			flag = False
		if temp_sum<255*rows:
			flag = True

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
		print(digit,count) 
		#Appending each digit to form a  number
		number=number + digit 
	return number	

def get_handwritten_dict():
	image_indices=GlobalVariables.handwritten_img_indices
	cols_names=GlobalVariables.handwritten_cols_names
	no_of_rows = GlobalVariables.no_of_rows 
	no_of_cols = GlobalVariables.no_of_cols 
	count=0
	for row in range(no_of_rows):
		for col in range(len(no_of_cols[row])): 
			count=count+1
			if count in image_indices: 	
				image_name='Cropped_Images/row'    +'_' + str(row+1) +  '_' + 'col' + '_' + str(col+1) +   str('.png')
				image=cv2.imread(image_name) 
				temp=(count-5)%len(cols_names)  
				key=cols_names[temp]
				value=GetDigits(image) 
				if key not in handwritten_dict.keys(): 
					value_list=[]
					value_list.append(value)
					handwritten_dict[key]=value_list
				else:
					value_lst=handwritten_dict[key]
					value_lst.append(value)
					handwritten_dict[key]=value_lst 
	return handwritten_dict	

#Loading Model 
model_name=GlobalVariables.Model_Name
model=load_model(model_name)  

#img = removeBlackPixels()
'''image_indices_handwritten=GlobalVariables.handwritten_img_indices 
for  

img = cv2.imread('Cropped_Images/row_8_col_1.png')
GetDigits(img)'''