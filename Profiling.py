import sys
import cv2
import numpy as np
import PIL.ImageOps
import GlobalVariables
from PIL import Image as im
from scipy.ndimage import interpolation as inter
from matplotlib import pyplot as plt
import os

def V_Profiling(InputRowImage):
	rows, cols = InputRowImage.shape

	Y_COORDINATES = []
	flag = False
	for i in range(cols):
		temp = 0
		for j in range(rows):
			k=InputRowImage[j,i]
			temp += k
		if temp<int(GlobalVariables.VProfile_threshold*rows*255) and not flag:
			Y_COORDINATES.append(i)
			flag = True
		if temp>int(GlobalVariables.VProfile_threshold*rows*255):
			flag = False

	return Y_COORDINATES

def H_Profiling(BinarizedImage):
	rows, cols = BinarizedImage.shape
	ROWS_COORDINATES = []
	FINAL_CROP_IMAGES = []

	flag = False
	threshold = int(GlobalVariables.HProfile_threshold*cols*255)
	for i in range(rows):
		temp = 0
		for j in range(cols):
			k=BinarizedImage[i,j]
			temp += k
		if temp<threshold and not flag:
			ROWS_COORDINATES.append(i)
			flag = True
		if temp>threshold:
			flag = False

	if(len(ROWS_COORDINATES)!=GlobalVariables.no_of_rows+1):
		print(ROWS_COORDINATES)
		print('Image is not as per the format. As number of Rows detected are', len(ROWS_COORDINATES)-1)
		sys.exit()

	#generating images for each row
	ROW_STARTING = 0
	ROW_ENDING = cols
	for i in range(len(ROWS_COORDINATES)-1):
		y = ROWS_COORDINATES[i]-3
		h = ROWS_COORDINATES[i+1]-ROWS_COORDINATES[i]+12
		crop_img = BinarizedImage[y:y+h, ROW_STARTING:ROW_STARTING+ROW_ENDING]

		COLS_COORDINATES = V_Profiling(crop_img)

		if(len(COLS_COORDINATES)!=len(GlobalVariables.no_of_cols[i])+1):
			print('Row '+str(i+1)+' is not as per the format.But Ignored')
			b = 0
			deleted = 0
			for a in range(1,len(COLS_COORDINATES)):
				perc = COLS_COORDINATES[a-deleted]-COLS_COORDINATES[0]
				perc = perc/(COLS_COORDINATES[-1]-COLS_COORDINATES[0])
				perc = perc*100
				if abs(perc-GlobalVariables.no_of_cols[i][b])>5:
					print('detected an extra column at pixel',COLS_COORDINATES[a-deleted])
					del COLS_COORDINATES[a-deleted]
					deleted = deleted + 1
				else:
					b = b+1

		if(len(COLS_COORDINATES)!=len(GlobalVariables.no_of_cols[i])+1):
			sys.exit('Image is not as per the format.')

		for j in range(len(COLS_COORDINATES)-1):
			Y_CORD = ROWS_COORDINATES[i]
			X_CORD = COLS_COORDINATES[j]
			Width = COLS_COORDINATES[j+1]-COLS_COORDINATES[j]
			Height = ROWS_COORDINATES[i+1]-ROWS_COORDINATES[i]
			FINAL_CROP_IMAGES.append([Y_CORD, X_CORD, Width, Height])
			
	Y_CORD = ROWS_COORDINATES[len(ROWS_COORDINATES)-1]
	Height = rows-ROWS_COORDINATES[len(ROWS_COORDINATES)-1]
	X_CORD = 0
	Width = cols
	FINAL_CROP_IMAGES.append([Y_CORD, X_CORD, Width, Height])

	return FINAL_CROP_IMAGES, ROWS_COORDINATES