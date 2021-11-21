import cv2
import glob
import os
import numpy as np


def clean(img):
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
    # blur = cv2.GaussianBlur(gray,(5,5),0)
    # cv2.imshow("Blur", blur)
    # bilateral = cv2.bilateralFilter(blur,5,75,75)
    #cv2.imshow("Bilateral", bilateral)

    #Thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    # cv2.imshow("Thresh", thresh)

    thresh_inv = cv2.bitwise_not(thresh)
    # Erosion
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # erosion = cv2.erode(thresh_inv, kernel, iterations = 1)
    # cv2.imshow("Erosion", erosion)


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilation = cv2.dilate(thresh_inv,kernel,iterations = 1)
    # cv2.imshow("Dilation", dilation)
    
    return dilation
    # dilation_inv = cv2.bitwise_not(dilation)

    

    # return dilation

def perform_ccl(image):
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, 4, cv2.CV_32S)

    # initialize an output mask to store all characters parsed from
    # the license plate
    mask = np.zeros(image.shape, dtype="uint8")

    # loop over the number of unique connected component labels
    for i in range(1, numLabels):
        # the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]
        # print("Number of labels: ", numLabels)
        print("Area: {}".format(area))
        # ensure the width, height, and area are all neither too small
        # nor too big
        # keepWidth = w > 100
        # keepHeight = h > 100
        keepArea = area > 50
        

        # ensure the connected component we are examining passes all
        # three tests
        if keepArea:
            # construct a mask for the current connected component and
            # then take the bitwise OR with the mask
            print("[INFO] keeping connected component '{}'".format(i))
            componentMask = (labels == i).astype("uint8") * 255
            mask = cv2.bitwise_or(mask, componentMask)
    


    return mask
    """
    # clone our original image (so we can draw on it) and then draw
    # a bounding box surrounding the connected component along with
    # a circle corresponding to the centroid
    output = image.copy()
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 1)
    # cv2.circle(output, (int(cX), int(cY)), 3, (0, 0, 255), -1)

    # construct a mask for the current connected component by
    # finding a pixels in the labels array that have the current
    # connected component ID
    componentMask = (labels == i).astype("uint8") * 255
    # show our output image and connected component mask
    cv2.imshow("Output", output)
    cv2.imshow("Connected Component", componentMask)
    key = cv2.waitKey(0)
    """
if __name__ == '__main__':
    list_images = glob.glob("../CCLData/PatnaCaptchaScreenShots/*.png")
    for i, image in enumerate(list_images[:1]):

        
        img = cv2.imread(image)
        
        # Crop the image to eliminate border
        h, w, c = img.shape

        start_x = int(0.12*w)
        start_y = int(0.15*h)

        original_img = img[start_y: h - start_y, start_x: w - start_x]

        img_s = clean(img)


        cv2.imshow("Original", original_img)
        cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original", 334, 100)

        filtered = perform_ccl(img_s);
      

        concatenated_imgs = np.vstack((img_s, filtered))
        cv2.imshow("Output", concatenated_imgs)
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Output", 334, 200)

        key = cv2.waitKey()
        if key == 27: # exit on ESC
            exit(0)