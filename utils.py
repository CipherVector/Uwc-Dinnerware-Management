import firebase_admin
from firebase_admin import db
import datetime
import cv2
from pyzbar import pyzbar
import numpy

class FirebaseApi:
    def __init__(self, credFilePath, databaseUrl, locationId):
        cred_obj = firebase_admin.credentials.Certificate(credFilePath)
        firebase_admin.initialize_app(cred_obj, {
	        'databaseURL': databaseUrl
    	})
        self.locationId = locationId
        self.ref = db.reference('/database/checkedOut')


    def checkOut(self, userId, cupId):
        contents = self.ref.get()
        for item in contents:
            item = contents[item]
            if not item['returned'] and item['cupId'] == cupId:
                print("item already exists")
                return
        self.ref.push().set({
            "abandoned": False,
            "returned": False,
            "timeCheckedOut": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "locationId": self.locationId,
            "cupId": cupId,
            "userId": userId
        })

    def returnItem(self, cupId, abandoned = False):
        for key, item in self.ref.get().items():
            if item['cupId'] == cupId and not item['returned']:
                self.ref.child(key).update({'returned': True, 'abandoned': abandoned})
                return
        print("no item wth id")

def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def setfourccmjpg(cap):
    oldfourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    codec = cv2.VideoWriter_fourcc(*'MJPG')
    res=cap.set(cv2.CAP_PROP_FOURCC,codec)
    if res:
        print("codec in ",decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))
    else:
        print("error, codec in ",decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))
	
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        print(barcode_info)
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
        if barcode_info:
            frame = barcode_info
    return frame

def read_barcodes_return(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        print(barcode_info)
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        api.returnItem(barcode_info)
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
        if barcode_info:
            frame = barcode_info
    return frame

def camera():
    camera = cv2.VideoCapture(0)
    w=19200
    h=1080
    fps=100000
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,w)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,h)
    camera.set(cv2.CAP_PROP_FPS,fps)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        frame = read_barcodes(frame)
        if type(frame) != numpy.ndarray:
            return frame
        cv2.imshow('Barcode', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
