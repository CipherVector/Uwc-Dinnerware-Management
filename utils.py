import firebase_admin
from firebase_admin import db
import datetime
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
from pyzbar import pyzbar
import numpy as np
import dbr
import time


class FirebaseApi:
    def __init__(self, credFilePath, databaseUrl):
        cred_obj = firebase_admin.credentials.Certificate(credFilePath)
        firebase_admin.initialize_app(cred_obj, {
            'databaseURL': databaseUrl
        })
        self.ref = db.reference('/database/checkedOut')

    def checkOut(self, userId, cupId):
        contents = self.ref.get()
        print(contents)
        for item in contents:
            item = contents[item]
            if not item['returned'] and item['cupId'] == cupId:
                print("item already exists")
                return
        self.ref.push().set({
            "abandoned": False,
            "returned": False,
            "timeCheckedOut": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "cupId": cupId,
            "userId": userId,
            "email_sent": False
        })
        print("success")

    def returnItem(self, cupId, abandoned=False):
        for key, item in self.ref.get().items():
            if item['cupId'] == cupId and not item['returned']:
                self.ref.child(key).update(
                    {'returned': True, 'abandoned': abandoned})
                return
        print("no item wth id")

    def abandonedItems(self):
        abandonedUserIds = {}
        for key, item in self.ref.get().items():
            expiretime = int(datetime.datetime.timestamp(
                datetime.datetime.now())) + 60 * 60 * 24
            if (not item['returned'] and item['abandoned'] == False) or (item['email_sent'] == False and item['abandoned'] == True):
                if expiretime > item['timeCheckedOut']:
                    self.ref.child(key).update({'abandoned': True})
                    if abandonedUserIds.get(item['userId'], None):
                        abandonedUserIds[item['userId']].append(key)
                    else:
                        abandonedUserIds[item['userId']] = [key]

        return abandonedUserIds

    def getAbandoned(self, userId):
        userId = str(userId)
        abandoned = []
        for _, item in self.ref.get().items():
            if str(item['userId']) == userId and item['abandoned']:
                abandoned.append(item)

        return abandoned

    def visualize(self):
        contents = self.ref.get()
        cupsout = 0
        cupsin = 0
        allcupsindb = set()
        alluniquecupsindb = set()
        for item in contents:
            item = contents[item]

            allcupsindb.add(item['cupId'])
            if not item['returned']:
                cupsout = cupsout + 1
        for cups in allcupsindb:
            if cups not in alluniquecupsindb:
                alluniquecupsindb.add(cups)
        totalcups = len(alluniquecupsindb)
        cupsin = totalcups - cupsout
        return cupsin, cupsout


def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])


def setfourccmjpg(cap):
    oldfourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    codec = cv2.VideoWriter_fourcc(*'MJPG')
    res = cap.set(cv2.CAP_PROP_FOURCC, codec)
    if res:
        print("codec in ", decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))
    else:
        print("error, codec in ", decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))


def detect(detectType, windowName, image, pixel_format):
    if detectType == "QR":
      try:
          buffer = image.tobytes()
          height = image.shape[0]
          width = image.shape[1]
          stride = image.strides[0]
          start = time.time()
          results = reader.decode_buffer_manually(buffer, width, height, stride, pixel_format, "")
          end = time.time()


          if results != None:
              for result in results:
                  print("Barcode Format : ")
                  print(result.barcode_format_string)
                  print("Barcode Text : ")
                  print(result.barcode_text)
                  if (result.barcode_format_string == "QR_CODE"):
                      if (type(int(result.barcode_text)) == int):
                          return(result.barcode_text)

      except:
        print("Error")

 
    if detectType == "BARCODE":
      try:
          buffer = image.tobytes()
          height = image.shape[0]
          width = image.shape[1]
          stride = image.strides[0]
          start = time.time()
          results = reader.decode_buffer_manually(buffer, width, height, stride, pixel_format, "")
          end = time.time()


          if results != None:
              for result in results:
                  print("Barcode Format : ")
                  print(result.barcode_format_string)
                  print("Barcode Text : ")
                  print(result.barcode_text)
                  if (result.barcode_format_string == "BARCODE"):
                      if (type(int(result.barcode_text)) == int):
                          return(result.barcode_text)

      except:
          print("Error")

def camera(detectType):
    # camera = cv2.VideoCapture(0)
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    w = 1920
    h = 1080
    fps = 30
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    camera.set(cv2.CAP_PROP_FPS, fps)
    ret, frame = camera.read()
    # camera = PiCamera()
    # raw_capture = PiRGBArray(camera)
    # time.sleep(0.1)
    # camera.capture(raw_capture, format="bgr")
    # image = raw_capture.array
    while ret:
        ret, frame = camera.read()
        # camera.capture(raw_capture, format="bgr")
        # image = raw_capture.array
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(
            frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        frame = detect(detectType, frame)
        if type(frame) != numpy.ndarray:
            print(str(frame))
            return frame
        # cv2.imshow('Barcode', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        time.sleep(0.1)
    # camera.release()
    cv2.destroyAllWindows()


def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
