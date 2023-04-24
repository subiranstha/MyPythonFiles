# This function will sort the contours in descending order and not only that will also return the contour in their adjusted loctaion
# For example, in index 0 will be the extreme left contour and also in index 1 will be the extreme right contour
import copy
import cv2
from minAndMaxIndexOfContours import topPoint, bottomPoint, min_xIndex, max_xIndex

def sortAndAdjustContours(contours):
    contours = list(contours)
    for i in range(len(contours)):
        len_i = cv2.arcLength(contours[i], False)
        for j in range(i, len(contours)):
            len_j = cv2.arcLength(contours[j], False)
            if(len_j > len_i):
                temp = copy.deepcopy(len_i)
                len_i = copy.deepcopy(len_j)
                len_j = copy.deepcopy(temp)

                temp = contours[i].copy()
                contours[i] = contours[j].copy()
                contours[j] = temp.copy()

    # At this point all the sorted contours are in the variable contours now we just have to ensure that at index 0 is the extreme left contour
    # and at index is the extreme right contours:
    x_left, y_left = topPoint(contours, 0)
    ind_left = 0

    for i in range(1, 4):
        x, y = topPoint(contours, i)
        leng = cv2.arcLength(contours[i], False)
        if(x<x_left and leng>500):
            x_left = copy.deepcopy(x)
            ind_left = i

    temp = contours[0].copy()
    contours[0] = contours[ind_left].copy()
    contours[ind_left] = temp.copy()
    # For the right one:
    x_right, y_right = topPoint(contours, 1)
    ind_right = 1

    for i in range(2, 4):
        leng = cv2.arcLength(contours[i], False)
        x, y = topPoint(contours, i)
        if(x>x_right and leng>500):
            x_right = copy.deepcopy(x)
            ind_right = i

    temp = contours[1].copy()
    contours[1] = contours[ind_right].copy()
    contours[ind_right] = temp.copy()

    contours = tuple(contours)
    return contours




