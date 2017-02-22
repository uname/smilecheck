#-*- coding: utf-8 -*-
import cv2
import time
import json
import urllib2
import urllib

wx_server_url = "http://115.159.213.156/motion"
motion_limit_value = 123000
limit_value_count = 5

def on_motion_detected():
    print "motion detected"
    res = urllib2.urlopen(wx_server_url + "?motion_str=19", timeout=5)
    print res.read()
    
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
            t = 0.2
            count += 1
            if count > limit_value_count:
                on_motion_detected()
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
        #on_motion_detected()
    except KeyboardInterrupt as e:
        print "Bay"
        
