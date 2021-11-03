import cv2
import glob
import os
import numpy as np


def perform_ccl(img):
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

    # dilation_inv = cv2.bitwise_not(dilation)

    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilation, 4, cv2.CV_32S)

    print("Number of labels: ", numLabels)

    return dilation

if __name__ == '__main__':
	list_images = glob.glob("../CCLData/PatnaCaptchaScreenShots/*.png")
	for i, image in enumerate(list_images[:1]):
		img = cv2.imread(image)
		img_s = perform_ccl(img)
		cv2.imshow("Final Output", np.hstack([img_s]))
		# cv2.imwrite(os.path.join("../CCLData/thresholded_sc_pbm_images", image.split("/")[-1].split(".")[0] + ".pbm"), img_s)

		cv2.waitKey(0)