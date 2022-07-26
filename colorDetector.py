import cv2
import urllib.request
import time
import numpy as np


def nothing(x):
    pass

def flash(x):
    urllib.request.urlopen(x)

url = 'http://10.0.0.17/cam-hi.jpg'
on = 'http://10.0.0.17/ledOn'
off = 'http://10.0.0.17/ledOff'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

white = (255, 255, 255)
black = (0, 0, 0)
small = (240, 320, 3)
large = (600, 800, 3)

#cardImage = ((100, 120), (700, 525))

def halfMask(size, half):

    if size == small:
        rectMask = np.full(size, black,  dtype=np.uint8)
        rectMask = cv2.rectangle(rectMask, (58, 28), (225, 211), 0, -1)
#        rectMask = cv2.rectangle(rectMask, (237, 14), (303, 226), 0, -1)

    if size == large:
        background = np.full(size, black,  dtype=np.uint8)
        if half == 'top':
            card = cv2.rectangle(background, (100, 120), (375, 525), white, -1)
        if half == 'bottom':
            card = cv2.rectangle(background, (375, 120), (700, 525), white, -1)
        picMask = cv2.rectangle(card, (210, 165), (525, 490), black, -1)
        textMask = cv2.rectangle(picMask, (550, 150), (660, 500), black, -1)

    return textMask


flash(on)
time.sleep(0.5)

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurBGR = cv2.GaussianBlur(grayFrame, (9, 9), cv2.BORDER_DEFAULT)

    thresh = cv2.adaptiveThreshold(blurBGR, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 1)

    edges = cv2.Canny(thresh, 40, 50)
    edges = cv2.dilate(edges, (7, 7), iterations=1)

    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(frame.shape, dtype=np.uint8)
    mask = cv2.drawContours(mask, [max(contours, key=len)], -1, (255,255,255), -1)

    img2gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('mask', masked)
    cv2.imshow("live transmission", frame)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break
flash(off)
cv2.destroyAllWindows()
