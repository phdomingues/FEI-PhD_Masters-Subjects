import cv2
import math
import numpy as np

np.set_printoptions(precision=3, threshold=np.inf, linewidth=np.inf, suppress=True)

def get_roi(src, pt1, pt2):

    col1, col2 = (pt1[0], pt2[0]) if pt1[0] < pt2[0] else (pt2[0], pt1[0])
    row1, row2 = (pt1[1], pt2[1]) if pt1[1] < pt2[1] else (pt2[1], pt1[1])
    return src[row1:row2, col1:col2]

def get_gradient_direction_line(avg_dir, cellUpperLeft, cellW, cellH, scale=0.8):

    halfScale = scale/2;
    centrePt = (int(cellUpperLeft[0] + (cellW/2)), int(cellUpperLeft[1] + (cellH/2)))
    strtPt = (int(centrePt[0] - (cellW * halfScale * math.cos(avg_dir))), int(centrePt[1] - (cellH * halfScale * math.sin(avg_dir))))
    endPt = (int(centrePt[0] + (cellW * halfScale * math.cos(avg_dir))), int(centrePt[1] + (cellH * halfScale * math.sin(avg_dir))))
    return [strtPt, endPt]

def get_gradient_directions_arrows(direction, kernel_w=3, kernel_h=3):

    arrows = np.zeros(direction.shape, dtype=np.uint8)
    n_cols = int(direction.shape[1] / kernel_w)
    n_rows = int(direction.shape[0] / kernel_h)

    for c in range(n_cols):
        # # Draw grid lines
        # cv2.line(arrows, (c*kernel_w, 0), (c*kernel_w, direction.shape[0]), (255,255,255), 1)
        # cv2.line(arrows, (0, c*kernel_h), (direction.shape[1], c*kernel_h), (255,255,255), 1)

        for r in range(n_rows):
            roiUpperleft = (c*kernel_w, r*kernel_h)
            roi = get_roi(direction, roiUpperleft, ((c+1)*kernel_w, (r+1)*kernel_h))
            avg_dir = cv2.mean(roi)[0]
            arrow_pnts = get_gradient_direction_line(avg_dir, roiUpperleft, kernel_w, kernel_h)
            cv2.arrowedLine(arrows, arrow_pnts[0], arrow_pnts[1], (255,255,255), 1)

    return arrows

def get_gradient_directions_colours(direction, kernel_w=3, kernel_h=3):
    # (red=0°; yellow=60°, green=120°, blue=240°...)

    hsv = np.zeros((direction.shape[0], direction.shape[1], 3), dtype=np.uint8)
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
    n_cols = int(direction.shape[1] / kernel_w)
    n_rows = int(direction.shape[0] / kernel_h)

    for c in range(n_cols):
        # Draw grid lines
        cv2.line(hsv, (c*kernel_w, 0), (c*kernel_w, direction.shape[0]), (180,255,255), 1)
        cv2.line(hsv, (0, c*kernel_h), (direction.shape[1], c*kernel_h), (180,255,255), 1)

        for r in range(n_rows):
            roiUpperleft = (c*kernel_w, r*kernel_h)
            roi = get_roi(direction, roiUpperleft, ((c+1)*kernel_w, (r+1)*kernel_h))
            avg_dir = cv2.mean(roi)[0]
            # avg_dir will be value between 0-359. HSV hue needs a value between 0-179
            avg_dir /= 2
            arrow_pnts = get_gradient_direction_line(avg_dir, roiUpperleft, kernel_w, kernel_h)
            cv2.rectangle(hsv, roiUpperleft, ((c+1)*kernel_w, (r+1)*kernel_h), (avg_dir, 255,255), -1)

    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

def main():
    src = cv2.imread('images/test_image.jpg', 0)

    # Calculate gradient magnitude and direction for the image
    dX = cv2.Sobel(src, cv2.CV_32F, 1, 0)
    dY = cv2.Sobel(src, cv2.CV_32F, 0, 1)
    mag, direction = cv2.cartToPolar(dX, dY, angleInDegrees=True)

    arrows = get_gradient_directions_arrows(direction, 8, 8)
    colours = get_gradient_directions_colours(direction, 10, 10)

    cv2.imshow('src', src)
    cv2.imshow('arrows', arrows)
    cv2.imshow('colours', colours)

    cv2.waitKey(0)

main()