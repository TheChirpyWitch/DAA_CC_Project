import cv2
import numpy as np
import glob
import os
# from imutils import paths
# from itertools import islice
# img = cv2.imread("test5.jpg")

# cv2.imshow("Original", img)

def crop_minAreaRect(img, rect):
	# rotate img
	angle = rect[2]
	rows,cols = img.shape[0], img.shape[1]
	M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
	img_rot = cv2.warpAffine(img,M,(cols,rows))

	# rotate bounding box
	rect0 = (rect[0], rect[1], 0.0) 
	box = cv2.boxPoints(rect0)
	pts = np.int0(cv2.transform(np.array([box]), M))[0]    
	pts[pts < 0] = 0

	# crop
	img_crop = img_rot[pts[1][1]:pts[0][1], 
						pts[1][0]:pts[2][0]]
	cv2.imshow("YOLO", img_crop)
	cv2.waitKey(0)
	return img_crop

def clean_image_original(img):
	#make image gray 
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	#Blur
	blur = cv2.GaussianBlur(gray,(5,5),0)
	bilateral = cv2.bilateralFilter(blur,5,75,75)

	#Thresholding
	thresh = cv2.threshold(bilateral, 0, 255, cv2.THRESH_OTSU)[1]
	# cv2.imshow("Thresh", thresh)

	# Erosion
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	# erosion = cv2.erode(thresh, kernel, iterations = 1)
	# cv2.imshow("Erosion", erosion)

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 2))
	dilation3 = cv2.dilate(thresh,kernel,iterations = 7)
	return dilation3

def clean_image(img):
	height, width = img.shape[:2]

	# Specify the color range of the lines you want to remove [lower, upper]
	lower = [0, 0, 0]
	upper = [120, 130, 130]
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8") 


	# Create a mask of the lines
	mask = cv2.inRange(img, lower, upper)

	output = cv2.bitwise_and(img, img, mask = mask)

	# As the original comment explains, dilate lines a bit because aliasing 
	# may have filtered borders too much during masking 
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	dilation = cv2.dilate(output, kernel, iterations = 3)

	# Conver the mask to gray scale
	gray = cv2.cvtColor(dilation, cv2.COLOR_BGR2GRAY)

	# Reference: https://docs.opencv.org/trunk/df/d3d/tutorial_py_inpainting.html
	# Apply the mask created above on the image
	dst = cv2.inpaint(img,gray,3,cv2.INPAINT_TELEA)


	# Post mask application, there will be inconsistency/gaps/separation of individual 
	# digits/alphabets. So we dilate (puff up the white blobs) so that each individual 
	# digit gets properly connected and considered as one blob (which can be further used
	# to find contours)
	dilation = cv2.dilate(dst, kernel, iterations = 2)

	# Reference for blurring and bilateral filtering: 
	# https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
	blur = cv2.GaussianBlur(dilation,(5,5),0)
	bilateral = cv2.bilateralFilter(blur,5,75,75)
	gray = cv2.cvtColor(bilateral, cv2.COLOR_BGR2GRAY)
	# If pixel value is greater than a threshold value, it is assigned one value (may be white), 
	# else it is assigned another value (may be black)
	# Reference: https://docs.opencv.org/3.4.0/d7/d4d/tutorial_py_thresholding.html
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

	return thresh

def clean_image_patna(img):
	# Crop the image to eliminate border
	h, w, c = img.shape

	start_x = int(0.12*w)
	start_y = int(0.15*h)

	img = img[start_y: h - start_y, start_x: w - start_x]
	#cv2.imshow("Original", img)
	#make image gray 
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imshow("Gray", gray)
	#Blur
	blur = cv2.GaussianBlur(gray,(5,5),0)
	# cv2.imshow("Blur", blur)

	# bilateral = cv2.bilateralFilter(blur,5,75,75)
	#cv2.imshow("Bilateral", bilateral)

	#Thresholding
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]
	# cv2.imshow("Thresh", thresh)

	thresh_inv = cv2.bitwise_not(thresh)
	# Erosion
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
	erosion = cv2.erode(thresh_inv, kernel, iterations = 1)
	# cv2.imshow("Erosion", erosion)


	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	dilation = cv2.dilate(erosion,kernel,iterations = 1)
	# cv2.imshow("Dilation", dilation)

	dilation_inv = cv2.bitwise_not(dilation)

	return dilation_inv

