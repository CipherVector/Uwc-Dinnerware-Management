import firebase_admin
from firebase_admin import db
import datetime
from dotenv import dotenv_values
import cv2
from pyzbar import pyzbar


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        print(barcode_info)
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame


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

config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'], config['db_url'], config['location_id'])
def camera():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 10)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        frame = read_barcodes(frame)
        cv2.imshow('Barcode', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
camera()
