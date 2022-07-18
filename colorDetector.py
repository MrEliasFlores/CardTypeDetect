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


lBlue = np.array([5,80,10])
uBlue = np.array([30,255,255])

flash(on)
time.sleep(0.5)
avgImg = np.full(large[:2], black[:1], dtype=np.uint8)
frames = 0
while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurRGB = cv2.GaussianBlur(frame, (9,9), 0)

    maskTop = halfMask(large, 'top')
    maskBottom = halfMask(large, 'bottom')

    resTop = cv2.bitwise_and(frame, maskTop)
    resBot = cv2.bitwise_and(frame, maskBottom)
    maskBlue = cv2.inRange(hsvFrame, lBlue, uBlue)
    resBlue = cv2.bitwise_and(hsvFrame, hsvFrame, mask = maskBlue)
    tight = cv2.Canny(avgImg, 35, 190)
    frames += 1
    avg = np.add(avgImg, tight)
    avgEdge = np.divide(avg.astype(np.float32), frames)
    cv2.imshow('blur', blurRGB)
    cv2.imshow('edge', tight)
    #cv2.imshow('hsv', resBlue)
    cv2.imshow("live transmission", frame)
    #cv2.imshow('maskedTop', resTop)
    #cv2.imshow('maskedBottom', resBot)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break
flash(off)
cv2.destroyAllWindows()
