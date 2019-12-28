import cv2
import GlobalVariables
import PreProcessing

def remove(img):
	rows, cols = img.shape[:2]
	BinarizedImage = PreProcessing.Binarization(img)

	upper_height = 0
	for i in range(rows):
		temp_sum = 0
		for j in range(cols):
			temp_sum += BinarizedImage[i,j]
		if temp_sum<int(0.15*255*cols):
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

	return img[y:h, x:w]

