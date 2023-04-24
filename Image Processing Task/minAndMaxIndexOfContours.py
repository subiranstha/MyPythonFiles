def min_xIndex(contours, index):
    min_x = 100000000
    max_y = -1000000
    for i in range(len(contours[index])):
        x = contours[index][i][0][0]
        y = contours[index][i][0][1]
        if x<min_x:
            min_x= x
            max_y = y
        elif x==min_x:
            if y>=max_y:
                max_y = y
    return min_x, max_y

def max_xIndex(contours, index):
    max_x = -100000000
    max_y = -100000000
    for i in range(len(contours[index])):
        x = contours[index][i][0][0]
        y = contours[index][i][0][1]
        if x > max_x:
            max_x = x
            max_y = y
        elif x==max_x:
            if y>=max_y:
                max_y = y
    return max_x, max_y

def topPoint(contours, index):
    top_x = contours[index][0][0][0]
    top_y = contours[index][0][0][1]

    return top_x, top_y


def bottomPoint(contours, index):
    max_y = -100000
    for i in range(len(contours[index])):
        x, y = contours[index][i][0]
        if(y>max_y):
            max_y = y
            max_x = x
    return max_x, max_y




