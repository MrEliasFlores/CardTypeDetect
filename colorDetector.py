import cv2
import urllib.request
import time
import numpy as np

def flash(x):
    urllib.request.urlopen(x)

url = 'http://10.0.0.17/cam-hi.jpg'
on = 'http://10.0.0.17/ledOn'
off = 'http://10.0.0.17/ledOff'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

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
    edges = cv2.dilate(edges, (9, 9), iterations=2)

    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxContour = [max(contours, key=len)]

    mask = np.zeros(frame.shape, dtype=np.uint8)
    mask = cv2.drawContours(mask, maxContour, -1, (255, 255, 255), -1)

    peri = cv2.arcLength(maxContour[0], True)
    corners = cv2.approxPolyDP(maxContour[0], 0.04*peri, True)
    result = frame.copy()
    cv2.polylines(result, [corners], True, (0,255,0), 1, cv2.LINE_AA)

    frameCopy = frame.copy()
    maskCopy = np.zeros(frameCopy.shape, dtype=np.uint8)

    cv2.fillPoly(maskCopy, [corners], color=(255,255,255))
    _,maskTest = cv2.threshold(frameCopy, 10,255, cv2.THRESH_BINARY)
    print(frameCopy.shape, maskCopy.shape)
    print(frameCopy)
    maskTst = cv2.bitwise_and(frameCopy,frameCopy, mask=maskTest)
    cv2.imshow('asdf', frameCopy)

    img2gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('maskTest', maskTst)
    cv2.imshow('boundingBox', result)
    cv2.imshow('Mask', masked)
    cv2.imshow("live transmission", frame)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break
flash(off)
cv2.destroyAllWindows()
