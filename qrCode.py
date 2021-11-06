import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import pyqrcode


# code = pyqrcode.create('bang')
# code.png('bang.png', scale=10)
#
# db = decode(Image.open('bang.png'))
# print(db)

cap = cv2.VideoCapture(0)

while(True):

    ret, img = cap.read()

    for i in decode(img):
        print(i.data.decode('utf-8'))

    cv2.imshow('img', img)
    cv2.waitKey(1)

cv2.relaese()
cv2.destroyAllWindows()
