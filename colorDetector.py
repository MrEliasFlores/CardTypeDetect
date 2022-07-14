import cv2
import urllib.request
import numpy as np


def nothing(x):
    pass

def flash(x):
    urllib.request.urlopen(x)

url = 'http://10.0.0.17/cam-hi.jpg'
##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
on = 'http://10.0.0.17/ledOn'
off = 'http://10.0.0.17/ledOff'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
loRes = (240, 320)
midRes = (530, 350)
hiRes = (600, 800)
l_h, l_s, l_v = 10, 5, 75
u_h, u_s, u_v = 50, 135, 240


def statMask(size):

    if size == loRes:
        rectMask = np.full(loRes, 255,  dtype=np.uint8)
        rectMask = cv2.rectangle(rectMask, (15, 235), (225, 300), 0, -1)
        rectMask = cv2.rectangle(rectMask, (25, 55), (225, 300), 0, -1)//255
        rectMask = cv2.threshold(rectMask, 127, 255, cv2.THRESH_BINARY)

    if size == midRes or size == hiRes:
        rectMask = np.full(hiRes, 255,  dtype=np.uint8)
        rectMask = cv2.rectangle(rectMask, (30, 580), (565, 760), 0, -1)
        rectMask = cv2.rectangle(rectMask, (80, 135), (535, 570), 0, -1)//255
        #rectMask = cv2.rectangle(rectMask, (15, 260), (330, 330), 0, -1)
        #rectMask = cv2.rectangle(rectMask, (35, 60), (310, 250), 0, -1)//255
        print(rectMask.shape[:2])

#    if size == hiRes:
#        rectMask = np.full(hiRes, 255, dtype=np.uint8)
#        rectMask = cv2.rectangle(rectMask, (30, 580), (565, 760), 0, -1)
#        rectMask = cv2.rectangle(rectMask, (80, 135), (535, 570), 0, -1)//255

    return rectMask

while True:
    flash(on)
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)
    # _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)
    mask2 = statMask(hiRes)
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 2000:
            cv2.drawContours(frame, [c], -1, (255, 0, 0), 3)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "blue", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    res = cv2.bitwise_and(frame, frame, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)
    cv2.imshow('mask2', res2)
    cv2.imshow("live transmission", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break
flash(off)
cv2.destroyAllWindows()