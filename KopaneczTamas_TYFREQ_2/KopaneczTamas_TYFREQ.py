import cv2
import numpy as np
from matplotlib import pyplot as plt

simg = cv2.imread('street_dark.jpg', cv2.IMREAD_COLOR)
cv2.imshow('eredeti', simg)
cv2.imwrite('eredeti.png', simg)

def contrast(src):
    cnt = 80
    brght = 130
    x = np.arange(0, 256, 1)

    factor = (259 * (cnt + 255)) / (255 * (259 - cnt))
    lut = np.uint8(np.clip(brght + (factor * (np.float32(x) - 128.0) + 128), 0, 255))
    cImage = cv2.LUT(src, lut)
    return cImage
cv2.imshow('kontraszt',contrast(simg))
cv2.imwrite('kontrasztos.png', contrast(simg))

def img_gamma(src):
    lut = np.arange(0, 256, 1, np.float32)
    lut = lut / 255.0
    lut = lut ** 0.7
    lut = np.uint8(lut * 255.0)
    gammas = cv2.LUT(src, lut, None)
    return  gammas

cv2.imshow('gamma', img_gamma(simg))
cv2.imwrite('gammas.png', img_gamma(simg))

imgLab = cv2.cvtColor(simg, cv2.COLOR_BGR2Lab)
L, a, b = cv2.split(imgLab)


l_histeq = cv2.equalizeHist(L)

def normalize(src):
    th_lower = 140
    th_upper = 240
    src[src > th_upper] = th_upper
    src[src < th_lower] = th_lower
    hist_stretch = cv2.normalize(src, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return hist_stretch

def multiply(src):
    lut = np.arange(0, 256, 1, np.float32)
    lut = lut / 255.0
    lut = lut * 1.2
    lut = np.uint8(lut * 255.0)
    res = cv2.LUT(src, lut, None)
    return res

combined = cv2.merge([normalize(l_histeq), multiply(a), multiply(b)])
cv2.imshow("Combined", combined)
cv2.imwrite('combined.png', combined)

result = cv2.cvtColor(combined, cv2.COLOR_Lab2BGR)

#cv2.imshow('',imgc)
#cv2.imshow('histed_l',l_histeq)
cv2.imshow('normalized', normalize(l_histeq))
cv2.imwrite('normalized.png', normalize(l_histeq))
cv2.imshow('final', result)
cv2.imwrite('colored.png', result)

cv2.waitKey(0)