import cv2
import numpy as np
import glob
import time

# Filtering function
def dfs(row, col, grid, n_components):
    n_rows, n_cols = grid.shape
    grid[row][col] = n_components
    if(row-1 >=0 and grid[row-1][col] == 255): dfs(row-1, col, grid, n_components)
    if(row+1 < n_rows and grid[row+1][col] == 255): dfs(row+1, col, grid, n_components)
    if(col-1 >=0 and grid[row][col-1] == 255): dfs(row, col-1, grid, n_components)
    if(col+1 < n_cols and grid[row][col+1] == 255): dfs(row, col+1, grid, n_components)


def onepass_ccl(grid):
    n_rows, n_cols = grid.shape
    n_components = 0

    for i in range(n_rows):
        for j in range(n_cols):
            if(grid[i][j] == 255):
                coordinates = []
                n_components+=1
                dfs(i, j, grid, n_components)
    return n_components

def clean(img):
    h, w, c = img.shape

    start_x = int(0.12*w)
    start_y = int(0.15*h)

    img = img[start_y: h - start_y, start_x: w - start_x]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #Thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    
    thresh_inv = cv2.bitwise_not(thresh)

    # dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilation = cv2.dilate(thresh_inv,kernel,iterations = 1)

    return dilation

if __name__ == '__main__':
    list_images = glob.glob("../CCLData/PatnaCaptchaScreenShots/*.png")

    for i, image in enumerate(list_images):
        # image = "../CCLData/CaptchaType2/stars.jpeg"
        img = cv2.imread(image)

        h, w, c = img.shape

        start_x = int(0.12*w)
        start_y = int(0.15*h)

        cropped_img = img[start_y: h - start_y, start_x: w - start_x]

        
        ### Threshold the image
        clean_img = clean(img)
        # threshinv = cv2.bitwise_not(clean_img)
        # cv2.imwrite("tempfile.png", threshinv)
        
        ### Perform one pass CCL algorithm
        copy_dilation = clean_img.copy()

        start = time.time()
        n_components = onepass_ccl(copy_dilation)
        print("Time taken: {}".format(time.time()-start))

        print("Number of components: ", n_components)

        ### Eliminating unwanted components
        mask = np.zeros(copy_dilation.shape, dtype="uint8")

        min_area = 50   # Area of the component should be greater than min_area to be kept in the mask

        for i in range(1, n_components+1):
            if(np.count_nonzero(copy_dilation==i) > min_area):
                componentMask = (copy_dilation == i).astype("uint8") * 255
                mask = cv2.bitwise_or(mask, componentMask)
        
        # stacked_imgs = np.vstack((clean_img, mask))
        cv2.imshow("Original", cropped_img)
        cv2.imshow("Binary Thresholded Image", clean_img)
        cv2.imshow("Noise Removed", mask)
        cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original", 334, 100)
        cv2.namedWindow("Binary Thresholded Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Binary Thresholded Image", 334, 100)
        cv2.namedWindow("Noise Removed", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Noise Removed", 334, 100)

        cv2.waitKey(0)