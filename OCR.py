import pytesseract 
import numpy as np
from PIL import Image, ImageChops
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import PIL.ImageOps
import sys
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import PreProcessing
import GlobalVariables
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 

form_dict={}

def get_form_text(crp_img):
	text = pytesseract.image_to_string(crp_img)
	key_start = 0
	key_end = 0
	value_start = 0
	value_end = 0

	for index in range(len(text)):
		ch = text[index]
		if ch in [' ','|','#','-','',';']:
			key_start += 1
			continue
		else:
			break

	for index in range(key_start,len(text)):
		ch = text[index]
		if ch!=':':
			key_end = index
		else:
			break
	
	for index in range(key_end, len(text)):
		ch = text[index]
		if ch in [':']:
			value_start = index+1
			break

	key = text[key_start:key_end+1]
	value = text[value_start:]
	return key,value
 
def OCR_DICT():
	image_indices = GlobalVariables.image_indices
	no_of_rows = GlobalVariables.no_of_rows
	no_of_cols = GlobalVariables.no_of_cols

	count=0
	for row in range(no_of_rows):
		for col in range(len(no_of_cols[row])): 
			count=count+1
			if count in image_indices: 	
				image_name='Cropped_Images/row'    +'_' + str(row+1) +  '_' + 'col' + '_' + str(col+1) +   str('.png')
				image=cv2.imread(image_name)
				BinarizedImage=PreProcessing.Binarization(image)
				if count==15:
					text = pytesseract.image_to_string(BinarizedImage)
					temp_text = text.split('-')
					form_dict[temp_text[0]] = temp_text[1]
				else:	
					key,value = get_form_text(BinarizedImage)
					form_dict[key]=value

	return form_dict

