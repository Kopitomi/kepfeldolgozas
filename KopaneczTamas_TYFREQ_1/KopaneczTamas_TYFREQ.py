import cv2

clk = 0
sugar = 10
color = (0, 0, 255)
img = cv2.imread('rajz_alap.png')
img2 = img

#img = np.ndarray((480, 640, 3), np.uint8)
#img.fill(255)
def mouse_click(event, x, y, flags, param):
    # Globalis valtozo atvetele
    global clk, sugar, color

    if event == cv2.EVENT_LBUTTONDOWN:
        clk = 1
        cv2.circle(img, (x, y), sugar, color, -1)
        cv2.imshow('rajz felulet', img)
    if event == cv2.EVENT_MOUSEMOVE:
        if clk == 1:
            cv2.circle(img, (x, y), sugar, color, -1)
            cv2.imshow('rajz felulet', img)
    if event == cv2.EVENT_LBUTTONUP:
        clk = 0


cv2.imshow('rajz felulet', img)
cv2.imshow('masolat', img2)
cv2.setMouseCallback('rajz felulet', mouse_click)

#cv2.waitKey(0)
while clk == 0 or clk == 1:
    cv2.imshow('masolat', img2)
    key = cv2.waitKeyEx(100)

    if key == 27 or key == ord('q'):
        print('Lenyomott billentyű és kódja:', chr(key), key)
        break
    if key == ord('s'):
        cv2.imwrite('KopaneczTamas_TYFREQ.png', img)
    if key == ord('r'):
        color = [0, 0, 255]
    if key == ord('g'):
        color = [0, 255, 0]
    if key == ord('b'):
        color = [255, 0, 0]
    if key == ord('k'):
        color = [0, 0, 0]
    if key == ord('w'):
        color = [255, 255, 255]
    if key == ord('-'):
        sugar -= 5
        if sugar < 5:
            sugar = 5
    if key == ord('+'):
        sugar += 5
        if sugar > 100:
            sugar = 100
    if key == ord('t'):
        img = cv2.imread('rajz_alap.png')
        img2 = img

cv2.destroyAllWindows()