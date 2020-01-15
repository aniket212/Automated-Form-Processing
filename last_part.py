import cv2
import GlobalVariables
import PreProcessing
import handwrittenOCR
import pytesseract

def display_img(imgName, img):
	img = cv2.resize(img, (600,700))
	cv2.imshow(imgName,img)
	cv2.waitKey(0)

def DrawRect(image,x,y):
	img = cv2.imread('OUTPUT/Digit_Detection.png')
	image = PreProcessing.Binarization(image)

	rows,cols = image.shape
	flag = True
	col_coordinate = [0]
	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += image[i][j]
		if temp_sum==255*rows and not flag:
			flag = True
			col_coordinate.append(j)
		if temp_sum!=255*rows and flag:
			flag = False

	for i in range(1,len(col_coordinate)):
		cv2.rectangle(img, (x+col_coordinate[i-1],y), (x+col_coordinate[i],y+rows), (0,0,255), 2)
	cv2.imwrite('OUTPUT/Digit_Detection.png', img)

def RemoveBorders(img):
	# footerName = GlobalVariables.FooterName
	# img=cv2.imread(footerName) 
	img=PreProcessing.Binarization(img)
	rows, cols = img.shape

	# cv2.imshow('before', img)
	# cv2.waitKey(0)

	x = 0
	y = 0
	w = 0
	h = 0

	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += img[i][j]
		if temp_sum!=rows*255:
			x = j
			break

	for j in range(cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += img[i][cols-j-1]
		if (temp_sum!=255*rows).any():
			w = cols-j-1
			break

	# display_img(img[:,x:w])

	for i in range(rows):
		temp_sum = 0
		for j in range(x,w):
			temp_sum += img[rows-1-i][j]
		if temp_sum!=255*(w-x):
			h = rows-1-i
			break

	flag = False
	for i in range(rows):
		temp_sum = 0
		for j in range(x,w):
			temp_sum += img[i,j]
		if temp_sum>=int(0.9*255*(w-x)):
			y = i
			break

	# cv2.imshow('after', img[:h,x:w])
	# cv2.waitKey(0)
	return y, x, img[y:h,x:w]

def separate(Binarized_Image, x, y):
	rows, cols = Binarized_Image.shape

	coordinates = []
	coordinates.append([y,x,x+cols,y+int(rows/2)])
	coordinates.append([y+int(rows/2),x,x+cols,y+int(3*rows/4)])
	coordinates.append([y+int(3*rows/4),x,x+cols,y+rows])
	return coordinates

def Process_First_Image(img, x, y, OringinalImg):
	img = PreProcessing.Binarization(img)
	rows, cols = img.shape
	DICT = {}
	KEYS = GlobalVariables.last_part_keys

	# display_img(OringinalImg[y:, x:])

	part_coordinates = []

	flag = True
	for j in range(int(3*cols/5)):
		temp_sum = 0
		for i in range(rows):
			temp_sum += img[i][j]
		if temp_sum==255*rows and not flag:
			flag = True
			first_part = img[:, 0:j+5]
			second_part = img[:, j:int(3*cols/5)]
			part_coordinates.append([y,x+j,x+int(3*cols/5),y+rows])
			break
		if temp_sum!=255*rows and flag:
			flag = False

	# display_img(second_part)

	flag = True
	for j in range(int(3*cols/5),cols):
		temp_sum = 0
		for i in range(rows):
			temp_sum += img[i][j]
		if temp_sum==255*rows and not flag:
			flag = True
			third_part = img[:, int(3*cols/5):j+5]
			fourth_part = img[:, j:cols]
			part_coordinates.append([y,x+j,x+cols,y+rows])
			break
		if temp_sum!=255*rows and flag:
			flag = False
	# display_img(fourth_part)

	VALUE_coordinates = []
	# print(part_coordinates)

	temp_y = 0
	flag = True
	rows = part_coordinates[0][3]-part_coordinates[0][0]
	cols = part_coordinates[0][2]-part_coordinates[0][1]
	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += second_part[i][j]
		if temp_sum==255*cols and not flag:
			VALUE_coordinates.append([part_coordinates[0][0]+temp_y, part_coordinates[0][1], part_coordinates[0][2], part_coordinates[0][0]+i])
			flag = True
			temp_y = i
		if temp_sum!=255*cols and flag:
			flag = False

	temp_y = 0
	flag = True
	rows = part_coordinates[1][3]-part_coordinates[1][0]
	cols = part_coordinates[1][2]-part_coordinates[1][1]
	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += fourth_part[i][j]
		if temp_sum==255*cols and not flag:
			VALUE_coordinates.append([part_coordinates[1][0]+temp_y, part_coordinates[1][1], part_coordinates[1][2], part_coordinates[1][0]+i])
			flag = True
			temp_y = i
		if temp_sum!=255*cols and flag:
			flag = False
	if not flag:
		VALUE_coordinates.append([part_coordinates[1][0]+temp_y, part_coordinates[1][1], part_coordinates[1][2], part_coordinates[1][0]+rows])

	VALUES = []
	count = 0
	for list_item in VALUE_coordinates:
		y = list_item[0]
		x = list_item[1]
		w = list_item[2]
		h = list_item[3]

		if count==0:
			temp_img = PreProcessing.Binarization(OringinalImg[y:h, x:w])
			VALUES.append(pytesseract.image_to_string(temp_img))
		else:
			VALUES.append(handwrittenOCR.GetDigits(OringinalImg[y:h, x:w]))
			DrawRect(OringinalImg[y:h, x:w],x,y)
			temp_img = cv2.imread('OUTPUT/Digit_Detection.png')
			display_img('Digit_Detection', temp_img)

		count += 1

	if len(KEYS)!=len(VALUES):
		print('error in reading from the footer section')
		return {}

	for i in range(len(KEYS)):
		DICT[KEYS[i]] = VALUES[i] 
	return DICT
