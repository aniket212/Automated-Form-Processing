import cv2
import GlobalVariables
import PreProcessing
import os


# remove borders of the croped image
def removeBoundary(img):
	rows, cols = img.shape[:2]
	BinarizedImage = PreProcessing.Binarization(img)

	upper_height = 0
	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += BinarizedImage[i,j]
		if temp_sum<int(0.50*255*cols):
			upper_height = i+5
		else:
			break

	lower_height = 0
	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += BinarizedImage[rows-1-i,j]
		if temp_sum<int(0.15*255*cols):
			lower_height = i+5
		else:
			break

	left_width = 0
	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += BinarizedImage[i,j]
		if temp_sum<int(0.03*255*rows):
			left_width = j+5
		else:
			break

	right_width = 0
	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += BinarizedImage[i,cols-1-j]
		if temp_sum<int(0.03*255*rows):
			right_width = j+5
		else:
			break

	x = left_width
	y = upper_height
	h = rows-1-lower_height
	w = cols-1-right_width

	return x,y,w,h,img[y:h, x:w]

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

# separatig each digit and storing column coordinate in the list and then returning the list
def BoundDigits(img, image, x, y, w, h):
	img = PreProcessing.Binarization(img)
	rows,cols = img.shape[:] 
	cols_coordinates = [0]

	flag = True
	for j in range(0,cols):

		temp_sum = 0
		for i in range(0,rows):
			temp_sum += img[i][j]

		if temp_sum == 255*rows and not flag:
			cols_coordinates.append(j+5)
			flag = True
		if temp_sum!=255*rows and flag:
			flag = False

	return cols_coordinates

# Creating Bounding Box on each digit detected and then saving the image as Digit_Detection.png
def Bounding_Box_Digit(image, FINAL_CROP_IMAGES_COORDINATES):

	indices = []
	for key in GlobalVariables.handwritten_info_dict.keys():
		for i in GlobalVariables.handwritten_info_dict[key]:
			indices.append(i)
	coordinates = []

	#coordinates is a list of x,y,w,h and image no of each cell
	for list_item_index in indices:
		list_item = FINAL_CROP_IMAGES_COORDINATES[list_item_index-1]
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]
		crp_img = image[y:y+h, x:x+w]
		# cv2.imshow('before', crp_img)
		xx,yy,w,h,crp_img = removeBoundary(crp_img)
		# cv2.imshow('after', crp_img)
		# cv2.waitKey(0)
		if not check_white_img(crp_img):
			x += xx
			temp = BoundDigits(crp_img, image, x, y, w, h)
			temp.append(list_item_index-1)
			if list_item_index==13:
				del temp[0]
			coordinates.append(temp)

	# using coordinates creating bounding box
	for temp_col_list in coordinates:
		list_item = FINAL_CROP_IMAGES_COORDINATES[temp_col_list[-1]]
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]
		crp_img = image[y:y+h, x:x+w]
		xx,yy,w,h,crp_img = removeBoundary(crp_img)
		x += xx
		y += yy
		for i in range(1,len(temp_col_list)-1):
			xx = temp_col_list[i-1]
			ww = temp_col_list[i]

			cv2.rectangle(image,(x+xx,y),(x+ww,y+h),(0,0,255),2)  

	# saving the image
	path = os.path.join(GlobalVariables.Output_path, 'Digit_Detection.png')
	cv2.imwrite(path, image)

# Creating Bounding Box on each row detected and then saving the image as Row_detection_Box.png
def Bounding_Box_Row(image, ROWS_COORDINATES):
	for i in range(len(ROWS_COORDINATES)-1):
		y = ROWS_COORDINATES[i]-3
		h = ROWS_COORDINATES[i+1] - ROWS_COORDINATES[i] + 12
		cv2.rectangle(image,(0,y),(image.shape[1],y+h),(0,0,255),4)
	path = os.path.join(GlobalVariables.Output_path,'Row_detection_Box.png')
	cv2.imwrite(path, image)

# Creating Bounding Box on each cell detected and then saving the image as Cell_detection_Box.png
def Bounding_Box_Cell(image, FINAL_CROP_IMAGES_COORDINATES):
	for list_item in FINAL_CROP_IMAGES_COORDINATES:
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]
		cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255),4)
	path = os.path.join(GlobalVariables.Output_path, 'Cell_detection_Box.png')
	cv2.imwrite(path, image)
	