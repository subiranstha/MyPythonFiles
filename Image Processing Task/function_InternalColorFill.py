#This function returns a contour after receiving the left contour and right internal contours:
import cv2
from minAndMaxIndexOfContours import topPoint, bottomPoint, min_xIndex, max_xIndex
import numpy as np
from fillContour import findContourforUpperBoundary, inBetweenContour
from arcFunc import convert_arc, draw_ellipse, find_ellipse_points

def internalContourFill(image, contours2): # contours2 is for the array of contours of internal contours, 0 iondex means and 1 means right
    height, width = image.shape[:2]
    dark = np.zeros((height, width), dtype=np.uint8)

    # The contour for upper boundary done in the first step:

    bottom_x_intL, bottom_y_intL = bottomPoint(contours2, 0)
    top_x_intL, top_y_intL = topPoint(contours2, 0)

    top_x_intR, top_y_intR = topPoint(contours2, 1)
    bottom_x_intR, bottom_y_intR = bottomPoint(contours2, 1)

    contours_upper, high = findContourforUpperBoundary(image)
    contour3 = inBetweenContour(contours_upper, high, top_x_intL, top_x_intR)

    # Now drawing all the contours in the dark image
    cv2.drawContours(dark, contours2, 0, (255, 255, 255), 3)  # for the left one  # intially 2
    cv2.drawContours(dark, contours2, 1, (255, 255, 255), 3)  # for the right one
    cv2.drawContours(dark, [contour3], -1, (255, 255, 255), 3)  # for the right one

    # Now the steps for the bottom one:
    center_int, radius_int, start_angle_int, end_angle_int = convert_arc((bottom_x_intL, bottom_y_intL),
        (bottom_x_intR, bottom_y_intR),(None, None), 70)

    axes_int = (radius_int, radius_int)
    draw_ellipse(dark, center_int, axes_int, 0, start_angle_int, end_angle_int, (255, 255, 255))

    contours, hierarchy = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours[0]









