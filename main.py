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
import BoundingBox
import copy
import last_part

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
		path = os.path.join(GlobalVariables.Cropped_path, "row_"+str(curr_row+1)+"_col_"+str(curr_col)+".png")
		cv2.imwrite(path, crp_img)
		if curr_col==len(GlobalVariables.no_of_cols[curr_row]):
			curr_row += 1
			curr_col = 1	
		else:
			curr_col += 1
 

#initializing global variables
imageName = GlobalVariables.image_to_edit

#converting given image to png file
temp_image_name = imageName.split('.')
if temp_image_name[1] != 'png' and temp_image_name[1] != 'PNG':
	img = im.open(imageName)
	img.save(temp_image_name[0]+'.png')
	imageName = temp_image_name[0]+'.png'

#loading Image
image = cv2.imread(imageName)
path = os.path.join(GlobalVariables.Output_path, "OriginalImage.png")
cv2.imwrite(path, image)
last_part.display_img('OriginalImage', image)

#Rotating Image
RotatedImage = Skew_Correction.Correct_skew(imageName)
path = os.path.join(GlobalVariables.Output_path, "RotatedImage.png")
cv2.imwrite(path, RotatedImage)
last_part.display_img('RotatedImage', RotatedImage)

#smoothening Image
SmoothImage = PreProcessing.smoothening(RotatedImage)
path = os.path.join(GlobalVariables.Output_path, "SmoothenedImage.png")
cv2.imwrite(path, SmoothImage)
last_part.display_img('SmoothImage', SmoothImage)

#Binarizing Image
BinarizedImage = PreProcessing.Binarization(SmoothImage)
path = os.path.join(GlobalVariables.Output_path, "BinarizedImage.png")
cv2.imwrite(path, BinarizedImage)
last_part.display_img('BinarizedImage', BinarizedImage)

#Creating Chunks of images so that information can be extracted
FINAL_CROP_IMAGES_COORDINATES, ROWS_COORDINATES = Profiling.H_Profiling(BinarizedImage)

#Saving All Chunks into a Folder(Name = 'Cropped_Images')
Save_Images(FINAL_CROP_IMAGES_COORDINATES)

OCR_information = OCR.OCR_DICT()
Handwritten_info=handwrittenOCR.get_handwritten_dict(copy.copy(RotatedImage), FINAL_CROP_IMAGES_COORDINATES)

#Merging Dictionaries
OCR_information.update(Handwritten_info) 

# Creating Bounding Box Image for Rows
BoundingBox.Bounding_Box_Row(copy.copy(RotatedImage), ROWS_COORDINATES)
BoundingBox.Bounding_Box_Cell(copy.copy(RotatedImage), FINAL_CROP_IMAGES_COORDINATES)
BoundingBox.Bounding_Box_Digit(copy.copy(RotatedImage), FINAL_CROP_IMAGES_COORDINATES)

# Processing the footer part of the Image
# last_part.display_img(crp_footer_img)
footer_coordinates = FINAL_CROP_IMAGES_COORDINATES[-1]
y = footer_coordinates[0]
x = footer_coordinates[1]
w = footer_coordinates[2]
h = footer_coordinates[3]
yy,xx, crp_footer_img = last_part.RemoveBorders(RotatedImage[y:, x:])
y += yy
x += xx
# last_part.display_img(crp_footer_img)
temp_coordinates = last_part.separate(crp_footer_img, x, y)  
first_img = RotatedImage[temp_coordinates[0][0]:temp_coordinates[0][3],temp_coordinates[0][1]:temp_coordinates[0][2]]
second_img = RotatedImage[temp_coordinates[1][0]:temp_coordinates[1][3],temp_coordinates[1][1]:temp_coordinates[1][2]]
third_img = RotatedImage[temp_coordinates[2][0]:temp_coordinates[2][3],temp_coordinates[2][1]:temp_coordinates[2][2]]
# last_part.display_img(first_img)

#Merging Dictionaries
OCR_information.update(last_part.Process_First_Image(first_img, temp_coordinates[0][1], temp_coordinates[0][0], copy.copy(RotatedImage)))
Key,Value = OCR.get_form_text(second_img)
OCR_information.update({Key:Value})
Key,Value = OCR.get_form_text(third_img[:,:int(third_img.shape[1]/2)])
OCR_information.update({Key:Value})
# print(OCR_information)
# last_part.display_img(third_img[:,int(third_img.shape[1]/2):])
Key,Value = OCR.get_form_text(third_img[:,int(third_img.shape[1]/2):])
OCR_information.update({Key:Value})

#Saving Data as json in File
json = json.dumps(OCR_information)
path = os.path.join(GlobalVariables.Output_path,'ExtractedInfo.txt')
f = open(path,'w')
f.write(json)
f.close()
