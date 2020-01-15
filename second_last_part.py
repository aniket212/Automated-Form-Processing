import cv2
import PreProcessing 
import last_part 

#Spliting the second image into small chunks
def get_Images_2(Binarized_Image, y, x, originalImage): 
	temp_coordinates = []
	rows,cols=Binarized_Image.shape
	row_index_2 = 0
	count=0
	for i in range(rows):
		sum1=0 
		for j in range(cols):
			sum1=sum1+Binarized_Image[i,j]  
		if sum1 == 255*cols:
			count=count+1 
		else:
			count=0
		if count == 25:
			row_index_2=i-1 
	temp_coordinates.append([y, x, cols, row_index_2])
	temp_coordinates.append([y+row_index_2+1,x,int(cols/2),rows])
	temp_coordinates.append([y+row_index_2+1,x+int(cols/2),cols, rows])
	return temp_coordinates


#Dividing the first image into 2 parts from the mid point 
def get_Images_1(Binarized_Image, y, x, originalImage, temp_coordinates):
	rows, cols = Binarized_Image.shape
	temp_coordinates += get_Images_first_part(Binarized_Image[:,:int(cols/2)], y,x)
	# rows,cols=Binarized_Image.shape
	# temp_coordinates.append(get_Images_second_part(Binarized_Image, y, x+int(cols/2)))
	print(temp_coordinates)
	return temp_coordinates


def get_Rows(Image, y, x):
	rows,cols=Image.shape
	ROWS_CORDINATES=[]
	prev=0 
	row_index_1=-1
	for i in range(rows):
		sum1=0
		for j in range(cols):
			sum1=sum1 + Image[i,j] 
		if sum1 == 255*cols:
			row_index_1=i 
		else:
			if row_index_1 != -1:
				ROWS_CORDINATES.append([y+prev,x,cols,row_index_1])
				prev=row_index_1 	
			row_index_1=-1	
	ROWS_CORDINATES.append([y+prev,x,cols,row_index_1])
	return ROWS_CORDINATES
			

#Processing first part of the image to fetch values_image from the image
def get_Images_first_part(Binarized_Image, y, x):
	rows,cols=Binarized_Image.shape
	count=0
	row_index_1=0
	for i in range(cols):
		sum1=0
		for j in range(rows):
			sum1=sum1 + Binarized_Image[j,i]
		if sum1 == 255*rows:
			count=count+1
		else:
			count=0
		if count == 25:
			row_index_1=i 
			break
	values_image_1=Binarized_Image[0:rows,row_index_1:cols]
	cv2.imshow('hand', values_image_1)
	cv2.waitKey(0)
	return get_Rows(values_image_1, y, row_index_1) 

#Processing second part of the image to fetch values_image from the image
def get_Images_second_part(imgName):
	first_img=cv2.imread(imgName)
	Binarized_Image=PreProcessing.Binarization(first_img) 
	rows,cols=Binarized_Image.shape
	count=0
	for i in range(cols):
		sum1=0
		for j in range(rows):
			sum1=sum1 + Binarized_Image[j,i]
		if sum1 == 255*rows:
			count=count+1
		else:
			count=0
		if count == 1:
			row_index_1=i-280 
	values_image_2=Binarized_Image[0:rows,row_index_1:cols] 	
	last_part.display_img(values_image_2)  
	get_Rows(values_image_2)


