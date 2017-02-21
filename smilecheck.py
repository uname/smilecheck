#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smilecheck.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    check if the face in picture is smiling by face++ api
    register in https://www.faceplusplus.com.cn/ to get APP-KEY and APP_SECRET
    then set them as env vars: FACEPLUSPLUS_KEY and FACEPLUSPLUS_SECRET
    after that you can exec like this:
    ./capsmile.py  img-file-path
"""

import sys
import os
import time
import json
import urllib2
import urllib

detect_api_url  = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
analyze_api_url = 'https://api-cn.faceplusplus.com/facepp/v3/face/analyze'
api_detect = "detect"
api_analyze = "analyze"
smile_value_limit = 70

try:
    key = os.environ["FACEPLUSPLUS_KEY"]       #"juCTJEOOR2N-I5ee8nIoF7KoRyUbA6DL"
    secret = os.environ["FACEPLUSPLUS_SECRET"] #"YD-fXK1ykb2PAwbiVo8rDl3GYS7D1hzY"
except KeyError as e:
    print "please set env: FACEPLUSPLUS_KEY and FACEPLUSPLUS_SECRET"
    sys.exit(1)

def base_data():
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    
    return boundary, data

def img_data(imgpath):
    try:
        fr = open(imgpath,'rb')
        data = fr.read()
        fr.close()
        return data
    except:
        print "fail to read image data"

def add_post_imgdata(data, boundary, imgdata):
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="co33.jpg"' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgdata)
    data.append('--%s--\r\n' % boundary)
    return data

def detect_request_data(imgpath):
    imgdata = img_data(imgpath)
    if imgdata is None:
        return None, None
        
    boundary, data = base_data()
    add_post_imgdata(data, boundary, imgdata)
    
    return boundary, data
    
def analyze_request_data(imgpath, face_token):
    imgdata = img_data(imgpath)
    if imgdata is None:
        return None, None

    boundary, data = base_data()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_tokens')
    data.append(face_token)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append('smiling')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    add_post_imgdata(data, boundary, imgdata)
    
    return boundary, data
    
def do_request(imgpath, api=api_detect, face_token=""):
    
    boundary, data, url = None, "", ""
    if api == api_detect:
        url = detect_api_url
        boundary, data = detect_request_data(imgpath)
    elif api == api_analyze:
        url = analyze_api_url
        boundary, data = analyze_request_data(imgpath, face_token)
        
    if boundary is None:
        return
    
    http_body = '\r\n'.join(data)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    
    try:
        resp = urllib2.urlopen(req, timeout=5)
        jsonstr = resp.read()
        return jsonstr
        
    except Exception,e:
        print 'http error',e    
    
def is_smiling(imgpath):
    jsonstr = do_request(imgpath, api=api_detect)
    if not jsonstr:
        print "error response api: %s" % api_detect
        return
    
    try:
        pydict = json.loads(jsonstr)
    except ValueError as e:
        print "fail to parse json string: %s" % e.__str__()
        return
    
    faces = pydict.get("faces", [])
    face_num = len(faces)
    if face_num < 1:
        print "no face detected!"
        return
    
    if face_num > 1:   # just keep a log here, always process the first face
	pass
        #print "more than one face"
    
    face = faces[0]
    face_token = face.get("face_token", "")
    if face_token == "":
        print "bad face token, API ERROR!!"
        sys.exit(1)
    
    jsonstr = do_request(imgpath, api_analyze, face_token.encode("utf-8"))
    if not jsonstr:
        print "error response api: %s" % api_analyze
        return
    
    try:
        pydict = json.loads(jsonstr)
    except ValueError as e:
        print "fail to parse json string: %s" % e.__str__()
        return
    
    if len(pydict.get("faces", [])) < 1:
        print "no face detected!"
        return
    
    smile = pydict["faces"][0].get("attributes", {}).get("smile", {})
    value = smile.get("value", 0)
    print value
    return value >= smile_value_limit
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./%s  img-path\n" % os.path.basename(sys.argv[0])
	sys.exit(1)

    if is_smiling(sys.argv[1]):
        print ":)"
    else:
        print ":-|"
