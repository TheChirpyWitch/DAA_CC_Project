import cv2
import glob
import os
import numpy as np
import time

def clean(img):
    # Crop the image to eliminate border
    h, w, c = img.shape

    start_x = int(0.12*w)
    start_y = int(0.15*h)

    img = img[start_y: h - start_y, start_x: w - start_x]

    # Gray scale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    thresh_inv = cv2.bitwise_not(thresh)

    # Morphing (dilating)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilation = cv2.dilate(thresh_inv, kernel, iterations = 1)
    
    # dilation = cv2.bitwise_not(dilation)
    return dilation

def perform_ccl(image):
    start = time.time()
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, 4, cv2.CV_32S)
    print("Time taken: {}".format(time.time()-start))

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
        
        # print("Area: {}".format(area))

        # Ensure that the area of the component is greater than 50 to be considered as a component
        keepArea = area > 50
        

        # ensure the connected component we are examining passes all
        # three tests
        if keepArea:
            # construct a mask for the current connected component and
            # then take the bitwise OR with the mask
            # print("[INFO] keeping connected component '{}'".format(i))
            componentMask = (labels == i).astype("uint8") * 255
            mask = cv2.bitwise_or(mask, componentMask)
    

    print("Number of components: ", numLabels)
    return mask
    
if __name__ == '__main__':
    list_images = glob.glob("../CCLData/PatnaCaptchaScreenShots/*.png")
    for i, image in enumerate(list_images):
        
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

        cv2.imshow("Input and Output", concatenated_imgs)
        cv2.namedWindow("Input and Output", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Input and Output", 334, 200)

        print("Click on the output window anywhere and press any button on the keyboard except the Escape button...")
        key = cv2.waitKey()
        if key == 27: # exit on ESC
            exit(0)