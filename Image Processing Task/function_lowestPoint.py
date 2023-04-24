import numpy as np
import cv2
import copy
def find_lowestPoint(image):
    xm, ym = 0,0
    h, w = image.shape[:2]  # finding the width and height of the image
    if (h == 500 and w == 500):  # For a 500, 500 performing all the operation again with different values
        blurForLower = copy.deepcopy(image)
        blurForLower = cv2.medianBlur(blurForLower, 7)
        imgForLower = cv2.Canny(blurForLower, 150, 250)
        flag = 1
    else: # Need to perform all the necessary steps
        blurForLower = cv2.medianBlur(image, 9)
        imgForLower = cv2.Canny(blurForLower, 150, 250, apertureSize=3)
        flag = 0

    contours, hierarchy = cv2.findContours(imgForLower, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    min = 10000000
    y_max = -10000  # variable to find the highest y value because, the lowest point always have highest y value
    try:
        for i in range(len(contours)):  # Looping over all the contours and then displaying the lowest contour
            x, y, w, h = cv2.boundingRect(contours[i])  # finding the bounding rectangle coordinates of each contour
            area = w * h
            if (flag == 1):  # for 500 by 500 image
                if x > 200 and x < 300 and y > 400 and y < 470:
                    if area < min:
                        min = area
                        xm = x
                        ym = y

            else:  # for image with other than 500*500 dimension
                if x > 100:  # find the maximum y now
                    if y > y_max and y < (
                            0.9 * image.shape[0]) and y > 700:  # Just mentioning the boundary of the image
                        ym = y
                        y_max = y
                        xm = x

    except:
        print("It seems there is no desired point")
    flag = None  # Making it None so that it is again reset for next images


    return xm, ym
