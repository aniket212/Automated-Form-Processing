# Importing all module
import cv2
import Skew_Correction
import PreProcessing
import Profiling
import Settings
from PIL import Image as im
import numpy as np
import PIL
import OCR
import os

def Save_Images(FINAL_CROP_IMAGES_COORDINATES): #Function to save Images in the Disk
	curr_row=0
	curr_col=1
	for list_item in FINAL_CROP_IMAGES_COORDINATES:
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]
		crp_img = RotatedImage[y:y+h, x:x+w]
		path = os.path.join(Settings.path, "row_"+str(curr_row+1)+"_col_"+str(curr_col)+".png")
		cv2.imwrite(path, crp_img)
		if curr_col==Settings.no_of_cols[curr_row]:
			curr_row += 1
			curr_col = 1	
		else:
			curr_col += 1

#initializing global variables
imageName = Settings.image_to_edit

#Loading Image from Disk
image = cv2.imread(imageName)

#Rotating Image
RotatedImage = Skew_Correction.Correct_skew(imageName)

#Smoothening Image
SmoothImage = PreProcessing.smoothening(RotatedImage)

#Binarizing Image
BinarizedImage = PreProcessing.Binarization(SmoothImage)
  
#Creating Chunks of images so that information can be extracted
FINAL_CROP_IMAGES_COORDINATES = Profiling.H_Profiling(BinarizedImage)

#Saving All Chunks into a Folder(Name = 'Cropped_Images')
Save_Images(FINAL_CROP_IMAGES_COORDINATES)
print("Below is the information that is Extracted from the From Using OCR")
information=OCR.get_Form_Dictionary()
print(information)