def clean_image_lucknow(img):
	#make image gray 
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	#Thresholding
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

	thresh_inv = cv2.bitwise_not(thresh)

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,2))
	dilation3 = cv2.dilate(thresh_inv, kernel, iterations = 1)

	inv_again = cv2.bitwise_not(dilation3)
	return inv_again
	
def localize(img):
	"""
	Localize text in a black and white image
	"""
	# # Crop the image to eliminate border
	# h, w, c = img.shape

	# start_x = int(0.12*w)
	# start_y = int(0.15*h)

	# img = img[start_y: h - start_y, start_x: w - start_x]

	# #make image gray 
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# #Blur
	# blur = cv2.GaussianBlur(gray,(5,5),0)

	# sobel = cv2.Sobel(blur, -1, 1, 0)
	# cv2.imshow("Sobel", sobel)

	# #Thresholding
	# thresh = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU)[1]
	# cv2.imshow("Thresh", thresh) 

	
	thresh = clean_image_patna(img)
	cv2.imshow("Original", thresh)
	height, width = thresh.shape
	
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,4))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) 

	cnts = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(thresh,(x,y),(x+w,y+h),(255,255,255),1)
		cv2.line(thresh, (x + (w/3), y), (x + (w/3), y+h), (255,255,255), 1)
		cv2.line(thresh, (x+(2*w/3), y), (x+(2*w/3), y+h), (255,255,255), 1)
	return closed, thresh

def clean_image_sc(img):
	# Crop the image to eliminate border
	# h, w, c = img.shape

	# start_x = int(0.12*w)
	# start_y = int(0.15*h)

	# img = img[start_y: h - start_y, start_x: w - start_x]
	#cv2.imshow("Original", img)
	#make image gray 
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imshow("Gray", gray)
	#Blur
	blur = cv2.GaussianBlur(gray,(5,5),0)
	# cv2.imshow("Blur", blur)

	# bilateral = cv2.bilateralFilter(blur,5,75,75)
	#cv2.imshow("Bilateral", bilateral)

	#Thresholding
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]
	# cv2.imshow("Thresh", thresh)

	thresh_inv = cv2.bitwise_not(thresh)
	# Erosion
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
	erosion = cv2.erode(thresh_inv, kernel, iterations = 1)
	# cv2.imshow("Erosion", erosion)


	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	dilation = cv2.dilate(erosion,kernel,iterations = 1)
	# cv2.imshow("Dilation", dilation)

	inv = cv2.bitwise_not(dilation)
	return inv

if __name__ == '__main__':
	# list_images = paths.list_images("../PatnaCaptcha/PatnaCaptchaScreenShots")
	# for image in list_images:
	# 	img = cv2.imread(image)
	# 	img_s = localize(img)
	# 	img_o = clean_image_original(img)
	# 	cv2.imshow("Final Output", np.hstack([img_s]))
	# 	cv2.waitKey(0)
	list_images = glob.glob("../CCLData/SupremeCourtCaptchaScreenShots/*.png")
	os.system("mkdir -p thresholded_patna_images")
	print(list_images[:2])
	for i, image in enumerate(list_images):
		img = cv2.imread(image)
		img_s = clean_image_sc(img)
		cv2.imshow("Final Output", np.hstack([img_s]))
		# print(os.path.join("thresholded_patna_images", image.split("/")[-1]))
		cv2.imwrite(os.path.join("../CCLData/thresholded_sc_pbm_images", image.split("/")[-1].split(".")[0] + ".pbm"), img_s)
		# cv2.imshow("Bounding Box", rect)

		# cv2.waitKey(0)