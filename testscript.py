# run this and modify it to test the rpi. just copy and paste into a python shell idk.

import cv2
import pyzbar
from kraken import binarization
from PIL import Image
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
w = 320
h = 180
fps = 30
camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
camera.set(cv2.CAP_PROP_FPS, fps)
ret, frame = camera.read()
# print(detect("QR", frame))
# frame = cv2.inRange(frame,(0,0,0),(200,200,200))
# frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
# frame = 255-frame # black-in-white
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite("unp.jpg", frame)
t = Image.fromarray(frame)
frame = binarization.nlbin(t)
# _, frame = cv2.threshold(
#     frame, 76, 95, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# frame = cv2.GaussianBlur(frame, (9,9), 0)
# frame = cv2.threshold(frame, 45, 255, cv2.THRESH_BINARY_INV)[1]
print(detect("QR", frame))
cv2.imwrite("img.jpg", frame)