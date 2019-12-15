import pytesseract 
import numpy as np
from PIL import Image, ImageChops
import cv2  #Importing Opencv	
from matplotlib import pyplot as plt
from PIL import Image
import PIL.ImageOps    							#Importing required libraries
import sys
from PIL import Image as im
from scipy.ndimage import interpolation as inter 
import Settings
import PreProcessing
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  

  
def get_form_text(crp_img ,image_cols_name):  #This Function returns the text from the Image
	text = pytesseract.image_to_string(crp_img)  
	print(text)
	print()
	index= text.find(image_cols_name)
	index+=len(image_cols_name)
	slice_str=text[index:] 
	for ch in slice_str:
		if ch in [' ',':','|','#','-','',';' ]:
			index=index+1
			continue
		else:
			break
	final_str=text[index:] 	
	return image_cols_name,final_str    

def SHOW_CROP_IMAGE(crp_img, y, x, w, h,image_cols_name):   #Function Displays the Crop Image 
	crp_img = crp_img[y:y+h, x:x+w]
	cv2.imshow("finally", crp_img)
	cv2.waitKey(0)
	return get_form_text(crp_img,image_cols_name)
  
def remove_borders(Image,image_cols_name):  #Function to Remove Upper and Left Border From the Image
	rows,cols=Image.shape
	print(rows,cols)
	flag=False
	count=0 
	for i in range(cols):
		sum=0
		for j in range(rows): 
			sum=sum+Image[j,i]
		if sum >= (int(0.98*255*cols)):
			continue
		elif sum > 0:
			y=i+5
			break
 
	for i in range(rows):
		sum=0
		for j in range(cols):
			 sum=sum+Image[i,j]
			 #print(Image[i,j])
		if sum  >= int(0.90*255*cols):
			continue
		elif sum>0:
			x=i+6
			break
			 
    #if cols - x > 0 and rows- y > 0 :
	w=cols-x
	h=rows-y
	return SHOW_CROP_IMAGE(Image,y,x,w,h,image_cols_name)	
	 		

def get_Form_Dictionary(): 
	form_dict={}
	image_indexes=[1,3,4,5,7,8,11,14,15] 
	no_of_rows=Settings.no_of_rows
	no_of_cols=Settings.no_of_cols
	image_cols=Settings.image_cols_name
	count=0
	k=0
	for row in range(no_of_rows):
		for col in range(no_of_cols[row]): 
			count=count+1
			if count in image_indexes: 		
				image_name='Cropped_Images/' + 'row' +'_' + str(row+1) +  '_' + 'col' + '_' + str(col+1) +   str('.png') 
				print(image_name) 
				image=cv2.imread(image_name)  
				cv2.imshow("",image) 
				BinarizedImage=PreProcessing.Binarization(image)  
				key,value=remove_borders(BinarizedImage,image_cols[k])
				form_dict[key]=value  
				cv2.waitKey(0) 
				k=k+1 	 				 	   
	return form_dict
	 