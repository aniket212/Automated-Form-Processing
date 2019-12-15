import cv2
def Horizontal_Profiling(image):	  	#Function to perform Horizontal Profiling

	#Inverting the Image

	invert=255-image           			
	proj = np.sum(invert,1)     
	m = np.max(proj)
	w = 500
	result = np.zeros((proj.shape[0],500))

	# Draw a line for each row
	for row in range(invert.shape[0]):
	   cv2.line(result, (0,row), (int(proj[row]*w/m),row), (255,255,255), 1)

	# Save result
	cv2.imwrite('horizontal_prof.png', result)

def Vertical_Profiling(image): 		 		#Function to perform Vertical Profiling

	#Inverting the Image
	
	invert=255-image           				
	proj = np.sum(invert,0) 
	print(proj.shape)   		#
	m = np.max(proj)
	w = 638
	result = np.zeros((493,638))

	# Draw a line for each row
	for col in range(invert.shape[1]):
	   cv2.line(result, (0,col), (int(proj[col]*w/m),col), (255,255,255), 1)

	# Save result
	cv2.imwrite('vertical_prof.png', result)	

