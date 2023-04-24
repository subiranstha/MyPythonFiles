import copy
import numpy as np
import cv2
def slicing_function(img):
    m, n = img.shape
    new_arr = np.zeros(img.shape, np.uint8)
    a=b=c=d =0
    for i in range(m):
        for j in range(int(n/2)):
            if(img[i][j]==255):
                if(img[i][j+1]==255 and img[i][j+2]==255 and img[i][j+3]==255 and img[i][j+4]==255):
                    new_arr[i][j] = 0
                    a = 1
                elif(img[i][j+1]==255 and img[i][j+2]==255 and img[i][j+3]==255 and a ):
                    a=0
                    b = 1
                    new_arr[i][j] = 255
                elif(img[i][j+1]==255 and img[i][j+2]==255 and b):
                    b = 0
                    c =1
                    new_arr[i][j] = 255
                elif(img[i][j+1]==255 and img[i][j+2]==0 and  c):
                    c = 0
                    d =1
                    new_arr[i][j] = 255
                elif(img[i][j+1]==0 and d):
                    d = 0
                    new_arr[i][j] = 255
                else:
                    continue
    a=b=c=d=e=0
    for i in range(m):
        for j in reversed(range((int(n/2)), n)):
            if (img[i][j]==255):
                if(img[i][j-1]==255 and img[i][j-2]==255 and img[i][j-3]==255 and img[i][j-4]==255 and img[i][j-5]==255):
                    a=1
                    new_arr[i][j] = 0
                elif(img[i][j-1]==255 and img[i][j-2]==255 and img[i][j-3]==255 and img[i][j-4]==255 and  a):
                    a=0
                    b=1
                    new_arr[i][j] = 255
                elif(img[i][j-1]==255 and img[i][j-2]==255 and img[i][j-3]==255 and b):
                    b =0
                    c=1
                    new_arr[i][j] = 255
                elif(img[i][j-1]==255 and img[i][j-2]==255 and c):
                    c=0
                    d=1
                    new_arr[i][j] = 255
                elif(img[i][j-1]==0 and img[i][j-2]==255 and  d):
                    d=0
                    e= 1
                    new_arr[i][j] = 255
                elif(img[i][j-1]==255 and e):
                    e=0
                    new_arr[i][j] = 255

                else:
                    continue


    return new_arr


def new_slicing_function(img):
    m, n = img.shape
    new_arr = np.zeros(img.shape, np.uint8)
    for i in range(m):
        for j in range(int(n/2)):
            if(img[i][j]==255):
                if(img[i][j+1]==255 and img[i][j+2]==255 and img[i][j+3]==255 and img[i][j+4]==0 and img[i][j+5]==0): # only till 3 was here
                    new_arr[i][j]=0
                elif(img[i][j+1]==255 and img[i][j+2]==255 and img[i][j+3]==0 and img[i][j+4]==0 and img[i][j+5]==0):
                    new_arr[i][j] = 255
                elif(img[i][j+1]==255 and img[i][j+2]==0 and img[i][j+3]==0 and img[i][j+4]==0 and img[i][j+5]==0):
                    new_arr[i][j] = 255
                elif(img[i][j+1]==0 and img[i][j+2]==0 and img[i][j+3]==0 and img[i][j+4]==0 and img[i][j+5]==0): # only till 2 was here
                    new_arr[i][j] = 255
                else:
                    continue


    for i in range(m):
        for j in reversed(range((int(n/2)), n)):
            if (img[i][j]==255):
                if(img[i][j-1]==255 and img[i][j-2]==255 and img[i][j-3]==255 and img[i][j-4]==0 and img[i][j-5]==0):
                    new_arr[i][j] = 0
                elif(img[i][j-1]==255 and img[i][j-2]==255 and img[i][j-3]==0 and img[i][j-4]==0 and img[i][j-5]==0):
                    new_arr[i][j] = 255
                elif(img[i][j-1]==255 and img[i][j-2]==0 and img[i][j-3]==0 and img[i][j-4]==0 and img[i][j-5]==0):
                    new_arr[i][j] = 255
                elif(img[i][j-1]==0 and img[i][j-2]==0 and img[i][j-3]==0 and img[i][j-4]==0 and img[i][j-5]==0):
                    new_arr[i][j] = 255
                else:
                    continue


    return new_arr
















