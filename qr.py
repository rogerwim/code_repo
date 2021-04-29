import qrcode
import cv2 as cv
import time
import numpy
from PIL import Image
crop = True
qr = qrcode.QRCode()
data = open("qr.py","rb").read()
qr.add_data(data)
qr.make()
points1 = None
points1_def = False
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
img.show()
camera = cv.VideoCapture(1)
camera.set(3,1920)
camera.set(4,1080)
while True:
    
    return_value, im = camera.read()
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    if points1_def:
        n = len(points1)
        points1 = points1.astype(numpy.int32)
        for j in range(n):
            cv.line(im, tuple(points1[j]), tuple(points1[ (j+1) % n]), (255,0,0), 5)
    if retval:
        points1_def = True
        points1 = points[0]
        print(retval)
        try:
            codeObject = compile(retval,"read_from_qr",'exec')
            exec(codeObject)
        except:
            print("invalid code")
    if points1_def and retval:
        im = cv.cvtColor(im,cv.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        x1 = 100000
        x2 = 0
        y1 = 100000
        y2 = 0
        for cood in points1:
            if cood[0] <= x1:
                x1 = cood[0]
            if cood[0] >= x2:
                x2 = cood[0]
            if cood[1] <= y1:
                y1 = cood[1]
            if cood[1] >= y2:
                y2 = cood[1]
            print(cood)
        print(x1,x2,y1,y2)
        im = im.crop(tuple([x1-10,y1-10,x2+10,y2+10]))
        im = numpy.asarray(im)
        im = cv.cvtColor(im,cv.COLOR_RGB2BGR)
        cv.imshow('image',im)
    if retval:
        w = int(straight_qrcode.shape[0] * 20)
        h = int(straight_qrcode.shape[1] * 20)
        d = (w,h)
        straight_qrcode = cv.resize(straight_qrcode,d,cv.INTER_AREA)
        cv.imshow('perfect',straight_qrcode)
    cv.waitKey(1)
    cv.imshow('image',im)
    cv.waitKey(1)
