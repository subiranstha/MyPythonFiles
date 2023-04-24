import cv2
import numpy as np
def convert_arc(pt1, pt2, pt3, sagitta):
    if sagitta is not None: # means we have three points

        x1, y1 = pt1
        x2, y2 = pt2

        n = np.array([y2 - y1, x1 - x2])
        n_dist = np.sqrt(np.sum(n**2))

        if np.isclose(n_dist, 0):
            print('Error: The distance between pt1 and pt2 is too small.')

        n = n/n_dist
        x3, y3 = (np.array(pt1) + np.array(pt2))/2 + sagitta * n

    else:
        x1, y1 = pt1
        x2, y2 = pt2
        x3, y3 = pt3

    """""
    pts = sorted([pt1, pt2, pt3], key = lambda p:p[1])
    pt1, pt2, pt3 = pts[0], pts[1], pts[2]
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    """""

    A = np.array([
        [x1**2 + y1**2, x1, y1, 1],
        [x2**2 + y2**2, x2, y2, 1],
        [x3**2 + y3**2, x3, y3, 1]])
    M11 = np.linalg.det(A[:, (1, 2, 3)])
    M12 = np.linalg.det(A[:, (0, 2, 3)])
    M13 = np.linalg.det(A[:, (0, 1, 3)])
    M14 = np.linalg.det(A[:, (0, 1, 2)])

    if np.isclose(M11, 0):
        # catch error here, the points are collinear (sagitta ~ 0)
        print('Error: The third point is collinear.')

    cx = 0.5 * M12/M11
    cy = -0.5 * M13/M11
    radius = np.sqrt(cx**2 + cy**2 + M14/M11)

    # calculate angles of pt1 and pt2 from center of circle becuase we need the starting and ending angles
    pt1_angle = 180*np.arctan2(y1 - cy, x1 - cx)/np.pi
    pt2_angle = 180*np.arctan2(y2 - cy, x2 - cx)/np.pi

    return (cx, cy), radius, pt1_angle, pt2_angle

def draw_ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness=3, lineType=cv2.LINE_AA, shift=10):
    center = (
        int(round(center[0] * 2**shift)),
        int(round(center[1] * 2**shift))
    )
    axes = (
        int(round(axes[0] * 2**shift)),
        int(round(axes[1] * 2**shift))
    )
    #print(center, axes, angle, startAngle, endAngle)

    return cv2.ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness, lineType, shift)

def find_ellipse_points(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness=3, lineType=cv2.LINE_AA, shift=10):
    center = (
        int(round(center[0] * 2**shift)),
        int(round(center[1] * 2**shift))
    )
    axes = (
        int(round(axes[0] * 2**shift)),
        int(round(axes[1] * 2**shift))
    )

    all_points = cv2.ellipse2Poly(center, axes, angle, startAngle, endAngle, 1)
    return all_points