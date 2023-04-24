import numpy as np
import copy
import cv2

def slicing_main(image, flag=0, top_y_extL= None, top_y_extR= None):

    if(flag==0): # It means slicing is for the first or for external contours:
        output = np.zeros_like(image)
        startOfI = 0
        endOfI = image.shape[0]
        startOfJ = 0
        endOfJ = int((image.shape[1])/2)

        output = LeftToRightSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ)

        startOfI = 0
        endOfI = image.shape[0]
        startOfJ = int((image.shape[1])/2)
        endOfJ = image.shape[1]
        output = RightToLeftSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ)

    else: # It means now its for internal contour:
        output = np.zeros_like(image)
        startOfI = 0
        endOfI = image.shape[0]
        startOfJ = int((image.shape[1])/2)
        endOfJ = top_y_extR   # We have to subtract to further the internal contour from the external contour
        output = LeftToRightSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ)

        startOfI = 0
        endOfI = image.shape[0]
        startOfJ = top_y_extL # We have to add to distant the internal contour from the external cotnour
        endOfJ = int((image.shape[1])/2)
        output = RightToLeftSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ)

    return output

def LeftToRightSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ):
    for i in range(startOfI, endOfI):
        count = 0
        for j in range(startOfJ, endOfJ):  # for j in range(int((image.shape[1])/2)):
            # If the current value is 255 and there are at least 8 more 255s to the right, keep only the second-last 5
            if (count > 0):
                count = count - 1
                continue
            if image[i][j] == 255 and (checkImage(image, i, j) == 1):
                output[i, j] = 0
            elif (image[i][j] == 255 and (checkImage(image, i, j)) == 2):

                output[i, j - 3] = 0
                output[i, j - 2] = 0  # 0
                output[i, j - 1] = 255
                output[i, j] = 255
                output[i, j + 1] = 255
                output[i, j + 2] = 0   #0  because eta ko right tira janu parne ho tei vayera right tira ko picel lai value deko ho!!
                output[i, j + 3] = 0

                count = 3
            # Otherwise, copy the value from the input array
            else:
                continue
    return output

def RightToLeftSlicing(output, image, startOfI, endOfI, startOfJ, endOfJ):

    for i in range(startOfI, endOfI):
        count = 0
        for j in reversed(range(startOfJ, endOfJ)):
            if(count>0):
                count = count-1
                continue

            if image[i][j] == 255 and (checkImageReversed(image, i, j)==1):
                output[i, j] = 0
            # Otherwise, copy the value from the input array
            elif(image[i][j] == 255 and (checkImageReversed(image, i, j)==2)):

                #output[i, j+3]= 0
                output[i, j+2] =0   # 0
                output[i, j+1]=255    #255
                output[i, j]=255
                output[i, j-1]=255
                output[i, j-2]=0     #0 because eta ko left tira aaunu pryo, so left ko pixel ma value deko ho
                output[i, j-3]=0


                count = 3

            else:
                continue

    return output



def checkImage(image, i, j):
    if(image[i][j+1]==255 and image[i][j+2]==255 and image[i][j+3]==255 and image[i][j+4]==255): # Check for 5 continuous values
        return 1
    elif((image[i][j+1]==255 and image[i][j+2]==255 and image[i][j+3]==255)): # means only 4 neighbors are there
        return 2


def checkImageReversed(image, i,j):
    if(image[i][j-1]==255 and image[i][j-2]==255 and image[i][j-3]==255 and image[i][j-4]==255):
        return 1
    elif ((image[i][j - 1] == 255 and image[i][j - 2] == 255 and image[i][j - 3] == 255)):  # means only 4 neighbors are there
        return 2

def largestAndsecondlargest(contours):
    max = -10000
    second_max = -10000
    third_max = -10000
    for i in range(len(contours)):
        x = cv2.arcLength(contours[i], False)
        if(x>max):
            max = x
            ind1 = i
    for i in range(len(contours)):
        x = cv2.arcLength(contours[i], False)
        if(x>second_max and ind1 !=i):
            second_max = x
            ind2 = i

    x_ind1, y_ind1 = contours[ind1][0][0]

    if(x_ind1 > 250): # means it is incorrect
        temp = copy.deepcopy(ind1)
        ind1 = copy.deepcopy(ind2)
        ind2 = copy.deepcopy(temp)

    x_ind2, y_ind2 = contours[ind2][0][0]

    for i in range(len(contours)):
        x = cv2.arcLength(contours[i], False)
        if(x>third_max and ind1 !=i and ind2!=i):
            third_max = x
            ind3 = i

    x_ind3, y_ind3 = contours[ind3][0][0]
    if(x_ind3>x_ind2):
        temp = copy.deepcopy(ind2)
        ind2 = copy.deepcopy(ind3)
        ind3 = copy.deepcopy(ind2)


    return ind1, ind2
