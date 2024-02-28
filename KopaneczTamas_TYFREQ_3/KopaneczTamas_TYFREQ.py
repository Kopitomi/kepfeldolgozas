import cv2 as cv2
import numpy as np

#simg = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_COLOR)
#imgr = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_GRAYSCALE)
simg = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_COLOR)
imgr = cv2.imread('car_numberplate_rs.jpg', cv2.IMREAD_GRAYSCALE)

gray_color = cv2.cvtColor(imgr, cv2.COLOR_GRAY2BGR)
#cv2.imshow('eredeti', simg)

alak = cv2.MORPH_RECT
ret = cv2.getStructuringElement(alak,(7,7))

def struktoral(src):
    dst1 = cv2.dilate(src,ret,1)
    eroz1 = cv2.erode(dst1,ret,1)
    eroz2 = cv2.erode(eroz1,ret,1)
    dst2 = cv2.dilate(eroz2,ret,1)
    return dst2
cv2.imshow("step1", struktoral(simg))

gaussed = cv2.GaussianBlur(struktoral(simg), (5, 5), sigmaX=4.0)
cv2.imshow('step2', gaussed)

b, g, r = cv2.split(gaussed)
max = cv2.max(g, b)
cv2.imshow('step3', max)

substr = cv2.subtract(r, max)
#cv2.imshow('step4', substr)

im_thresh = np.ndarray(substr.shape, substr.dtype)
im_thresh.fill(0)
im_thresh[substr > 50] = 255
cv2.imshow('step4', im_thresh)

im_thresh_line = cv2.Canny(im_thresh, 100, 200)
cv2.imshow('step5', im_thresh_line)

gray_color[im_thresh_line == 255] = (0, 0, 255)
cv2.imshow('step6', gray_color)

#cv2.imwrite('result_TYFREQ.png', gray_color)

cv2.waitKey(0)