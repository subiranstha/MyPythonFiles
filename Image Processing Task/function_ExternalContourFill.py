# This function will return the conrour for filling the full external things:
import copy
import cv2
from peronaMaliktest import PeronaMalik
from minAndMaxIndexOfContours import topPoint, bottomPoint, min_xIndex, max_xIndex
import numpy as np
from fillContour import findContourforUpperBoundary, inBetweenContour
from arcFunc import convert_arc, draw_ellipse, find_ellipse_points
from slicing_openAI_revised import slicing_main, largestAndsecondlargest
from function_lowestPoint import find_lowestPoint


def externalContourFill(image, contours1):
    height, width = image.shape[:2]
    dark = np.zeros((height, width), dtype=np.uint8)

    top_x_extL, top_y_extL = topPoint(contours1, 0)
    top_x_extR, top_y_extR = topPoint(contours1, 1)
    bottom_x_extL, bottom_y_extL = max_xIndex(contours1, 0)
    bottom_x_extR, bottom_y_extR = min_xIndex(contours1, 1)

    contours_upper, high = findContourforUpperBoundary(image) # image must be the copy of temp, unprocessed one
    contour3 = inBetweenContour(contours_upper, high, top_x_extL, top_x_extR)

    cv2.drawContours(dark, contours1, 0, (255, 255, 255), 3)
    cv2.drawContours(dark, contours1, 1, (255, 255, 255), 3)
    cv2.drawContours(dark, [contour3], -1, (255, 255, 255), 3)

    # Now finding the lowest point and drawing the curve in the dark image
    low_x, low_y = find_lowestPoint(image)
    if (low_x == 0 and low_y == 0):  # means we only have two points available
        center_ext, radius_ext, start_angle_ext, end_angle_ext = convert_arc((bottom_x_extL, bottom_y_extL),
            (bottom_x_extR, bottom_y_extR), (None, None), 70)

    else:
        center_ext, radius_ext, start_angle_ext, end_angle_ext = convert_arc((bottom_x_extL, bottom_y_extL),
            (bottom_x_extR, bottom_y_extR), (low_x, low_y), None)

    axes_ext = (radius_ext, radius_ext)
    draw_ellipse(dark, center_ext, axes_ext, 0, start_angle_ext, end_angle_ext, (255, 255, 255))

    contours, hierarchy = cv2.findContours(dark, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours[0]


#def differenceContour(image, contours1, contours2):
#
 #   height, width = image.shape[:2]
  #  dark1 = np.zeros((height, width), dtype=np.uint8)
   # dark2






