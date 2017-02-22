#-*- coding: utf-8 -*-
import cv2
import time

motion_limit_value = 130000
limit_value_count = 5

def motion_detect():
    img1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    img2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = 1
    count = 0
    while True:
        img = cam.read()[1]
        d1 = cv2.absdiff(img3, img2)
        d2 = cv2.absdiff(img2, img1)
        value = cv2.countNonZero(cv2.bitwise_and(d1, d2))
        print value
        if value >= motion_limit_value:
            t = 0.5
            count += 1
            if count > limit_value_count:
                print "Motion!"
                count = 0
        else:
            t = 1
            count = 0
            
        img1 = img2
        img2 = img3
        img3 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        time.sleep(t)
    
if __name__ == "__main__":
    try:
        cam = cv2.VideoCapture(0)
    except:
        print "fail to get camera"
        sys.exit(1)
        
    try:
        motion_detect()
    except KeyboardInterrupt as e:
        print "Bay"
        