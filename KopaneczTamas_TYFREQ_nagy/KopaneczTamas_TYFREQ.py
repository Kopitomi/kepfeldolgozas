import cv2 as cv2
import numpy as np

# simg = cv2.imread('img_como_jugar_al_domino_1206_600.jpg', cv2.IMREAD_COLOR)
# imgr = cv2.imread('img_como_jugar_al_domino_1206_600.jpg', cv2.IMREAD_GRAYSCALE)
# imgr = cv2.imread('domino_test.jpg', cv2.IMREAD_GRAYSCALE)
# simg = cv2.imread('domino_test.jpg', cv2.IMREAD_COLOR)
imgr = cv2.imread('domino-65136_960_720.jpg', cv2.IMREAD_GRAYSCALE)
simg = cv2.imread('domino-65136_960_720.jpg', cv2.IMREAD_COLOR)
#cv2.imshow('gray_image', imgr)
gray = cv2.cvtColor(imgr, cv2.COLOR_GRAY2BGR)

#honlapról szedett kód
def add_point_noise(img_in, percentage, value):
    noise = np.copy(img_in)
    n = int(img_in.shape[0] * img_in.shape[1] * percentage)
    print(n)
    for k in range(1, n):
        i = np.random.randint(0, img_in.shape[1])
        j = np.random.randint(0, img_in.shape[0])
        if img_in.ndim == 2:
            noise[j, i] = value
        if img_in.ndim == 3:
            noise[j, i] = [value, value, value]
    return noise
def add_salt_and_pepper_noise(img_in, percentage1, percentage2):
    n = add_point_noise(img_in, percentage1, 255)   # Só
    n2 = add_point_noise(n, percentage2, 0)         # Bors
    return n2
noise = add_salt_and_pepper_noise(simg, 0.01, 0.01)
cv2.imshow('noise', noise)

def vagas(img, rect):

    kp, r, alpha = rect[0], rect[1], rect[2]
    kp, r = tuple(map(int, kp)), tuple(map(int, r))
    x, y = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D(kp, alpha, 1)
    img_rot = cv2.warpAffine(img, M, (y, x))
    dobozolt = cv2.getRectSubPix(img_rot, r, kp)
    return dobozolt, img_rot


nblurred = cv2.blur(noise, (5, 5))
ngaussed = cv2.GaussianBlur(noise, (5, 5), sigmaX=2.0, sigmaY=2.0)
substr = cv2.subtract(nblurred, ngaussed, dtype=cv2.CV_16S)
im_blur = cv2.GaussianBlur(substr, (5, 5), 2.0)
sharped = cv2.add(simg, 0.65 * substr, dtype=cv2.CV_8UC1)
ret, thresh = cv2.threshold(imgr, 150, 250, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



i = 0
for cnt in contours:
    rbox = cv2.minAreaRect(cnt)
    pts = cv2.boxPoints(rbox).astype(np.int32)
    dobozolt, img_rot = vagas(sharped, rbox)
    if type(dobozolt) == type(None):
        continue
    if dobozolt.size <1000:
        continue
    i += 1
    outfile = 'img_crop_' + str(i) + '.jpg'
    cv2.imwrite(outfile, dobozolt)

    cv2.drawContours(simg, [pts], -1, (0, 255, 0), 3)

cv2.imshow('korvonal', simg)
cv2.imwrite('eredmeny.jpg', simg)
cv2.imshow(outfile, simg)
cv2.waitKey(0)
cv2.destroyAllWindows()


