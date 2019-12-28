# Importing all modules
import cv2
import Skew_Correction
import PreProcessing
import Profiling
import GlobalVariables
import RemoveBorders
import handwrittenOCR
from PIL import Image as im
import numpy as np
import PIL
import os
import OCR
import json

#Function to Save Images in Disk
def Save_Images(FINAL_CROP_IMAGES_COORDINATES):
	curr_row=0
	curr_col=1
	for list_item in FINAL_CROP_IMAGES_COORDINATES:
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]
		crp_img = RotatedImage[y:y+h, x:x+w]
		crp_img = RemoveBorders.remove(crp_img)
		path = os.path.join(GlobalVariables.path, "row_"+str(curr_row+1)+"_col_"+str(curr_col)+".png")
		cv2.imwrite(path, crp_img)
		if curr_col==len(GlobalVariables.no_of_cols[curr_row]):
			curr_row += 1
			curr_col = 1	
		else:
			curr_col += 1
 

#initializing global variables
imageName = GlobalVariables.image_to_edit

#converting jpg to png file
temp_image_name = imageName.split('.')
if temp_image_name[1] == 'jpg' or temp_image_name[1] =='JPG':
	img = im.open(imageName)
	img.save(temp_image_name[0]+'.png')
	imageName = temp_image_name[0]+'.png'

#loading Image
image = cv2.imread(imageName)

#Rotating Image
RotatedImage = Skew_Correction.Correct_skew(imageName)

#smoothening Image
SmoothImage = PreProcessing.smoothening(RotatedImage)

#Binarizing Image
BinarizedImage = PreProcessing.Binarization(SmoothImage)

#Creating Chunks of images so that information can be extracted
FINAL_CROP_IMAGES_COORDINATES = Profiling.H_Profiling(BinarizedImage)

#Saving All Chunks into a Folder(Name = 'Cropped_Images')
Save_Images(FINAL_CROP_IMAGES_COORDINATES)

OCR_information = OCR.OCR_DICT()
Handwritten_info=handwrittenOCR.get_handwritten_dict() 

#Merging Dictionaries
OCR_information.update(Handwritten_info) 

#Saving Data as json in File
with  open('data_5.txt', 'w') as outfile:
    json.dump(OCR_information, outfile) 